import signal
import socket
import sys
import threading
from threading import Lock

__author__ = 'Mostafa Khaki'

__doc__ = " This module written for Broadcasting (admin usage)"

clients = []
lock = Lock()


class Client(threading.Thread):
    def __init__(self, ip, _port, connection):
        threading.Thread.__init__(self)
        self.connection = connection
        self.ip = ip
        self.port = _port

    def run(self):
        pass

    def send_msg(self, msg):
        self.connection.sendall(msg.encode())


class Server:
    def __init__(self, ip, _port):
        self.ip = ip
        self.port = _port
        self.address = (self.ip, self.port)
        self.server = None

    def open_socket(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind(self.address)
        except socket.error:
            if self.server:
                self.server.close()
            sys.exit(1)

    def run(self, *args, **kwargs):
        self.open_socket()
        self.server.listen(5)

        while True:
            lock.acquire()
            connection, (ip, _port) = self.server.accept()

            print(f'\na client with ip: {ip} , port: {_port} joined...')

            c = Client(ip, _port, connection)
            c.start()
            c.join()

            clients.append(c)
            lock.release()


class Admin:
    def run(self, *args, **kwargs):
        while True:
            msg = input("admin >")

            for client in clients:
                client.send_msg(msg)


if __name__ == '__main__':
    host = input('host ( default 127.0.0.1): ') or '127.0.0.1'
    port = input('port (default 12345): ') or 12345
    server = Server(host, int(port))
    admin = Admin()

    server_thread = threading.Thread(target=server.run)
    admin_thread = threading.Thread(target=admin.run)

    server_thread.start()
    admin_thread.start()

    server_thread.join()
    admin_thread.join()

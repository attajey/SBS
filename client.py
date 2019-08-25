import socket

__author__ = 'Mostafa Khaki'


def client(_host, _port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f'Trying to connect to the server: {_host}, ({_port})')
        s.connect((_host, _port))
        print("Connected ...")
        while True:
            resp = s.recv(4096).decode()  # str

            print(f'admin > {resp}')


if __name__ == "__main__":
    host = input('host ( default 127.0.0.1): ') or '127.0.0.1'
    port = input('port (default 12345): ') or 12345
    client(_host=host, _port=int(port))

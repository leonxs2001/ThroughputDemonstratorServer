import socket
import time
from enum import Enum


class DataUnit(Enum):
    GB = 1024 ** 3
    MB = 1024 ** 2
    KB = 1024
    B = 1


HOST = '127.0.0.1'
PORT = 65432

BUFFER_SIZE = 1024
DATA_AMOUNT = 1
DATA_UNIT = DataUnit.GB
DATA_SIZE = DATA_AMOUNT * DATA_UNIT.value


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print('Server is waiting for connection...')
        conn, addr = s.accept()
        with conn:
            print('Connected with', addr)
            conn.sendall(f"{BUFFER_SIZE};{DATA_SIZE}".encode())

            response = conn.recv(1024).decode()

            if response == "ready":
                print("Start sending data.")
                dummy_data = b'A' * DATA_SIZE
                conn.sendall(dummy_data)
            else:
                print("Can not start sending data.")


if __name__ == '__main__':
    start_server()

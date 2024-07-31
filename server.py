import os
import socket
from enums import DataUnit, SendingType, CommunicationType

HOST = 0.0.0.0 # Set host here
PORT = 65432 # Set port here

BUFFER_SIZE = 1024
DATA_AMOUNT = 1
DATA_UNIT = DataUnit.GB
DATA_SIZE = DATA_AMOUNT * DATA_UNIT.value
SEND_DUMMY_BYTE = b"A"
DOWNLOADABLE_FILE = r"C:\Users\user\myfile.file" # Set file here
DIRECTORY_PATH = "files"


def start_server():
    if not os.path.exists(DIRECTORY_PATH):
        os.makedirs(DIRECTORY_PATH)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        while True:

            s.listen()
            print('Server is waiting for connection...')
            conn, addr = s.accept()
            with conn:
                print('Connected with', addr)
                communication_type_data, sending_type_data = conn.recv(BUFFER_SIZE).decode().split(";")
                sending_type = SendingType.from_string(sending_type_data)
                communication_type = CommunicationType.from_string(communication_type_data)
                conn.sendall(b"\x01")

                try:
                    if sending_type == SendingType.DUMMY:
                        if communication_type == CommunicationType.DOWNLOAD:
                            send_dummy_data(conn)
                        else:
                            receive_dummy_data(conn)
                    else:
                        if communication_type == CommunicationType.DOWNLOAD:
                            send_file(conn)
                        else:
                            receive_file(conn)
                except Exception as e:
                    print(e)


def send_file(conn):
    buffer_size = int(conn.recv(BUFFER_SIZE).decode())
    filename = os.path.basename(DOWNLOADABLE_FILE)
    filesize = os.path.getsize(DOWNLOADABLE_FILE)
    conn.sendall(f"{filename};{filesize}".encode())
    if conn.recv(1) == b"\x01":
        with open(DOWNLOADABLE_FILE, 'rb') as f:
            while True:
                bytes_read = f.read(buffer_size)
                if not bytes_read:
                    break
                conn.sendall(bytes_read)
    else:
        print("Can not start sending data. Client is not ready.")


def send_dummy_data(conn):
    buffer_size_data, data_size_data = conn.recv(BUFFER_SIZE).decode().split(";")
    buffer_size = int(buffer_size_data)
    data_size = int(data_size_data)
    numbers_of_iteration = data_size / buffer_size
    for _ in range(int(numbers_of_iteration)):
        conn.sendall(SEND_DUMMY_BYTE * buffer_size)
    missing_data = SEND_DUMMY_BYTE * (data_size - buffer_size * int(numbers_of_iteration))
    if missing_data:
        conn.sendall(missing_data)


def receive_dummy_data(conn):
    buffer_size = int(conn.recv(BUFFER_SIZE).decode())

    conn.sendall(b"\x01")

    received_data = "data"
    while received_data:
        received_data = conn.recv(buffer_size)


def receive_file(conn):
    buffer_size_data, filename = conn.recv(BUFFER_SIZE).decode().split(";")
    buffer_size = int(buffer_size_data)

    filepath = os.path.join(DIRECTORY_PATH, filename)

    os.path.exists(filepath)

    name, extension = os.path.splitext(filename)
    i = 1
    while True:
        new_filename = f"{name}_{i}{extension}"
        new_filepath = os.path.join(DIRECTORY_PATH, new_filename)
        if not os.path.exists(new_filepath):
            filepath = new_filepath
            break
        i += 1

    conn.sendall(b"\x01")

    with open(filepath, 'wb') as file:
        received_data = conn.recv(buffer_size)
        while received_data:
            file.write(received_data)
            received_data = conn.recv(buffer_size)


if __name__ == '__main__':
    start_server()

import os
import socket
from enums import DataUnit, SendingType, CommunicationType

HOST = "192.168.137.1"  # "192.168.137.7"  # '127.0.0.1' #192.168.137.7
PORT = 65432

BUFFER_SIZE = 1024
DATA_AMOUNT = 1
DATA_UNIT = DataUnit.GB
DATA_SIZE = DATA_AMOUNT * DATA_UNIT.value
SEND_DUMMY_BYTE = b"A"
DOWNLOADABLE_FILE = r"C:\Users\fbi-user\Documents\MODSYS\Masterarbeit.pdf"


def start_server():
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

                if sending_type == SendingType.DUMMY:
                    if communication_type == CommunicationType.DOWNLOAD:
                        send_dummy_data(conn)
                    else:
                        receive_dummy_data(conn)
                else:
                    send_file(conn)



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

if __name__ == '__main__':
    start_server()

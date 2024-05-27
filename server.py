import socket
from enums import DataUnit, SendingType

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

            sending_type = SendingType.from_string(conn.recv(1024).decode())
            if sending_type == SendingType.DUMMY:
                conn.sendall(b"\x01")
                buffer_size_data, data_size_data = conn.recv(1024).decode().split(";")
                print((buffer_size_data, data_size_data))
                buffer_size = int(buffer_size_data)
                data_size = int(data_size_data)
                numbers_of_iteration = data_size / buffer_size
                for _ in range(int(numbers_of_iteration)):
                    conn.sendall(b"A" * buffer_size)

                missing_data = b"A" * (data_size - buffer_size * int(numbers_of_iteration))
                if missing_data:
                    conn.sendall(missing_data)


if __name__ == '__main__':
    start_server()

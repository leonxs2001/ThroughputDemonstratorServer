import socket

HOST = '127.0.0.1'
PORT = 65432


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print('Server is waiting for connection...')
        conn, addr = s.accept()
        with conn:
            print('Connected with', addr)

            buffer_and_data_size_data = conn.recv(1024).decode()
            buffer_size_data, data_size_data = buffer_and_data_size_data.split(";")

            buffer_size = int(buffer_size_data)
            data_size = int(data_size_data)

            print('Buffer size:', buffer_size)
            print('Data size:', data_size)

            conn.sendall(b'ready')

            received_data_amount = 0
            print(f"Received Data 0%")
            while received_data_amount < data_size:
                chunk = conn.recv(buffer_size)
                if not chunk:
                    break
                received_data_amount += buffer_size
                percent = (received_data_amount / data_size) * 100
                print(f"Received Data {percent:.2f}%")
            print("Receiving ended")
            s.close()


if __name__ == '__main__':
    start_server()

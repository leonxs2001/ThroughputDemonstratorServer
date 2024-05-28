import socket
import time

from enums import DataUnit, SendingType

HOST = '127.0.0.1'
PORT = 65432
BUFFER_SIZE = 1024


def get_buffer_size():
    buffer_size = input("Enter buffer size in B ( is set to 1024 if no value is given): ")
    if not buffer_size:
        buffer_size = 1024
    return buffer_size


def get_data_size():
    choice_unit = input(
        "Which unit for datasize do you prefer B (enter B), KB (enter KB), MB (enter MB) or GB (enter GB)?").upper()

    multiplier = DataUnit.from_string(choice_unit).value[1]

    data_size = input(f"Enter data size (in {choice_unit}): ")

    return int(data_size) * multiplier


def get_sending_type():
    sending_type = input(
        "Do you wanna download a real file (enter file) or dummy data (enter dummy). In case of dummy data you can decide which size the data have.")
    return SendingType.from_string(sending_type)


def start_client():
    sending_type = get_sending_type()
    buffer_size = int(get_buffer_size())
    data_size = 0
    if sending_type == SendingType.DUMMY:
        data_size = int(get_data_size())

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        s.sendall(sending_type.value.encode())
        ready_signal = s.recv(1)

        if ready_signal == b'\x01':
            execution_time_seconds = 0
            if sending_type == SendingType.DUMMY:
                    s.sendall(f"{buffer_size};{data_size}".encode())

                    print(f"Received Data 0%")
                    start_time = time.time()

                    numbers_of_iteration = data_size / buffer_size
                    for i in range(int(numbers_of_iteration)):
                        s.recv(buffer_size)
                        percent = ((i + 1) / numbers_of_iteration) * 100
                        print(f"Received Data {percent:.2f}%")

                    difference = numbers_of_iteration - int(numbers_of_iteration)
                    if difference:
                        s.recv(int(difference * buffer_size))
                        print(f"Received Data 100%")
                    end_time = time.time()

                    execution_time_seconds = end_time - start_time
            else:
                s.sendall(str(buffer_size).encode())
                filename, filesize_data = s.recv(BUFFER_SIZE).decode().split(";")
                filesize = int(filesize_data)
                s.sendall(b'\x01')

                numbers_of_iteration = filesize / buffer_size
                with open(f"{filename}", 'wb') as file:
                    start_time = time.time()
                    for i in range(int(numbers_of_iteration)):
                        chunk = s.recv(buffer_size)
                        if not chunk:
                            break
                        file.write(chunk)
                        percent = ((i + 1) / numbers_of_iteration) * 100
                        print(f"Received Data {percent:.2f}%")

                    difference = numbers_of_iteration - int(numbers_of_iteration)
                    if difference:
                        chunk = s.recv(buffer_size)
                        if chunk:
                            file.write(chunk)
                        print(f"Received Data 100%")
                    end_time = time.time()
                    execution_time_seconds = end_time - start_time

            execution_time_minutes = execution_time_seconds // 60
            execution_time_seconds -= execution_time_minutes * 60
            execution_time_milliseconds = int((execution_time_seconds - int(execution_time_seconds)) * 1000)
            execution_time_seconds = int(execution_time_seconds)
            print(
                f"Receiving ended. Execution time is {execution_time_minutes} minutes, {execution_time_seconds} seconds and {execution_time_milliseconds} milliseconds.")

        else:
            print("Can not start sending data. Server is not ready")



if __name__ == '__main__':
    start_client()

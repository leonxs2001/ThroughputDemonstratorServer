import socket
import time

HOST = '127.0.0.1'
PORT = 65432


def get_buffer_size():
    buffer_size = input("Enter buffer size in B ( is set to 1024 if no value is given): ")
    if not buffer_size:
        buffer_size = 1024
    return buffer_size


def get_data_size():
    choice_unit = input(
        "Which unit for datasize do you prefer B (enter B), KB (enter KB), MB (enter MB) or GB (enter GB)?").upper()

    if choice_unit == "B":
        multiplier = 1
    elif choice_unit == "KB":
        multiplier = 1024
    elif choice_unit == "MB":
        multiplier = 1024 ** 2
    elif choice_unit == "GB":
        multiplier = 1024 ** 3
    else:
        raise Exception("Nothing valid entered.")

    data_size = input(f"Enter data size (in {choice_unit}): ")

    return int(data_size) * multiplier


def start_client():
    buffer_size = get_buffer_size()
    data_size = get_data_size()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        buffer_and_data_size_data = s.recv(1024).decode()
        buffer_size_data, data_size_data = buffer_and_data_size_data.split(";")
        buffer_size = int(buffer_size_data)
        data_size = int(data_size_data)

        print('Buffer size:', buffer_size)
        print('Data size:', data_size)

        s.sendall(b'ready')

        received_data_amount = 0
        print(f"Received Data 0%")
        start_time = time.time()
        while received_data_amount < data_size:
            chunk = s.recv(buffer_size)
            if not chunk:
                if received_data_amount == 0:
                    start_time = time.time()
                break
            received_data_amount += buffer_size
            percent = (received_data_amount / data_size) * 100
            print(f"Received Data {percent:.2f}%")
        end_time = time.time()
        execution_time_seconds = end_time - start_time
        execution_time_minutes = execution_time_seconds // 60
        execution_time_seconds -= execution_time_minutes * 60
        execution_time_hours = execution_time_minutes // 60
        execution_time_minutes -= execution_time_hours * 60
        execution_time_milliseconds = int((execution_time_seconds - int(execution_time_seconds)) * 1000)
        execution_time_seconds = int(execution_time_seconds)
        print(
            f"Receiving ended. Execution time is {execution_time_hours} hours, {execution_time_minutes} minutes, {execution_time_seconds} seconds and {execution_time_milliseconds} milliseconds.")

        """s.sendall(f"{buffer_size};{data_size}".encode())

        response = s.recv(1024).decode()

        if response == "ready":
            print("Start sending data.")
            dummy_data = b'A' * data_size
            s.sendall(dummy_data)
            s.close()
        else:
            print("Can not start sending data.")
            s.close()"""


if __name__ == '__main__':
    start_client()

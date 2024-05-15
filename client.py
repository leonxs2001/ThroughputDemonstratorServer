import socket

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

        s.sendall(f"{buffer_size};{data_size}".encode())

        response = s.recv(1024).decode()

        if response == "ready":
            print("Start sending data.")
            dummy_data = b'A' * data_size
            s.sendall(dummy_data)
            s.close()
        else:
            print("Can not start sending data.")
            s.close()


if __name__ == '__main__':
    start_client()

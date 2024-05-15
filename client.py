import socket

HOST = '127.0.0.1'
PORT = 65432


def start_client():
    buffer_size = input("Enter buffer size in B ( is set to 1024 if no value is given): ")
    if not buffer_size:
        buffer_size = 1024

    choice_unit = input("Which unit for datasize do you prefer B (enter B), KB (enter KB), MB (enter MB) or GB (enter GB)?").upper()

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

    print(multiplier)

    data_size = input(f"Enter data size (in {choice_unit}): ")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        byte_amount = int(data_size) * multiplier

        s.sendall(f"{buffer_size};{byte_amount}".encode())

        response = s.recv(1024).decode()
        print(response)

        if response == "ready":
            print("Start sending data.")
            dummy_data = b'A' * byte_amount
            s.sendall(dummy_data)
            s.close()
        else:
            print("Can not start sending data.")
            s.close()


if __name__ == '__main__':
    start_client()

import socket
import threading
import random
import time

# ? key for DES


def generate_session_key() -> str:
    arr = '123456789ABCDEFF'
    key = ''
    for _ in range(16):
        key += arr[random.randint(0, len(arr) - 1)]
    return key


def decrypt1(c) -> None:
    print('\n\ndecrypt1')

    with open(".key/privateKey-b.txt", "r") as f:
        d = f.read().split('\n')
        n = int(d[1])
        d = int(d[0])

    m = pow(int(c), d, n)
    with open(".key/n-a.txt", "w") as f:
        print(str(m)[0], file=f)

    with open(".key/id-a.txt", "w") as f:
        print(str(m)[1:], file=f)
    print(f'raw: {c}, dec: {m}')


def encrypt1() -> str:
    print('\n\nencrypt1')

    with open(".key/n-a.txt", "r") as f:
        n1 = int(f.read())

    with open(".key/n-b.txt", "r") as f:
        id = f.read()

    with open(".key/publicKey-a.txt", "r") as f:
        e = f.read().split('\n')
        n = int(e[1])
        e = int(e[0])

    m = n1 * 10 ** len(id) + int(id)
    c = pow(m, e, n)
    print(f'raw: {m}, enc: {c}')
    return str(c)


def decrypt2(c) -> None:
    print('\n\ndecrypt2')

    with open(".key/privateKey-b.txt", "r") as f:
        d = f.read().split('\n')
        n = int(d[1])
        d = int(d[0])

    m = pow(int(c), d, n)

    # ? check if N2 is the same
    with open(".key/n-b.txt", "r") as f:
        n1 = f.read().replace('\n', '')
        if n1 != str(m)[0]:
            print('N2 is not the same! Aborting')
            exit()
    print(f'raw: {m}, enc: {c}')


def encrypt2(key) -> str:
    print('\n\nencrypt2')

    m = int(key, 16)
    with open(".key/publicKey-a.txt", "r") as f:
        e = f.read().split('\n')
        n = int(e[1])
        e = int(e[0])

    c = pow(m, e, n)
    print(f'raw: {m}, enc: {c}')
    return str(c)

# ? my own code
def handle_client(client_socket):
    for i in range(2):
        message = ''
        data = client_socket.recv(1024).decode('utf-8')

        if i == 0:
            decrypt1(data)
            message = encrypt1()
            client_socket.send(message.encode('utf-8'))
        elif i == 1:
            decrypt2(data)
            key = generate_session_key()
            print('key = ', key)
            for j in range(0, 16, 2):
                subkey = key[j:j+2]
                message = encrypt2(subkey)
                print(j, j+1)
                print(subkey)
                print(message)
                time.sleep(1)
                client_socket.send(message.encode('utf-8'))
    client_socket.close()

# ? chatGPT code
'''
def handle_client(client_socket):
    while True:
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            break

        if len(data) > 1:
            if data[0] == '1':
                data = decrypt(data[1::])

        print(f"Received message: {data}")
        response = input("Enter your response: ")
        client_socket.send(response.encode('utf-8'))
    client_socket.close()
'''


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Enable SO_REUSEADDR
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind(('0.0.0.0', 5555))  # Use an available port number
    server.listen(5)
    print("Server listening for connections...")

    # ? my own code
    client, addr = server.accept()
    print(f"Accepted connection from {addr}")
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()

    # ? chatGPT code
'''    
    while True:
        client, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()
'''
if __name__ == "__main__":
    start_server()
    # key = generate_sesion_key()
    # print(key)
    # print(key[0:2])

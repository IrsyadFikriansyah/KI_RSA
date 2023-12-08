import socket

def encrypt1() -> str:
    print('\n\nencrypt1')
    with open(".key/n-a.txt", "r") as f:
        n1 = int(f.read())

    with open(".key/id-a.txt", "r") as f:
        id = f.read()

    with open(".key/publicKey-b.txt", "r") as f:
        e = f.read().split('\n')
        n = int(e[1])
        e = int(e[0])

    m = n1 * 10 ** len(id) + int(id) # combining n1 and id_a

    if m >= n:
        print('Error! m > n')
        exit()

    c = pow(m, e, n) # performing encryption
    print(f'raw: {m}, enc: {c}')
    return str(c)

def decrypt1(c) -> None:
    print('\n\ndecrypt1')
    with open(".key/privateKey-a.txt", "r") as f:
        d = f.read().split('\n')
        n = int(d[1])
        d = int(d[0])

    m = pow(int(c), d, n)
    
    # ? check if N1 is the same
    with  open(".key/n-a.txt", "r") as f:
        n1 = f.read().replace('\n', '')
        if n1 != str(m)[0]:
            print('N1 is not the same! Aborting')
            exit()

    # ? saving N2
    with open(".key/n-b.txt", "w") as f:
        print(str(m)[1:], file = f)
    print(f'raw: {c}, dec: {m}')
    
def encrypt2() -> str:
    print('\n\nencrypt2')
    with open(".key/n-b.txt", "r") as f:
        m = int(f.read())

    with open(".key/publicKey-b.txt", "r") as f:
        e = f.read().split('\n')
        n = int(e[1])
        e = int(e[0])

    if m >= n:
        print('Error! m > n')
        exit()

    c = pow(m, e, n) # performing encryption
    print(f'raw: {m}, enc: {c}')
    return str(c)

def decrypt2(c) -> str:
    print('\n\ndecrypt2')
    with open(".key/privateKey-a.txt", "r") as f:
        d = f.read().split('\n')
        n = int(d[1])
        d = int(d[0])

    print(c, type(c))

    m = pow(int(c), d, n)
    print(m, type(m))
    return str(m)

def store_symmetric_key(key) -> None:
    with open(".key/symmetric_key.txt", "w") as f:
        print(key, file = f)

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = '127.0.0.1'
    server_port = 5555
    client.connect((server_ip, server_port))

    response = ''
    for i in range(0, 2):
        message = ''
        if i == 0:
            message = encrypt1()
        elif i == 1:
            decrypt1(response)
            message = encrypt2()
            client.send(message.encode('utf-8'))
            key = ''
            for _ in range(8):
                response = client.recv(1024).decode('utf-8')
                key += hex(int(decrypt2(response))).replace('0x', '')
            store_symmetric_key(key)
            print(key)
            break
        else:
            break
        client.send(message.encode('utf-8'))
        response = client.recv(1024).decode('utf-8')
        print(f"Received response: {response}")
    client.close()
        
if __name__ == "__main__":
    start_client()

import threading
import socket

host = '' # your server host wich can be your pc or your server (PUT IN THE QUOTES THE IP ADDRESS OF YOUR HOST)
port =  # put a port higher than 10000 (THE PORT MUST NOT BE IN PARENTHESES OR QUOTES)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} ha rage quittato'.encode('ascii'))
            nickname.remove(nickname)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"Connetced with {str(address)}")

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'nickname of the client is {nickname}!')
        broadcast(f'{nickname} joined the chat'. encode('ascii'))
        client.send('Connected to the server!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server is ready...")
receive()

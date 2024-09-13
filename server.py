import socket
import threading
from datetime import datetime

HOST = ""  # Bind to all interfaces
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
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
            if message.startswith(b'/private'):  # Handle private messages
                target_nickname, private_message = message[8:].decode('utf-8').split(':', 1)
                send_private_message(target_nickname, private_message, client)
            elif message == b'/list':  # List connected users
                user_list = ', '.join(nicknames)
                client.send(f"Connected users: {user_list}".encode('utf-8'))
            elif message.startswith(b'/nick'):  # Change nickname
                new_nickname = message[6:].decode('utf-8')
                change_nickname(client, new_nickname)
            elif message:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f"{nicknames[clients.index(client)]} [{timestamp}]: {message.decode('utf-8')}")
                broadcast(f"{nicknames[clients.index(client)]} [{timestamp}]: {message.decode('utf-8')}".encode('utf-8'))
            else:
                raise Exception("Message is empty")
        except Exception as e:
            print(f"Error: {e}")
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            broadcast(f"{nickname} has left the chat.".encode('utf-8'))
            break

def send_private_message(target_nickname, private_message, sender_client):
    if target_nickname in nicknames:
        target_index = nicknames.index(target_nickname)
        target_client = clients[target_index]
        sender_nickname = nicknames[clients.index(sender_client)]
        target_client.send(f"[Private from {sender_nickname}]: {private_message}".encode('utf-8'))
    else:
        sender_index = clients.index(sender_client)
        sender_client.send(f"User {target_nickname} not found.".encode('utf-8'))

def change_nickname(client, new_nickname):
    index = clients.index(client)
    old_nickname = nicknames[index]
    nicknames[index] = new_nickname
    client.send(f"Nickname changed from {old_nickname} to {new_nickname}".encode('utf-8'))
    broadcast(f"{old_nickname} is now known as {new_nickname}".encode('utf-8'))

def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}!")
        client.send("NICKNAME".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)
        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} has joined the chat.".encode('utf-8'))
        client.send("Connected to the server.".encode('utf-8'))
        threading.Thread(target=handle, args=(client,)).start()

print("Server running...")
receive()

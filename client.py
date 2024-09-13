import socket
import threading

HOST = '127.0.0.1'  # Localhost
PORT = 9090         # Same as server's port

def listen_for_messages_from_server(client):
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            if message:
                print(message)
            else:
                print("Server disconnected.")
                break
        except:
            print("An error occurred!")
            client.close()
            break

def communicate_to_server(client):
    username = input("Enter your username: ")
    client.send(username.encode())

    threading.Thread(target=listen_for_messages_from_server, args=(client,)).start()
    send_message_to_server(client)

def send_message_to_server(client):
    while True:
        message = input("")
        if message.startswith('/'):
            client.send(message.encode())
        else:
            client.send(message.encode())

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
        print("Successfully connected to server")
    except Exception as e:
        print(f"Unable to connect to the server at {HOST}:{PORT}. Error: {e}")
        return

    communicate_to_server(client)

if __name__ == '__main__':
    main()

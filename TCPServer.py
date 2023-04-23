import json
from socket import *
import threading
from message import I_AM_ALIVE_RESPONSE, Message
from typing import List

BUFFER_SIZE = 1024
PORT = 12000

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('', PORT))
server_socket.listen(1)

print('The server is ready to receive')


def add_client(sender: socket):
    """Add a new client to the list if it doesn't already exist."""
    _port = sender.getsockname()[1]
    for client in clients:
        if client.getsockname()[1] == _port:
            return
    clients.append(sender)


def i_am_alive(_, sender):
    # Broadcast the message to all connected clients
    response = I_AM_ALIVE_RESPONSE(clients)
    add_client(sender)
    broadcast(response, sender)


actions = {
    1: i_am_alive,
}

# Store a list of connected clients
clients: List[socket] = []


def broadcast(data, sender):
    """Send a message to all connected clients except the sender."""
    for client in clients:
        if client != sender:
            client.send(data)
    print(data)


def handle_client(sender, client_address):
    """Manage communication with a single client."""
    print(f"New connection from {client_address}")

    # Add the client to the list of connected clients

    while True:
        try:
            # Receive data from the client
            request = sender.recv(BUFFER_SIZE)
            json_data = json.loads(request)
            request = Message(**json_data)

            if request:
                actions.get(request.action)(request, sender)

            else:
                # If no data is received, remove the client from the list of connected clients
                clients.remove(sender)
                print(f"Connection closed with {client_address}")
                sender.close()
                break
        except Exception as e:
            print(f"Error: {e}")
            if sender in clients:
                clients.remove(sender)
            sender.close()
            break


while True:
    # Wait for a new client to connect
    _client_socket, client_address = server_socket.accept()

    # Create a new thread to handle communication with the client
    thread = threading.Thread(target=handle_client,
                              args=(_client_socket, client_address))
    thread.start()

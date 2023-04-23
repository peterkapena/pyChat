from dataclasses import dataclass
import json
from socket import *
import threading
from message import JSON, Message, client
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
    with clients_lock:
        for client in clients:
            if client.getsockname()[1] == _port:
                return
        clients.append(sender)


def i_am_alive(_, sender: socket):
    cls = []
    for c in clients:
        peer = c.getpeername()
        cls.append(client(peer[0], peer[1]))

    if len(cls) > 0:
        broadcast(cls, sender)


def broadcast(data, sender: socket):
    """Send a message to all connected clients except the sender."""

    json_string = json.dumps(data, cls=JSON)

    # print(json_string)
    for c in clients:
        if c.getpeername() != sender.getpeername():
            c.send("json.dumps(data.__dict__)".encode())
            c.send(json_string.encode())
    print(data)


actions = {
    1: i_am_alive,
}

# Store a list of connected clients
clients: List[socket] = []

# Create a lock to synchronize access to the clients list
clients_lock = threading.Lock()


def handle_client(sender, client_address):
    """Manage communication with a single client."""
    print(f"New connection from {client_address}")

    # Add the client to the list of connected clients
    with clients_lock:
        clients.append(sender)

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
                with clients_lock:
                    clients.remove(sender)
                print(f"Connection closed with {client_address}")
                sender.close()
                break
        except Exception as e:
            print(f"Error: {e}")
            with clients_lock:
                if sender in clients:
                    clients.remove(sender)
            sender.close()
            break


while True:
    # Wait for a new client to connect
    _client_socket, client_address = server_socket.accept()

    add_client(_client_socket)
    thread = threading.Thread(target=handle_client,
                              args=(_client_socket, client_address))
    thread.start()

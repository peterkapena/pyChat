from dataclasses import dataclass
import json
from socket import *
import threading
from message import JSON, Message, MessageActions, client
from typing import List

BUFFER_SIZE = 1024
PORT = 12000

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('', PORT))
server_socket.listen(1)

print('The server is ready to receive')


def add_client(sender: socket):
    """Add a new client to the list if it doesn't already exist."""
    with clients_lock:
        if sender in clients:
            return
        clients.append(sender)


def i_am_alive_request_handler(request: Message, sender: socket):
    cls = []
    for c in clients:
        peer = c.getpeername()
        cls.append(client(peer[0], peer[1], request.user_name, True))

    if len(cls) > 1:
        broadcast(cls, sender, MessageActions.I_AM_ALIVE, request)


def broadcast(data, sender: socket, action: MessageActions, request: Message):
    """Send a message to all connected clients except the sender."""

    json_string = json.dumps(data, cls=JSON)

    peer = sender.getpeername()
    message = Message(action=action.value, source=client(
        peer[0], peer[1], request.user_name, True), body=json_string)

    j = json.dumps(message, cls=JSON)
    for c in clients:
        if c.getpeername() != sender.getpeername():
            c.send(j.encode())
    print(j)


actions = {
    1: i_am_alive_request_handler,
}

# Store a list of connected clients
clients: List[socket] = []

# Create a lock to synchronize access to the clients list
clients_lock = threading.Lock()


def handle_client_requests(sender: socket, client_address):
    """Manage communication with a single client."""
    print(f"New connection from {client_address}")

    add_client(sender)

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
            # sender.close()
            break


while True:
    # Wait for a new client to connect
    _client_socket, client_address = server_socket.accept()

    add_client(_client_socket)
    thread = threading.Thread(target=handle_client_requests,
                              args=(_client_socket, client_address))
    thread.start()

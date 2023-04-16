from socket import *
from message import *
import json

serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

action = MessageActions.I_AM_ALIVE.value

# Create a Message object with the action and body attributes
message = Message(action=action, body="")

# Convert the Message object to a JSON string
json_data = json.dumps(message.__dict__)

# Send the JSON string to the server
clientSocket.send(json_data.encode())

# Receive the response from the server
modifiedSentence = clientSocket.recv(1024)
# Print the response
print('From Server: ', modifiedSentence.decode())

while True:
    # sentence = input('Input lowercase sentence:')
    message.body = input('Input lowercase sentence:')
    message.action = MessageActions.SENDING_MESSAGE.value
    # Convert the Message object to a JSON string
    json_data = json.dumps(message.__dict__)

    # Send the JSON string to the server
    # clientSocket.connect((serverName, serverPort))
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))

    clientSocket.send(json_data.encode())

    # Receive the response from the server
    modifiedSentence = clientSocket.recv(1024)
    # Print the response
    print('From Server: ', modifiedSentence.decode())

clientSocket.close()

from datetime import datetime
import tkinter as tk
from tkinter import simpledialog
from threading import *
from socket import *
import time
from chat_log import ChatLog
from message import Message, MessageActions, client
import json
from typing import List


class ChatApp:
    def __init__(self, master):
        # Set up the window
        self.master = master
        self.master.title("Chat App")
        self.master.geometry("800x600")
        self.master.resizable(False, False)
        self.username = ""
        # simpledialog.askstring(
        #     "Username", "Enter your username:")

        if self.username:
            self.master.title(self.username)

        self.users: List[client] = []
        self.set_left_frame()
        self.set_right_frame()
        self.set_chat_log()

        self.connect_to_server()

    def set_right_frame(self):
        self.right_frame = tk.Frame(self.master, bg="#A6BDB9")
        self.right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Set up the label for the current user being chatted to
        self.chatting_with_label = tk.Label(
            self.right_frame, text="Chatting with:", font=("Arial", 14), bg="#A6BDB9")
        self.chatting_with_label.pack(side=tk.TOP, padx=10, pady=10)

        # Set up the input field and send button

        self.send_frame = tk.Frame(self.right_frame, bg="#A6BDB9")
        self.send_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.input_field = tk.Entry(self.send_frame, font=("Arial", 14))
        self.input_field.pack(side=tk.LEFT, padx=10,
                              pady=10, fill=tk.X, expand=True)
        self.input_field.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self.send_frame, text="Send", font=(
            "Arial", 14), command=self.send_message)
        self.send_button.pack(side=tk.LEFT, padx=10, pady=10)

    def set_left_frame(self):
        # Set up the left and right sections
        self.left_frame = tk.Frame(self.master, bg="#1C413A")
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add the label for the online users
        self.online_users_label = tk.Label(
            self.left_frame, text="Online users", font=("Arial", 14), bg="#1C413A", fg="white")
        self.online_users_label.pack(side=tk.TOP, padx=10, pady=10)

        self.online_users_frame = tk.Frame(self.left_frame, bg="#1C413A")
        self.online_users_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add the dummy users
        # self.user1_label = tk.Label(
        #     self.left_frame, text="192.168.0.1 - John Doe", font=("Arial", 12), bg="#1C413A", fg="white")
        # self.user1_label.pack(side=tk.TOP, padx=10, pady=5)

        # self.user2_label = tk.Label(
        #     self.left_frame, text="192.168.0.2 - Jane Smith", font=("Arial", 12), bg="#1C413A", fg="white")
        # self.user2_label.pack(side=tk.TOP, padx=10, pady=5)

        # self.user3_label = tk.Label(
        #     self.left_frame, text="192.168.0.3 - Bob Johnson", font=("Arial", 12), bg="#1C413A", fg="white")
        # self.user3_label.pack(side=tk.TOP, padx=10, pady=5)

    def set_chat_log(self):
        self.chat_log = ChatLog(self.right_frame)
        self.chat_log.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        for i in range(20):
            message = {
                "text": f"Message {i}",
                "sender": "Me" if i % 2 == 0 else "You",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.chat_log.add_message(message)

    def send_message(self, event=None):
        # self.send_i_am_alive_message()
        message = {
            "text": f"Message {1}",
            "sender": "Me" if 1 % 2 == 0 else "You",
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.chat_log.add_message(message)
        message = self.input_field.get()

        if message:
            print(message)  # Replace with your code to send the message

            # Clear the input field
            self.input_field.delete(0, tk.END)

    def connect_to_server(self):
        self.server_address = ('localhost', 12000)
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.server_address)
        self.master.title(
            f"{self.username} - {self.client_socket.getsockname()}")
        self.send_i_am_alive_message()
        Thread(target=self.handle_response).start()

    def send_i_am_alive_message(self):
        action = MessageActions.I_AM_ALIVE.value
        message = Message(action=action)
        json_data = json.dumps(message.__dict__)
        self.client_socket.send(json_data.encode())
        self.master.after(7000, self.send_i_am_alive_message)

    def render_online_user(self):
        for child in self.online_users_frame.winfo_children():
            child.destroy()

        for c in self.users:
            user_label = tk.Label(
                self.online_users_frame, text=f"{c.addr} - {c.port}", font=("Arial", 12), bg="#1C413A", fg="white")
            user_label.pack(side=tk.TOP, padx=10, pady=5)

    def i_am_alive_response_handler(self, body, source: client):

        clients: List[client] = json.loads(
            body, object_hook=lambda d: client(**d))

        print(source)
        for c in clients:
            # if the client equals the source client or it is already in the list of users, skip it
            if (self.client_socket.getsockname()[0] == c.addr and self.client_socket.getsockname()[1] == c.port) or c in self.users:
                continue
            self.users.append(c)

        if len(clients) != len(self.users):
            self.render_online_user()

    response_actions = {
        1: i_am_alive_response_handler,
    }

    def handle_response(self):
        while True:
            try:
                response = self.client_socket.recv(1024).decode()
                json_data = json.loads(response)
                response = Message(**json_data)
                if response:
                    self.response_actions.get(
                        response.action)(self, response.body, client(**response.source))
                else:
                    3

            except Exception as e:
                # If there's an error, assume the connection has been lost and close the client socket
                print(f"Error: {e}")


root = tk.Tk()
app = ChatApp(root)
root.mainloop()

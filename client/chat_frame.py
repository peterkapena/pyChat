import tkinter as tk
from datetime import datetime
import tkinter as tk
from tkinter import StringVar
from threading import *
from socket import *
from chat_log import ChatLog
from message_store import MessageStorage
from message import DEFAULT_DATE_TIME_FORMAT, JSON, ME, NOT_ME,  Message, MessageActions, chat_message, client
import json
from typing import List

server = "localhost"
# "102.37.221.168"
# "localhost"


class ChatFrame(tk.Frame):
    def __init__(self, master, username):
        super().__init__(master)
        self.username = username
        self.storage = MessageStorage()
        self.current_chat_user = None

        self.create_widgets()

        if self.username:
            self.master.title(self.username)

        self.users: List[client] = []
        self.set_left_frame()
        self.set_right_frame()
        self.online_users: List[client] = []

        self.connect_to_server()

    def create_widgets(self):
        self.configure(bg="#1C413A")
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def logout(self):
        self.master.show_login_page()

    def set_right_frame(self):
        self.right_frame = tk.Frame(self.master, bg="#A6BDB9")
        self.right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.chatting_with_str = StringVar()
        self.chatting_with_label = tk.Label(
            self.right_frame, textvariable=self.chatting_with_str, font=("Arial", 14), bg="#A6BDB9")
        self.chatting_with_label.pack(side=tk.TOP, padx=10, pady=10)

        self.chat_log = ChatLog(self.right_frame)
        self.chat_log.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.chat_log.pack_forget()

        # Set up the input field and send button
        self.send_frame = tk.Frame(self.right_frame, bg="#A6BDB9")
        self.send_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.send_frame.pack_forget()

        self.input_field = tk.Entry(self.send_frame, font=("Arial", 14))
        self.input_field.pack(side=tk.LEFT,
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

    def send_message(self, _=None):
        addr = self.client_socket.getsockname()[0]
        port = self.client_socket.getsockname()[1]
        un = self.username
        u = self.current_chat_user
        sender = client(addr, port, un, True)
        t = self.input_field.get()
        if t:
            when = datetime.utcnow().strftime(DEFAULT_DATE_TIME_FORMAT)

            chat: chat_message = chat_message(t, sender, u, when, ME)

            json_string = json.dumps(chat, cls=JSON)
            action = MessageActions.SENDING_MESSAGE.value
            message = Message(action, sender, json_string, un, u)
            json_data = json.dumps(message, cls=JSON)
            self.client_socket.send(json_data.encode())

            self.chat_log.add_message(chat)
            self.storage.add_message(chat.dest, chat)
            self.input_field.delete(0, tk.END)

    def connect_to_server(self):
        self.server_address = (server, 12000)
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.server_address)
        self.master.title(
            f"{self.username} / {self.client_socket.getsockname()}")
        self.send_i_am_alive_message()
        Thread(target=self.handle_response).start()

    def send_i_am_alive_message(self):
        action = MessageActions.I_AM_ALIVE.value
        message = Message(action=action, user_name=self.username)
        json_data = json.dumps(message.__dict__)
        self.client_socket.send(json_data.encode())
        self.master.after(3000, self.send_i_am_alive_message)

    def set_current_chat_user(self, user: client):
        self.current_chat_user = user
        self.chatting_with_str.set(
            f"Chatting with: {user.addr} - {user.port} - {user.user_name}")
        self.chat_log.pack()
        self.send_frame.pack()
        self.chat_log.clear_chat_log()
        messages = self.storage.get_messages(user)
        print(messages)
        self.chat_log.load_messages(messages)

    def i_am_alive_response_handler(self, _: str, source: client):
        if not source in self.online_users:
            self.online_users.append(source)
            user_label = tk.Button(
                self.online_users_frame, text=f"{source.addr} - {source.port} - {source.user_name}", font=("Arial", 12), bg="#05231e", fg="white")
            user_label.pack(side=tk.TOP, padx=10, pady=10,)
            user_label.bind(
                "<Button-1>", lambda _: self.set_current_chat_user(source))

    def incoming_chat_handler(self, body: str, _: client):
        data_dict = json.loads(body)
        chat_msg = chat_message(
            text=data_dict['text'],
            sender=client(**data_dict['sender']),
            dest=client(**data_dict['dest']),
            when=data_dict['when'],
            _from=NOT_ME
        )

        if not self.current_chat_user:
            self.set_current_chat_user(chat_msg.sender)
            self.chat_log.add_message(chat_msg)
        elif self.current_chat_user == chat_msg.sender:
            self.chat_log.add_message(chat_msg)

        self.storage.add_message(chat_msg.sender, chat_msg)

    response_actions = {
        1: i_am_alive_response_handler,
        2: incoming_chat_handler,
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

import tkinter as tk
from tkinter import StringVar, simpledialog
from threading import *
from socket import *
import time
from message import Message, MessageActions
import json


class ChatApp:
    def __init__(self, master):
        # Set up the window
        self.master = master
        self.master.title("Chat App")
        self.master.geometry("800x600")
        self.master.resizable(False, False)

        # Ask for the username and set the window title
        self.username = StringVar()

        self.username.set(simpledialog.askstring(
            "Username", "Enter your username:"))

        if self.username:
            self.master.title(self.username.get())

        # Set up the left and right sections
        self.left_frame = tk.Frame(self.master, bg="#1C413A")
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.right_frame = tk.Frame(self.master, bg="#A6BDB9")
        self.right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Set up the label for the current user being chatted to
        self.chatting_with_label = tk.Label(
            self.right_frame, text="Chatting with:", font=("Arial", 14), bg="#A6BDB9")
        self.chatting_with_label.pack(side=tk.TOP, padx=10, pady=10)

        # Set up the input field and send button
        self.input_field = tk.Entry(self.right_frame, font=("Arial", 14))
        self.input_field.pack(side=tk.LEFT, padx=10,
                              pady=10, fill=tk.BOTH, expand=True)
        self.input_field.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self.right_frame, text="Send", font=(
            "Arial", 14), command=self.send_message)
        self.send_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.connect_to_server()

    def send_message(self, event=None):
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
            f"{self.username.get()} - {self.client_socket.getsockname()}")
        self.send_i_am_alive_message()
        Thread(target=self.receive_messages).start()

    def send_i_am_alive_message(self):
        action = MessageActions.I_AM_ALIVE.value
        message = Message(action=action, body="")
        json_data = json.dumps(message.__dict__)
        self.client_socket.send(json_data.encode())
        self.master.after(5000, self.send_i_am_alive_message)

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                print(message)
                # self.chat_log.config(state=tk.NORMAL)
                # self.chat_log.insert(tk.END, message + "\n")
                # self.chat_log.config(state=tk.DISABLED)
                # self.chat_log.see(tk.END)
            except:
                # If there's an error, assume the connection has been lost and close the client socket
                self.client_socket.close()


root = tk.Tk()
app = ChatApp(root)
root.mainloop()

import tkinter as tk
from tkinter import messagebox


class LoginPage(tk.Frame):
    def __init__(self, master, on_login_success):
        super().__init__(master)
        self.on_login_success = on_login_success
        self.create_widgets()

    def create_widgets(self):
        self.configure(bg="#1C413A")
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add the label for the online users
        # self.online_users_label = tk.Label(
        #     self.left_frame, text="Online users", font=("Arial", 14), bg="#1C413A", fg="white")
        # self.online_users_label.pack(side=tk.TOP, padx=10, pady=10)

        # self.online_users_frame = tk.Frame(self.left_frame, bg="#1C413A")
        # self.online_users_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.online_users_label = tk.Label(
            self, text="Welcome!", font=("Arial", 16), bg="#1C413A", fg="white")
        self.online_users_label.pack(pady=40)

        self.online_users_label = tk.Label(
            self, text="Sign in", font=("Arial", 25), bg="#1C413A", fg="white")
        self.online_users_label.pack(pady=20)

        self.online_users_label = tk.Label(
            self, text="Username", font=("Arial", 14), bg="#1C413A", fg="white")
        self.online_users_label.pack(pady=10)

        self.username_entry = tk.Entry(self, font=("Arial", 14))
        self.username_entry.pack(pady=10)
        self.username_entry.bind("<Return>", lambda _, self=self: self.login())

        self.online_users_label = tk.Label(
            self, text="Password", font=("Arial", 14), bg="#1C413A", fg="white")
        self.online_users_label.pack(pady=10)

        self.password_entry = tk.Entry(self, font=("Arial", 14))
        self.password_entry.pack()
        self.password_entry.bind("<Return>", lambda _, self=self: self.login())

        self.send_button = tk.Button(self, text="Login", font=(
            "Arial", 14), command=self.login)
        self.send_button.pack(pady=10, )

    def login(self):
        username = self.username_entry.get()
        # password = self.password_entry.get()

        # Here, you can implement  logic to validate the login credentials
        # For this example, let's assume the username and password are valid
        if True:
            self.on_login_success(username)
        # else:
        #     messagebox.showerror(
        #         "Login Failed", "Invalid username or password!")

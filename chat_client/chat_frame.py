import tkinter as tk


class ChatFrame(tk.Frame):
    def __init__(self, master, username):
        super().__init__(master)
        self.username = username
        self.create_widgets()

    def create_widgets(self):
        self.configure(bg="#1C413A")
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.title_label = tk.Label(self, text="Welcome to the Home Page!")
        self.title_label.pack()

        self.username_label = tk.Label(
            self, text="Logged in as: {}".format(self.username))
        self.username_label.pack()

        self.logout_button = tk.Button(
            self, text="Logout", command=self.logout)
        self.logout_button.pack()

    def logout(self):
        self.master.show_login_page()

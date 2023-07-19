import tkinter as tk
from chat_frame import ChatFrame
from login import LoginPage


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Chat App")
        self.geometry("800x600")
        self.configure(bg="#1C413A")
        
        self.login_page = LoginPage(self, self.login_success)
        self.home_page = None

        self.show_login_page()

    def show_login_page(self):
        if self.home_page:
            self.home_page.pack_forget()
        self.login_page.pack()

    def show_home_page(self, username):
        self.login_page.pack_forget()
        self.home_page = ChatFrame(self, username)

    def login_success(self, username):
        self.show_home_page(username)


if __name__ == "__main__":
    app = Application()
    app.mainloop()

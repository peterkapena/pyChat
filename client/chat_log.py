import tkinter as tk
from datetime import datetime

from message import ME, chat_message


class ChatLog(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # create a scrollbar and canvas for the message frame
        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas = tk.Canvas(
            self, bg="white", highlightthickness=0, height=500)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.message_frame = tk.Frame(self.canvas)
        self.canvas_frame = self.canvas.create_window(
            (0, 0), window=self.message_frame, anchor="nw")

        # configure the scrollbar to scroll the canvas
        scrollbar.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=scrollbar.set)

        # bind mouse wheel events to scroll the canvas
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))

        self.canvas.bind("<MouseWheel>", lambda e: self.canvas.yview_scroll(
            int(-1 * (e.delta / 120)), "units"))
        self.bind("<MouseWheel>", lambda e: self.canvas.yview_scroll(
            int(-1 * (e.delta / 120)), "units"))
        master.bind("<MouseWheel>", lambda e: self.canvas.yview_scroll(
            int(-1 * (e.delta / 120)), "units"))

        # resize the canvas when the parent container is resized
        self.bind("<Configure>", self.resize_canvas)

    def resize_canvas(self, event):
        self.canvas.itemconfigure(self.canvas_frame, width=event.width-10)
        self.canvas.configure(
            scrollregion=self.canvas.bbox("all"), width=event.width)

    def add_message(self, message: chat_message):
        bg_color = "lightblue" if message._from == ME else "white"
        sender_or_dest = "To: " + message.dest.user_name if message._from == ME else "From: " + \
            message.sender.user_name

        message_frame = tk.Frame(self.message_frame, bg=bg_color)

        text_label = tk.Label(message_frame, text=message.text, font=(
            "Arial", 10), wraplength=300, justify="left", fg="black", bg=bg_color)
        time_label = tk.Label(message_frame, text=message.when, font=(
            "Arial", 8), fg="gray", bg=bg_color)
        sender_or_dest_label = tk.Label(message_frame, text=sender_or_dest, font=(
            "Arial", 8, "italic"), fg="gray", bg=bg_color)

        message_frame.grid_columnconfigure(0, weight=1)
        sticky = "e" if message._from == ME else "w"

        text_label.grid(row=0,  sticky=sticky)
        time_label.grid(row=2,  sticky=sticky)
        sender_or_dest_label.grid(row=3,  sticky=sticky)

        message_frame.bind("<MouseWheel>", lambda e: self.canvas.yview_scroll(
            int(-1 * (e.delta / 120)), "units"))

        message_frame.pack(fill=tk.X, padx=5, pady=10)
        message_frame.update_idletasks()

        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.auto_scroll()

    def auto_scroll(self):
        self.canvas.yview_moveto(1)
        tk.Frame(self.message_frame,)
        tk.Frame(self.message_frame,)

    def load_messages(self, messages):
        for message in messages:
            self.add_message(message)

    def clear_chat_log(self):
        """Clears the chat log by removing all the message_frame widgets from self.message_frame."""

        for message_frame in self.message_frame.winfo_children():
            message_frame.destroy()

        self.canvas.config(scrollregion=self.canvas.bbox("all"))

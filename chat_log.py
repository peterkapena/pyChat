import tkinter as tk
from datetime import datetime


class ChatLog(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # create a scrollbar and canvas for the message frame
        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas = tk.Canvas(
            self, bg="white", width=self.winfo_reqwidth(), highlightthickness=0)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.message_frame = tk.Frame(self.canvas)
        self.canvas.create_window(
            (0, 0), window=self.message_frame, anchor="nw", width=573)

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
        self.bind("<Configure>", lambda e: self.canvas.config(width=e.width))

    def add_message(self, message):
        bg_color = "lightblue" if message["sender"] == "Me" else "white"

        message_frame = tk.Frame(self.message_frame, bg=bg_color)
        sender_label = tk.Label(message_frame, text=message["sender"], font=(
            "Arial", 8, "bold"), fg="gray", bg=bg_color)
        text_label = tk.Label(message_frame, text=message["text"], font=(
            "Arial", 10), wraplength=300, justify="left", fg="black", bg=bg_color)
        time_label = tk.Label(message_frame, text=message["time"], font=(
            "Arial", 8), fg="gray", bg=bg_color)

        if message["sender"] == "Me":
            message_frame.grid_columnconfigure(0, weight=1)
            text_label.grid(row=0, column=0, padx=(
                0, 5), pady=(5, 0), sticky="e")
            sender_label.grid(row=1, column=0, padx=(0, 5),
                              pady=(0, 5), sticky="e")
            time_label.grid(row=2, column=0, padx=(
                0, 5), pady=(0, 5), sticky="e")
        else:
            message_frame.grid_columnconfigure(0, weight=1)
            text_label.grid(row=0, column=0, padx=(
                5, 0), pady=(5, 0), sticky="w")
            sender_label.grid(row=1, column=0, padx=(5, 0),
                              pady=(0, 5), sticky="w")
            time_label.grid(row=2, column=0, padx=(
                5, 0), pady=(0, 5), sticky="w")

        message_frame.bind("<MouseWheel>", lambda e: self.canvas.yview_scroll(
            int(-1 * (e.delta / 120)), "units"))

        message_frame.pack(fill=tk.X, padx=5, pady=5)
        message_frame.update_idletasks()

        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def load_messages(self, messages):
        for message in messages:
            self.add_message(message)

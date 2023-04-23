import tkinter as tk
from datetime import datetime

from chat_log import ChatLog

root = tk.Tk()
root.geometry("400x400")

chat_log = ChatLog(root)
chat_log.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# add sample messages
chat_log.messages = []
for i in range(20):
    message = {
        "text": f"Message {i}",
        "sender": "Me" if i % 2 == 0 else "You",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    chat_log.messages.append(message)
    chat_log.add_message(message)

root.mainloop()

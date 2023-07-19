from message import chat_message, client


class MessageStorage:
    def __init__(self):
        self.messages = {}

    def add_message(self, user: client, message: chat_message):
        user_key = str(user)
        if user_key not in self.messages:
            self.messages[user_key] = []

        self.messages[user_key].append(message)

    def get_messages(self, user: client):
        user_key = str(user)
        if user_key in self.messages:
            return self.messages[user_key]
        else:
            return []

    def clear_messages(self, user: client = None):
        if user is None:
            self.messages.clear()
        else:
            user_key = str(user)
            if user_key in self.messages:
                del self.messages[user_key]

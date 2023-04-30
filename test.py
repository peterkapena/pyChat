import json
from dataclasses import dataclass


@dataclass
class client:
    addr: str
    port: int
    user_name: str
    isonLine: bool


@dataclass
class chat_message:
    text: str
    sender: client
    dest: client
    when: str
    _from: int


json_str = '{ "text": "aa", "sender": { "addr": "127.0.0.1", "port": 63904, "user_name": "aa", "isonLine": true }, "dest": { "addr": "127.0.0.1", "port": 63904, "user_name": "aa", "isonLine": true }, "when": "2023-04-30 06:29:52", "_from": 3 }'

data_dict = json.loads(json_str)

chat_msg = chat_message(
    text=data_dict['text'],
    sender=client(**data_dict['sender']),
    dest=client(**data_dict['dest']),
    when=data_dict['when'],
    _from=data_dict['_from']
)

print(chat_msg)

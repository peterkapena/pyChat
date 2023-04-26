from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from socket import *
from typing import List
import json


class MessageActions(Enum):
    I_AM_ALIVE = 1
    SENDING_MESSAGE = 2


@dataclass
class client:
    addr: str
    port: int
    user_name: str
    isonLine: bool = False

    # def __init__(self, addr: str, port: int, user_name: str):
    #     self.addr = addr
    #     self.port = port
    #     self.user_name = user_name


@dataclass
class Message:
    action: int
    source: client = None
    body: str = ""
    user_name: str = ""


# @dataclass
# class I_am_alive:
#     clients: List[client]

# class user:
#     isOnline: bool
#     client: client


class JSON(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, object):
            return obj.__dict__
        return super().default(obj)


NOT_ME = 1
ME = 2


@dataclass
class chat_message:
    text: str
    sender: client
    time: datetime
    _from: int

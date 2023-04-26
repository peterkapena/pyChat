from dataclasses import dataclass
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
    isonLine: bool = False

    def __init__(self, addr: str, port: int):
        self.addr = addr
        self.port = port


@dataclass
class Message:
    action: int
    source: client = None
    body: str = ""


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

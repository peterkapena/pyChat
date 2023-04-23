from dataclasses import dataclass
from enum import Enum
from socket import *
from typing import List
import json


class MessageActions(Enum):
    I_AM_ALIVE = 1
    SENDING_MESSAGE = 2


@dataclass
class Message:
    action: int
    body: str = ""
    addr: str = ""
    port: int = 0


@dataclass
class client:
    addr: str
    port: int


class JSON(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, client):
            return obj.__dict__
        return super().default(obj)

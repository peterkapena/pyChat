from dataclasses import dataclass
from enum import Enum
from socket import *
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


@dataclass
class Message:
    action: int
    source: client = None
    body: str = ""
    user_name: str = ""
    dest: client = None


class JSON(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, object):
            return obj.__dict__
        return super().default(obj)


NOT_ME = 1
ME = 2
UNKNOWN = 3
DEFAULT_DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


@dataclass
class chat_message:
    text: str
    sender: client
    dest: client
    when: str
    _from: int

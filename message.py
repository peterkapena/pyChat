from dataclasses import dataclass
from enum import Enum
from socket import *
from typing import List

class MessageActions(Enum):
    I_AM_ALIVE = 1
    SENDING_MESSAGE = 2


@dataclass
class Message:
    action: int
    body: str

@dataclass
class I_AM_ALIVE_RESPONSE:
    clients: List[socket]    
     


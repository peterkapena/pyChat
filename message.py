from dataclasses import dataclass
from enum import Enum

class MessageActions(Enum):
    I_AM_ALIVE = 1
    SENDING_MESSAGE = 2


@dataclass
class Message:
    action: int
    body: str

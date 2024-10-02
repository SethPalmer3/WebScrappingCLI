

from typing import Any
from .messagetypes import MessageTypes
from .messenger import Messenger


class Message:
    def __init__(self, srcMessenger: Messenger, dstMessenger: Messenger | None, message_type: MessageTypes, message_data: Any) -> None:
        pass

    def send(self) -> None:
        pass

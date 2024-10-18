from typing import Any
from uuid import UUID
from .messagetypes import MessageTypes


class Message:
    def __init__(self, srcMessenger, dstMessenger, message_type: MessageTypes, message_data: Any) -> None:
        self.srcMessenger = srcMessenger
        self.dstMessenger = dstMessenger
        self.message_type = message_type
        self.message_data = message_data

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"<Message {self.message_type} from {self.srcMessenger.__str__()} to {self.dstMessenger.__str__()}>"

    def respond_message(self, mt: MessageTypes, data: Any = None) -> "Message":
        return Message(self.dstMessenger, self.srcMessenger, mt, data)
    
    def forward_message(self, new_messnger: UUID) -> "Message":
        return Message(self.srcMessenger, new_messnger, self.message_type, self.message_data)


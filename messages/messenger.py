from multiprocessing import Pipe
from multiprocessing.connection import Connection
import threading
from typing import Callable

from .message import Message
from .messagetypes import MessageTypes

class MessengerThread:
    pass

class Messenger(threading.Thread):
    def __init__(self, *args: "Messenger") -> None:
        super().__init__()
        self.name = self.__class__.__name__
        self.internal_end, self.external_end = Pipe(duplex=True)
        self.commands: dict[str, Callable[[Message], Message]] = {}
        self.messengers: list["Messenger"] = list(args)
        for m in self.messengers:
            m.start()

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"<Messenger {self.name}>"

    def get_connection(self) -> Connection:
        return self.external_end

    def run(self) -> None:
        while True:
            incoming_message = self.internal_end.recv()
            if not isinstance(incoming_message, Message):
                self.internal_end.send(Message(self, None, MessageTypes.ERROR, "Invalid message type"))
                continue
            incoming_message: Message = incoming_message
            if incoming_message.message_type == MessageTypes.STOP:
                for m in self.messengers:
                    m.get_connection().send(Message(self, m, MessageTypes.STOP, None))
                self.internal_end.send(Message(self, incoming_message.srcMessenger, MessageTypes.STOP, None))
                break
            elif incoming_message.dstMessenger is self and \
                incoming_message.message_type == MessageTypes.COMMAND and \
                incoming_message.message_data["command"] in self.commands:
                self.internal_end.send(self.commands[incoming_message.message_data["command"]](incoming_message))


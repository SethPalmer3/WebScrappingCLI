from multiprocessing import Pipe
from multiprocessing.connection import Connection
import threading
from typing import Callable
from uuid import uuid4, UUID

from .message import Message, MessageTypes

class MessengerThread:
    pass

class Messenger(threading.Thread):
    def __init__(self, commands: dict[str, Callable[[Message], Message]] = {}, *args: "Messenger") -> None:
        threading.Thread.__init__(self)
        self.id = uuid4()
        self.internal_end, self.external_end = Pipe(duplex=True)
        self.commands: dict[str, Callable[[Message], Message]] = commands
        self.messengers: list["Messenger"] = list(args)
        for m in self.messengers:
            m.start()

    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, Messenger):
            return self.id == value.id
        if isinstance(value, UUID):
            return self.id == value
        return False

    def __hash__(self) -> int:
        return hash(id(self))
    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"<Messenger {self.name}({self.id})>"

    def get_connection(self) -> Connection:
        return self.external_end

    def run(self) -> None:
        while True:
            incoming_message = self.internal_end.recv()
            if not isinstance(incoming_message, Message): # Make sure the data is a message
                self.internal_end.send(Message(self, None, MessageTypes.ERROR, "Invalid message type"))
                continue

            incoming_message: Message = incoming_message

            if incoming_message.message_type == MessageTypes.STOP: # Stop this thread and all its messengers
                print("Stopping")
                for m in self.messengers:
                    m.get_connection().send(incoming_message.forward_message(m.id))
                    m.join(timeout=1.0)

                respond = incoming_message.respond_message(MessageTypes.STOPPED)
                self.internal_end.send(respond)
                break
            elif self != incoming_message.dstMessenger: # If this message is for a different messenger
                for m in self.messengers:
                    if m.id == incoming_message.dstMessenger:
                        m.get_connection().send(incoming_message)
                        break

                self.internal_end.send(incoming_message.respond_message(MessageTypes.ERROR, "Invalid message destination"))
            else: # This message is for this messenger
                try:
                    msg = self.commands[incoming_message.message_data["command"]](incoming_message)
                    self.internal_end.send(msg)
                except KeyError:
                    self.internal_end.send(incoming_message.respond_message(MessageTypes.ERROR, {"data": ["Unknown command"]}))


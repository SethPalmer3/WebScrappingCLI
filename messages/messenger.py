from multiprocessing import Pipe
from multiprocessing.connection import Connection
import threading

from .message import Message
from .messagetypes import MessageTypes

class MessengerThread:
    pass

class Messenger:
    def __init__(self) -> None:
        self.name = self.__class__.__name__
        self.internal_end, self.external_end = Pipe(duplex=True)
        self.thread = threading.Thread(target=self._run)

    def get_pipe(self) -> Connection:
        return self.external_end

    def _run(self) -> None:
        while True:
            incoming_message = self.internal_end.recv()
            if not isinstance(incoming_message, Message):
                self.internal_end.send(Message(self, None, MessageTypes.ERROR, "Invalid message type"))
                continue

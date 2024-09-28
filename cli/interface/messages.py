from enum import Enum
from typing import Any

class CLIMessages(Enum):
    DATA = 'data'
    ECHO = 'echo'
    DISPLAY = 'display'
    ERROR = 'error'
    OK = 'ok'
    STOP = 'stop'

class Message:
    def __init__(self, source: "Messenger", destination: "Messenger", message: CLIMessages, message_data: list[Any]) -> None:
        self.srcMessenger = source
        self.destMessenger = destination
        self.message = message
        self.message_data = message_data

class Messenger:
    def __init__(self) -> None:
        self.receive_queue = []
        self.name = "Messenger"

    def receive(self, message: Message) -> None:
        self.receive_queue.append(message)

    def send_to(self, message: Message) -> None:
        message.destMessenger.receive(message)

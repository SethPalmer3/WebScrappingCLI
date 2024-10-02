from enum import Enum
from typing import Any

class CLIMessages(Enum):
    DATA = 'data'
    COMMAND = 'command'
    COMMAND_NOT_FOUND = 'command not found'
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

    def respond_message(self, respond_message_type: CLIMessages, message_data: list[Any] = []) -> "Message":
        return Message(self.destMessenger, self.srcMessenger, respond_message_type, message_data)

    def __repr__(self) -> str:
        return f"Message({self.srcMessenger.name}->{self.destMessenger.name}, message={self.message.name}, message_data={self.message_data})"

class Messenger:
    def __init__(self) -> None:
        self.receive_queue = []
        self.name = "Messenger"

    def __repr__(self) -> str:
        return f"{self.name}({self.receive_queue})"

    def receive(self, message: Message) -> None:
        self.receive_queue.append(message)

    def send_to(self, message: Message) -> None:
        message.destMessenger.receive(message)

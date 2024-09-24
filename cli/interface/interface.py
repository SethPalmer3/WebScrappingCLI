from enum import Enum
# import os
import os
import sys
from typing import Any

LOGGING = False

class HistoryElement:
    def __init__(self, input_str: str, output_str: str | None) -> None:
        self.input_str = input_str
        self.output_str = output_str

    def add_output(self, output_str: str) -> bool:
        if self.output_str is not None:
            self.output_str = output_str
            return True
        else:
            return False

class CLIMessages(Enum):
    DATA = 'Data'
    DISPLAY = 'Display'
    ERROR = 'Error'
    STOP = 'Stop'

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
        if LOGGING:
            sys.stdout.write(f"LOG: {self.name} received message from {message.srcMessenger.name} to {message.destMessenger.name}\n")
        self.receive_queue.append(message)

    def send_to(self, message: Message) -> None:
        if LOGGING:
            sys.stdout.write(f"LOG: sending message from {message.srcMessenger.name} to {message.destMessenger.name}\n")
        message.destMessenger.receive(message)

class Displayer:
    def __init__(self, user_input_marker: str, respond_marker: str) -> None:
        self.history = []
        self.user_input_marker = user_input_marker
        self.respond_marker = respond_marker

    def add_history_element(self, input_str: str, output_str: str | None) -> None:
        self.history.append(HistoryElement(input_str, output_str))

    def display(self):
        os.system('clear')
        for h in self.history:
            if isinstance(h, HistoryElement):
                sys.stdout.write(f"{h.input_str}\n{self.respond_marker}{h.output_str}\n")
            else:
                sys.stdout.write(f"{h.__str__()}\n")
        sys.stdout.write(self.user_input_marker)
        sys.stdout.flush()

    def display_message(self, message: str):
        sys.stdout.flush()
        sys.stdout.write(f"\033[1m{message}\033[0m\n")

class CommandMessenger(Messenger):
    def __init__(self) -> None:
        super().__init__()
        self.name = "CommandMessenger"

    def receive(self, message: Message) -> None:
        if LOGGING:
            sys.stdout.write(f"LOG: {self.name} received message from {message.srcMessenger.name} to {message.destMessenger.name}\n")
        new_message = Message(message.destMessenger, message.srcMessenger, CLIMessages.DISPLAY, message.message_data)
        self.send_to(new_message)

class UserInterfaceMessenger(Messenger):
    def __init__(self, displayer: Displayer, commander: CommandMessenger) -> None:
        super().__init__()
        self.displayer = displayer
        self.commander = commander
        self.name = "UserInterfaceMessenger"

    def listen(self) -> None:
        while True:
            self.displayer.display()
            usr_input = sys.stdin.readline().strip()
            cmnd_message = Message(self, self.commander, CLIMessages.DATA, [usr_input])
            self.send_to(cmnd_message)
            return_message = self.receive_queue.pop(0)
            if return_message.message == CLIMessages.STOP:
                self.displayer.display_message("Shutting down...")
                break
            self.displayer.add_history_element(usr_input, return_message.message_data[0])



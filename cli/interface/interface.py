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
    DATA = 'data'
    ECHO = 'echo'
    DISPLAY = 'display'
    ERROR = 'error'
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

    def add_display_element(self, input_str: str) -> None:
        self.history.append(self.inline_message(input_str))

    def display(self):
        os.system('clear')
        for h in self.history:
            write_string = ""
            if isinstance(h, HistoryElement):
                write_string = f"{h.input_str}\n{self.respond_marker}{h.output_str}"
            else:
                write_string = f"{str(h)}"
            sys.stdout.write(write_string)
        sys.stdout.write(f"\n{self.user_input_marker}")
        sys.stdout.flush()

    def important_message(self, message: str):
        os.system('clear')
        sys.stdout.write(f"\033[1m{message}\033[0m\n")
        sys.stdout.flush()

    def inline_message(self, message: str):
        self.history.append(f"\033[3m{message}\033[0m")

class CommandMessenger(Messenger):
    def __init__(self) -> None:
        super().__init__()
        self.name = "CommandMessenger"
        self.commands = {
            "stop": Message(self, self, CLIMessages.STOP, []),
            "echo": Message(self, self, CLIMessages.ECHO, []),
        }

    def get_command(self, message: Message) -> Message:
        if message.message_data[0] in self.commands.keys():
            new_msg = self.commands[message.message_data[0]]
            new_msg.message_data = message.message_data[1:]
            new_msg.destMessenger = message.srcMessenger
            return new_msg
        else:
            # TODO: Check other command messengers
            err_msg = Message(self, message.srcMessenger, CLIMessages.ERROR, ["Could not find command: " + message.message_data[0]])
            return err_msg 

    def receive(self, message: Message) -> None:
        if LOGGING:
            sys.stdout.write(f"LOG: {self.name} received message from {message.srcMessenger.name} to {message.destMessenger.name}\n")
        if message.message == CLIMessages.DATA:
            new_message = self.get_command(message)
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
            cmnd_message = Message(self, self.commander, CLIMessages.DATA, usr_input.split(" "))
            self.send_to(cmnd_message)
            return_message = self.receive_queue.pop(0)
            if return_message.message == CLIMessages.STOP:
                self.displayer.important_message("Shutting down...")
                break
            elif return_message.message == CLIMessages.DISPLAY:
                self.displayer.add_history_element(usr_input, return_message.message_data[0])
            elif return_message.message == CLIMessages.ECHO:
                self.displayer.add_display_element(" ".join(return_message.message_data))
            elif return_message.message == CLIMessages.ERROR:
                pass



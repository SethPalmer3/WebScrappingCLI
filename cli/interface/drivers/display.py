from ..messages import Message, Messenger, CLIMessages
import os
import sys

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

class Displayer:
    def __init__(self, user_input_marker: str, respond_marker: str) -> None:
        self.history = []
        self.user_input_marker = user_input_marker
        self.respond_marker = respond_marker

    def add_history_element(self, input_str: str, output_str: str | None) -> None:
        self.history.append(HistoryElement(input_str, output_str))

    def add_display_element(self, input_str: str) -> None:
        self.inline_message(input_str)

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

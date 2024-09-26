import os
import sys

from .terminal.displayelement import DisplayElement
from .terminal.displayelements import Terminal, TextElement, StyleElement, Styles, InputElement, Window

class HistoryElement:
    def __init__(self, input_str: str, output_str: str | None) -> None:
        self.input_str = input_str
        self.output_str = output_str

    def __repr__(self) -> str:
        return f"HistoryElement({self.input_str}, {self.output_str})"

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

        self.width = os.get_terminal_size().columns
        self.height = os.get_terminal_size().lines
        self.terminal = Terminal([
            Window([], row=0, col=0, width=self.width, height=self.height - 1, z_order=1), # History log
            Window([
                InputElement(user_input_marker, row=0, col=0, input_row=0, input_col=len(user_input_marker), width=self.width, height=1, z_order=2),
            ], row=self.height, col=0, width=self.width, height=1, z_order=1), # Input prompt
        ])

    def add_history_element(self, input_str: str, output_str: str | None) -> None:
        self.history.append(HistoryElement(input_str, output_str))

    def add_display_element(self, input_str: str) -> None:
        self.inline_message(input_str)

    def display(self):
        history = []
        for i, h in enumerate(self.history):
            write_string = None
            if isinstance(h, DisplayElement):
                h.row = i
                h.z_order = 2 + i
                history.append(h)
            elif isinstance(h, HistoryElement):
                write_string = f"{h.input_str}\n{self.respond_marker}{h.output_str}"
            else:
                write_string = f"{str(h)}"
            if write_string is not None:
                history.append(TextElement(write_string, i, 0, self.terminal.width, 1, z_order=2 + i))
        self.terminal.elements[0].__setattr__('elements', history)
        self.terminal.draw()

    def important_message(self, message: str):
        os.system('clear')
        sys.stdout.write(f"\033[1m{message}\033[0m\n")
        sys.stdout.flush()

    def error_message(self, message: str):
        se = StyleElement(message, 0, 0, self.terminal.width, 1, 3, Styles.RED, Styles.BOLD)
        self.history.append(se)

    def inline_message(self, message: str):
        se = StyleElement(message, 0, 0, self.terminal.width, 1, 3, Styles.ITALIC, Styles.FAINT)
        self.history.append(se)

from typing_extensions import NewType
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

class DisplayElement:
    def __init__(self,  row: int, col: int, width: int, height: int, z_order: int = 0) -> None:
        self.z_order = z_order
        self.row = row
        self.col = col
        self.width = width
        self.height = height

    @staticmethod
    def move_cursor(row: int, col: int) -> None:
        sys.stdout.write(f"\033[{row};{col}H")

    @staticmethod
    def move_cursor_up(amount: int = 1) -> None:
        sys.stdout.write(f"\033[{amount}A")

    @staticmethod
    def move_cursor_down(amount: int = 1) -> None:
        sys.stdout.write(f"\033[{amount}B")

    @staticmethod
    def move_cursor_right(amount: int = 1) -> None:
        sys.stdout.write(f"\033[{amount}C")

    @staticmethod
    def move_cursor_left(amount: int = 1) -> None:
        sys.stdout.write(f"\033[{amount}D")

    @staticmethod
    def reset_mode() -> None:
        sys.stdout.write("\033[0m")

    def draw(self, ref_row: int, ref_col: int) -> None:
        pass

class TextElement(DisplayElement):
    def __init__(self, text: str, row: int, col: int, width: int, height: int, z_order: int) -> None:
        super().__init__(row, col, width, height, z_order)
        self.text = text

    def draw(self, ref_row: int, ref_col: int) -> None:
        new_row = ref_row + self.row
        new_col = ref_col + self.col
        DisplayElement.move_cursor(new_row, new_col)
        for i in range(self.height):
            sys.stdout.write(f"{self.text[i*self.width: (i+1)*self.width]}")
            if i + 1 < self.height:
                # DisplayElement.move_cursor_down()
                sys.stdout.write("\n")

class InputElement(DisplayElement):
    def __init__(self, preamble: str, row: int, col: int, input_row: int, input_col: int, width: int, height: int, z_order: int) -> None:
        super().__init__(row, col, width, height, z_order)
        self.text = preamble
        self.input_row = input_row
        self.input_col = input_col

    def draw(self, ref_row: int, ref_col: int) -> None:
        new_row = ref_row + self.row
        new_col = ref_col + self.col
        DisplayElement.move_cursor(new_row, new_col)
        for i in range(self.height):
            sys.stdout.write(f"{self.text[i*self.width: (i+1)*self.width]}")
            if i + 1 < self.height:
                DisplayElement.move_cursor_down()
                # sys.stdout.write("\n")
        DisplayElement.move_cursor(new_row+self.input_row, new_col+self.input_col)

class Window(DisplayElement):
    def __init__(self, elements: list[DisplayElement], row: int = 0, col: int = 0, width: int = 0, height: int = 0, z_order: int = 0) -> None:
        super().__init__(row, col, width, height, z_order)
        self.elements = elements
        self.elements.sort(key=lambda e: e.z_order)

    def draw(self, ref_row: int, ref_col: int) -> None:
        new_row = ref_row + self.row
        new_col = ref_col + self.col
        for e in self.elements:
            e.draw(new_row, new_col)
        # DisplayElement.move_cursor(new_row+self.height, new_col)

class Terminal(Window):
    def __init__(self, elements: list[DisplayElement]) -> None:
        width = os.get_terminal_size().columns
        height = os.get_terminal_size().lines
        
        super().__init__(elements, row=1, col=1, width=width, height=height, z_order=-1)

    def draw(self, ref_row: int = 1, ref_col: int = 1) -> None:
        os.system('clear')
        super().draw(ref_row, ref_col)
        sys.stdout.flush()

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

    def display(self, skip_history: bool = False):
        if not skip_history:
            history = []
            for i, h in enumerate(self.history):
                write_string = ""
                if isinstance(h, HistoryElement):
                    write_string = f"{h.input_str}\n{self.respond_marker}{h.output_str}"
                else:
                    write_string = f"{str(h)}"
                history.append(TextElement(write_string, i, 0, self.terminal.width, 1, z_order=2 + i))
            self.terminal.elements[0].elements = history
        self.terminal.draw()

    def important_message(self, message: str):
        os.system('clear')
        sys.stdout.write(f"\033[1m{message}\033[0m\n")
        sys.stdout.flush()

    def error_message(self, message: str):
        os.system('clear')
        sys.stdout.write(f"\033[1;91m{message}\033[0m\n")
        sys.stdout.flush()

    def inline_message(self, message: str):
        self.history.append(f"\033[3m{message}\033[0m")

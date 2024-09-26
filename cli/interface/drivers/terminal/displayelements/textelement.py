from ..displayelement import DisplayElement
import sys
from enum import Enum

class Styles(Enum):
    BOLD = "1"
    FAINT = "2"
    ITALIC = "3"
    UNDERLINE = "4"
    BLINK = "5"
    REVERSE = "7"
    HIDDEN = "8"
    STRIKE = "9"
    BLACK = "30"
    RED = "31"
    GREEN = "32"
    YELLOW = "33"
    BLUE = "34"
    MAGENTA = "35"
    CYAN = "36"
    WHITE = "37"
    RESET = "0"

    @staticmethod
    def construct(args) -> str:
        ret_str = "\033["
        for arg in args:
            try:
                ret_str += f"{arg.value};"
            except Exception:
                raise Exception(f"{arg}: {args[0]}")

        ret_str = ret_str[:-1] + "m"
        return ret_str

class StyleElement(DisplayElement):
    def __init__(self, text: str, row: int, col: int, width: int, height: int, z_order: int, *args) -> None:
        super().__init__(row, col, width, height, z_order)
        self.text = text
        self.styles = args

    def __repr__(self) -> str:
        return f"StyleTextElement(text={self.text}, row={self.row}, col={self.col}, width={self.width}, height={self.height}, z={self.z_order})"

    def draw(self, ref_row: int, ref_col: int) -> None:
        new_row = ref_row + self.row
        new_col = ref_col + self.col
        DisplayElement.move_cursor(new_row, new_col)
        for i in range(self.height):
            sys.stdout.write(f"{Styles.construct(self.styles)}{self.text[i*self.width: (i+1)*self.width]}\033[0m")
            if i + 1 < self.height:
                # DisplayElement.move_cursor_down()
                sys.stdout.write("\n")


class TextElement(DisplayElement):
    def __init__(self, text: str, row: int, col: int, width: int, height: int, z_order: int) -> None:
        super().__init__(row, col, width, height, z_order)
        self.text = text

    def __repr__(self) -> str:
        return f"TextElement(text={self.text}, row={self.row}, col={self.col}, width={self.width}, height={self.height}, z={self.z_order})"

    def draw(self, ref_row: int, ref_col: int) -> None:
        new_row = ref_row + self.row
        new_col = ref_col + self.col
        DisplayElement.move_cursor(new_row, new_col)
        for i in range(self.height):
            sys.stdout.write(f"{self.text[i*self.width: (i+1)*self.width]}")
            if i + 1 < self.height:
                # DisplayElement.move_cursor_down()
                sys.stdout.write("\n")

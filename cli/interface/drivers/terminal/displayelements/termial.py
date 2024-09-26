from ..displayelement import DisplayElement
from .window import Window
import os
import sys


class Terminal(Window):
    def __init__(self, elements: list[DisplayElement], row: int = 1, col: int = 1) -> None:
        width = os.get_terminal_size().columns
        height = os.get_terminal_size().lines
        
        super().__init__(elements, row=row, col=col, width=width, height=height, z_order=-1)

    def __repr__(self) -> str:
        return f"Terminal([{[e.__repr__() for e in self.elements]}], row={self.row}, col={self.col}, width={self.width}, height={self.height}, z={self.z_order})"

    def draw(self, ref_row: int = 0, ref_col: int = 0) -> None:
        os.system('clear')
        super().draw(ref_row, ref_col)
        sys.stdout.flush()

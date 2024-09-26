from ..displayelement import DisplayElement
import sys

class InputElement(DisplayElement):
    def __init__(self, preamble: str, row: int, col: int, input_row: int, input_col: int, width: int, height: int, z_order: int) -> None:
        super().__init__(row, col, width, height, z_order)
        self.text = preamble
        self.input_row = input_row
        self.input_col = input_col

    def __repr__(self) -> str:
        return f"InputElement(preamble={self.text}, row={self.row}, col={self.col}, width={self.width}, height={self.height}, z={self.z_order})"

    def draw(self, ref_row: int, ref_col: int) -> None:
        if not self.drawable:
        new_row = ref_row + self.row
        new_col = ref_col + self.col
        DisplayElement.move_cursor(new_row, new_col)
        for i in range(self.height):
            sys.stdout.write(f"{self.text[i*self.width: (i+1)*self.width]}")
            if i + 1 < self.height:
                DisplayElement.move_cursor_down()
                # sys.stdout.write("\n")
        DisplayElement.move_cursor(new_row+self.input_row, new_col+self.input_col)

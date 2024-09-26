import sys

class DisplayElement:
    def __init__(self,  row: int, col: int, width: int, height: int, z_order: int = 0) -> None:
        self.z_order = z_order
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.drawable = True

    def __repr__(self) -> str:
        return f"DisplayElement(row={self.row}, col={self.col}, width={self.width}, height={self.height}, z={self.z_order})"

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

    def display(self, ref_row: int, ref_col: int) -> None:
        if self.drawable:
            self.draw(ref_row, ref_col)

    def draw(self, ref_row: int, ref_col: int) -> None:
        pass

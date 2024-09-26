from ..displayelement import DisplayElement

class Window(DisplayElement):
    def __init__(self, elements: list[DisplayElement], row: int = 0, col: int = 0, width: int = 0, height: int = 0, z_order: int = 0) -> None:
        super().__init__(row, col, width, height, z_order)
        self.elements = elements
        self.elements.sort(key=lambda e: e.z_order)

    def __repr__(self) -> str:
        return f"Window([{[e.__repr__() for e in self.elements]}], row={self.row}, col={self.col}, width={self.width}, height={self.height}, z={self.z_order})"

    def draw(self, ref_row: int, ref_col: int) -> None:
        new_row = ref_row + self.row
        new_col = ref_col + self.col
        for e in self.elements:
            e.display(new_row, new_col)
        # DisplayElement.move_cursor(new_row+self.height, new_col)

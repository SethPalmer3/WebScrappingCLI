import os

class HistoryElement:
    def __init__(self, input_str: str, output_str: str | None, output_indicator: str) -> None:
        self.input_str = input_str
        self.output_str = output_str
        self.output_indicator = output_indicator

    def __str__(self) -> str:
        return f"{self.input_str}\n{self.output_indicator} {self.output_str if self.output_str is not None else ''}"
    

    def add_output(self, output_str: str) -> bool:
        if self.output_str is not None:
            self.output_str = output_str
            return True
        else:
            return False

class CommandHanlder:
    def consume(self, consumable: str, output_delim: str) -> HistoryElement:
        return HistoryElement(consumable, consumable, output_delim)


class CLInterface:
    def __init__(self, command_handler: CommandHanlder,
                 input_indicator: str,
                 output_indicator: str) -> None:
        self.input = None
        self.history: list[HistoryElement] = []
        self.line_indicator = input_indicator
        self.output_indicator = output_indicator
        self.input_handler: CommandHanlder = command_handler

    def loop(self):
        # Clear the terminal
        os.system("clear")
        for h in self.history:
            print(h)

        print(self.line_indicator, end="")
        self.input = input()
        self.history.append(self.input_handler.consume(self.input, self.output_indicator))

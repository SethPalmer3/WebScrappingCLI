import os

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

class InputProcessor:
    def process(self, controller: "CLInterface", consumable: str) -> HistoryElement:
        if consumable == "stop":
            controller.stop()

        return HistoryElement(consumable, consumable)

class CommandHanlder:
    def __init__(self, input_processor: InputProcessor) -> None:
        self.input_processor = input_processor

    def consume(self, interface: "CLInterface", consumable: str) -> HistoryElement:
        processor_output = self.input_processor.process(interface, consumable)
        return processor_output

class DisplayHandler:
    def __init__(self, input_indicator: str, output_indicator: str) -> None:
        self.line_indicator = input_indicator
        self.output_indicator = output_indicator
        self.history: list[HistoryElement] = []
    
    def add_history(self, history_element: HistoryElement) -> None:
        self.history.append(history_element)

    def display(self) -> None:
        os.system("clear")
        for h in self.history:
            print(f"{h.input_str}\n{self.output_indicator}{h.output_str}")

        print(self.line_indicator, end="")

    def stop_message(self) -> None:
        os.system("clear")
        print("Stopping...")

class CLInterface:
    def __init__(self, input_handler: CommandHanlder, output_handler: DisplayHandler) -> None:
        self.input_handler = input_handler
        self.output_handler = output_handler
        self.run_state = False

    def loop(self):
        self.run_state = True
        while self.run_state:
            # Clear the terminal
            self.output_handler.display()
            print(f"Current run state: {self.run_state}")
            self.input = input()
            h_elem = self.input_handler.consume(self, self.input)
            self.output_handler.add_history(h_elem)
    
    def stop(self):
        self.run_state = False
        self.output_handler.stop_message()

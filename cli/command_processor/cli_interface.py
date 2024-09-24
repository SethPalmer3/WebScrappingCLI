from cli.interface.interface import CommandHanlder, HistoryElement

class ScrapperHanlder(CommandHanlder):
    def consume(self, consumable: str, output_delim: str) -> HistoryElement:
        return HistoryElement(f"Command: {consumable}", consumable, output_delim)


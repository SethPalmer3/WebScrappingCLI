from typing import Any

class Command:
    def __init__(self, func: Any, help_text: str) -> None:
        self.func = func
        self.help_text = help_text

    def run(self, *args: Any) -> str:
        return self.func(*args)

class CommandManager:
    def __init__(self, valid_commands: dict[str, Command]) -> None:
        self.commands = valid_commands

    def process_command(self, in_command: str) -> str:
        base, *args = in_command.split(" ")
        return self.commands[base].run(*args)
    

from cli.interface.messengers.commandmessenger import CommandMessenger
from cli.interface.messages import Message

def action_click(message: Message):
    pass

class ScrapeCommander(CommandMessenger):
    def __init__(self, command_managers: list["CommandMessenger"] = []) -> None:
        super().__init__(command_managers)
        self.instructions = []
        self.commands = {
            
        }

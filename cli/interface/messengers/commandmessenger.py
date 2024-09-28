from ..messages import Message, Messenger, CLIMessages
from collections.abc import Callable

class CommandMessenger(Messenger):
    def __init__(self, command_managers: list["CommandMessenger"] = []) -> None:
        super().__init__()
        self.name = "CommandMessenger"
        self.commands: dict[str, Callable[[Message, Messenger], Message]] = {}
        self.command_managers: list["CommandMessenger"] = command_managers

    def get_command(self, message: Message) -> Message:
        if message.message_data[0] in self.commands.keys():
            new_msg = self.commands[message.message_data[0]](message, self)
            if new_msg.destMessenger == self:
                new_msg.destMessenger = message.srcMessenger
                new_msg.srcMessenger = self
            return new_msg
        else:
            for commander in self.command_managers:
                other_msg = commander.get_command(message)
                if other_msg.message != CLIMessages.ERROR:
                    return other_msg
            err_msg = Message(self, message.srcMessenger, CLIMessages.ERROR, ["Could not find command: " + message.message_data[0]])
            return err_msg 

    def receive(self, message: Message) -> None:
        if message.message == CLIMessages.DATA:
            new_message = self.get_command(message)
            self.send_to(new_message)

class DummyCommandMessenger(CommandMessenger):
    @staticmethod
    def dummy_stop(m: Message, _messenger: Messenger) -> Message:
        new_m = Message(m.srcMessenger, m.destMessenger, CLIMessages.STOP, [])
        return new_m

    @staticmethod
    def dummy_echo(m: Message, _messenger: Messenger) -> Message:
        new_m = Message(m.srcMessenger, m.destMessenger, CLIMessages.ECHO, [m.message_data[1:]])
        return new_m

    def __init__(self) -> None:
        super().__init__()
        self.name = "DummyCommandMessenger"
        self.commands = {
            "stop": DummyCommandMessenger.dummy_stop,
            "echo": DummyCommandMessenger.dummy_echo
        }

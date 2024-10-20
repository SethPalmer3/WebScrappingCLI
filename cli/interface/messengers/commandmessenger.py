from ..messages import Message, Messenger, CLIMessages
from collections.abc import Callable

class CommandMessenger(Messenger):
    def __init__(self, command_managers: list["CommandMessenger"] = []) -> None:
        super().__init__()
        self.name = self.__class__.__name__
        self.commands: dict[str, Callable[[Message], Message]] = {
            "stop": self.stop
        }
        self.command_managers: list["CommandMessenger"] = command_managers

    def get_command(self, message: Message) -> Message:
        if message.message_data[0] in self.commands.keys():
            new_msg = self.commands[message.message_data[0]](message)
            if new_msg.destMessenger == self or new_msg.srcMessenger == message.destMessenger:
                new_msg.destMessenger = message.srcMessenger
                new_msg.srcMessenger = self
            return new_msg
        else:
            for commander in self.command_managers:
                other_msg = commander.get_command(message.new_receiver(commander))
                if other_msg.message != CLIMessages.COMMAND_NOT_FOUND:
                    return other_msg
            err_msg = Message(self, message.srcMessenger, CLIMessages.COMMAND_NOT_FOUND, ["Could not find command: " + message.message_data[0]])
            return err_msg 

    def receive(self, message: Message) -> None:
        if message.message == CLIMessages.DATA:
            new_message = self.get_command(message)
            self.send_to(new_message)

    def stop(self, message: Message) -> Message:
        for commander in self.command_managers:
            commander.stop(message)
        return message.respond_message(CLIMessages.STOPPED)

class DummyCommandMessenger(CommandMessenger):
    @staticmethod
    def dummy_stop(m: Message) -> Message:
        new_m = Message(m.destMessenger, m.srcMessenger, CLIMessages.STOP, [])
        return new_m

    @staticmethod
    def dummy_echo(m: Message) -> Message:
        new_m = Message(m.destMessenger, m.srcMessenger, CLIMessages.ECHO, m.message_data[1:])
        return new_m

    def __init__(self) -> None:
        super().__init__()
        self.name = "DummyCommandMessenger"
        self.commands = {
            "stop": DummyCommandMessenger.dummy_stop,
            "echo": DummyCommandMessenger.dummy_echo
        }

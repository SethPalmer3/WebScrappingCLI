from ..messages import Message, Messenger, CLIMessages

class CommandMessenger(Messenger):
    def __init__(self) -> None:
        super().__init__()
        self.name = "CommandMessenger"
        self.commands = {
            "stop": Message(self, self, CLIMessages.STOP, []),
            "echo": Message(self, self, CLIMessages.ECHO, []),
        }

    def get_command(self, message: Message) -> Message:
        if message.message_data[0] in self.commands.keys():
            new_msg = self.commands[message.message_data[0]]
            new_msg.message_data = message.message_data[1:]
            new_msg.destMessenger = message.srcMessenger
            return new_msg
        else:
            # TODO: Check other command messengers
            err_msg = Message(self, message.srcMessenger, CLIMessages.ERROR, ["Could not find command: " + message.message_data[0]])
            return err_msg 

    def receive(self, message: Message) -> None:
        if message.message == CLIMessages.DATA:
            new_message = self.get_command(message)
            self.send_to(new_message)

import sys
from ..messages import Message, Messenger, CLIMessages
from .commandmessenger import CommandMessenger
from ..drivers.display import Displayer

class UserInterfaceMessenger(Messenger):
    def __init__(self, displayer: Displayer, commander: CommandMessenger) -> None:
        super().__init__()
        self.displayer = displayer
        self.commander = commander
        self.name = "UserInterfaceMessenger"

    def listen(self) -> None:
        while True:
            self.displayer.display()
            usr_input = sys.stdin.readline().strip()
            cmnd_message = Message(self, self.commander, CLIMessages.DATA, usr_input.split(" "))
            self.send_to(cmnd_message)
            return_message = self.receive_queue.pop(0)
            if return_message.message == CLIMessages.STOP:
                self.displayer.important_message("Shutting down...")
                break
            elif return_message.message == CLIMessages.DISPLAY:
                self.displayer.add_history_element(usr_input, return_message.message_data[0])
            elif return_message.message == CLIMessages.ECHO:
                self.displayer.add_display_element(" ".join(return_message.message_data))
            elif return_message.message == CLIMessages.ERROR:
                pass

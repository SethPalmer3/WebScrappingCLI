from cli.interface.messengers.commandmessenger import CommandMessenger
from cli.interface.messages import CLIMessages, Message, Messenger

from ..webactions.interactingactions.clickaction import ClickAction

class ScrapeCommander(CommandMessenger):
    @staticmethod
    def action_click(message: Message, receiver: Messenger) -> Message:
        if isinstance(receiver, ScrapeCommander) == False:
            return message.respond_message(CLIMessages.ERROR, ["Not a ScrapeCommander"])

        if len(message.message_data) == 0:
            return message.respond_message(CLIMessages.ERROR, ["No xpath provided"])

        select_frame = None
        xpath = message.message_data[0]
        if len(message.message_data) > 1:
            select_frame = message.message_data[1]

        receiver.__getattribute__('instructions').append(ClickAction(xpath, frame=select_frame))

        return message.respond_message(CLIMessages.OK)

    def __init__(self, command_managers: list["CommandMessenger"] = []) -> None:
        super().__init__(command_managers)
        self.instructions = []
        self.commands = {
            "click": ScrapeCommander.action_click
        }

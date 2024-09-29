from cli.interface.messengers.commandmessenger import CommandMessenger
from cli.interface.messages import CLIMessages, Message, Messenger

from ..webactions.interactingactions import ClickAction, TypingAction

class ScrapeCommander(CommandMessenger):
    @staticmethod
    def action_click(message: Message, receiver: Messenger) -> Message:
        """
        message_data = "command", "xpath", ["frame"]
        """
        if not isinstance(receiver, ScrapeCommander):
            return message.respond_message(CLIMessages.ERROR, ["Cannot Handle ScrapeCommander Commands"])

        if len(message.message_data) == 0:
            return message.respond_message(CLIMessages.ERROR, ["No xpath provided"])

        select_frame = None
        xpath = message.message_data[1]
        if len(message.message_data) > 3:
            select_frame = message.message_data[2]

        receiver.__getattribute__('instructions').append(ClickAction(xpath, frame=select_frame))

        return message.respond_message(CLIMessages.OK)

    @staticmethod
    def action_type(message: Message, receiver: Messenger) -> Message:
        """
        message_data = "command", "xpath", "type data", ["frame"]
        """
        if not isinstance(receiver, ScrapeCommander):
            return message.respond_message(CLIMessages.ERROR, ["Cannot Handle ScrapeCommander Commands"])

        if len(message.message_data) < 3:
            return message.respond_message(CLIMessages.ERROR, ["Not Enough Arguments"])

        select_frame = None
        xpath = message.message_data[1]
        type_data = message.message_data[2]
        if len(message.message_data) > 3:
            select_frame = message.message_data[3]

        receiver.__getattribute__('instructions').append(TypingAction(xpath, type_data, frame=select_frame))

        return message.respond_message(CLIMessages.OK)

    def __init__(self, command_managers: list["CommandMessenger"] = []) -> None:
        super().__init__(command_managers)
        self.instructions = []
        self.commands = {
            "click": ScrapeCommander.action_click
        }

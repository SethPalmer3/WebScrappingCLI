from multiprocessing.connection import Connection, Pipe
from actions.scrappingmanager.scrapper import Scrapper
from cli.interface.messengers.commandmessenger import CommandMessenger
from cli.interface.messages import CLIMessages, Message, Messenger

from ..webactions.interactingactions import ClickAction, TypingAction

import threading

SCRAPPER = 'scrapper'
MANAGER_END = 'manager_end'
ACTION_READY_EVENT = 'action_ready_event'
INSTRUCTIONS = 'instructions'

class ScrapeCommander(CommandMessenger):
    @staticmethod
    def base_action(message: Message, receiver: Messenger, action_class, **kwargs) -> Message:
        if not isinstance(receiver, ScrapeCommander):
            return message.respond_message(CLIMessages.ERROR, ["Cannot Handle ScrapeCommander Commands"])

        if len(message.message_data) == 0:
            return message.respond_message(CLIMessages.ERROR, ["No xpath provided"])

        new_action = action_class(kwargs)
        if receiver.__getattribute__(SCRAPPER) is not None:
            mang_conn: Connection = receiver.__getattribute__(MANAGER_END)
            mang_conn.send(new_action)
            action_event: threading.Event = receiver.__getattribute__(ACTION_READY_EVENT)
            action_event.set()
            mang_conn.recv()
        receiver.__getattribute__('instructions').append(new_action)

        return message.respond_message(CLIMessages.OK)

    @staticmethod
    def action_click(message: Message, receiver: Messenger) -> Message:
        """
        message_data = "command", "xpath", ["frame"]
        """
        return ScrapeCommander.base_action(message, receiver, ClickAction, xpath=message.message_data[1], frame=None if len( message.message_data ) < 3 else message.message_data[2])

    @staticmethod
    def action_type(message: Message, receiver: Messenger) -> Message:
        """
        message_data = "command", "xpath", "type data", ["frame"]
        """
        return ScrapeCommander.base_action(message, receiver, TypingAction,
                                           xpath=None if len(message.message_data) == 0 else message.message_data[1],
                                           text="" if len(message.message_data) < 3 else message.message_data[2],
                                           frame=None if len(message.message_data) < 4 else message.message_data[3])

    @staticmethod
    def action_url(message: Message, receiver: Messenger) -> Message:
        if not isinstance(receiver, ScrapeCommander):
            return message.respond_message(CLIMessages.ERROR, ["Cannot Handle ScrapeCommander Commands"])

        if len(message.message_data) == 0:
            return message.respond_message(CLIMessages.ERROR, ["No url provided"])

        url = message.message_data[1]
        # receiver.__setattr__('scrapper', Scrapper(url, receiver.__getattribute__('instructions')))
        action_ready_event = threading.Event()
        (manager_end, scrapper_end) = Pipe()
        receiver.__setattr__('scrapper', threading.Thread(target=Scrapper(scrapper_end, action_ready_event, url, *receiver.__getattribute__('instructions')).start))
        receiver.__setattr__('action_ready_event', action_ready_event)
        receiver.__setattr__('manager_end', manager_end)

        return message.respond_message(CLIMessages.OK)

    @staticmethod
    def action_start(message: Message, receiver: Messenger) -> Message:
        if not isinstance(receiver, ScrapeCommander):
            return message.respond_message(CLIMessages.ERROR, ["Cannot Handle ScrapeCommander Commands"])

        if (driver := receiver.__getattribute__('scrapper')) is not None:
            driver.scrape()
            return message.respond_message(CLIMessages.OK)
        return message.respond_message(CLIMessages.ERROR, ["No URL set for this scrape job"])

    def __init__(self, command_managers: list["CommandMessenger"] = []) -> None:
        super().__init__(command_managers)
        self.instructions = []
        self.scrapper = None
        self.commands = {
            "click": ScrapeCommander.action_click,
            "type" : ScrapeCommander.action_type,
            "url" : ScrapeCommander.action_url,
            "start" : ScrapeCommander.action_start
        }

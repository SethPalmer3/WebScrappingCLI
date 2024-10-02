from multiprocessing.connection import Connection, Pipe
from actions.scrappingmanager.scrapper import Scrapper
from cli.interface.messengers.commandmessenger import CommandMessenger
from cli.interface.messages import CLIMessages, Message, Messenger

from ..webactions.interactingactions import ClickAction, TypingAction
from ..webactions.noninteractingactions import FindElementsAction

import threading

SCRAPPER = 'scrapper'
MANAGER_END = 'manager_end'
ACTION_READY_EVENT = 'action_ready_event'
INSTRUCTIONS = 'instructions'

class ScrapeCommander(CommandMessenger):
    @staticmethod
    def base_action(message: Message, action_class, **kwargs) -> Message:
        receiver = message.destMessenger
        if not isinstance(receiver, ScrapeCommander):
            return message.respond_message(CLIMessages.ERROR, ["Cannot Handle ScrapeCommander Commands"])

        if len(message.message_data) == 0:
            return message.respond_message(CLIMessages.ERROR, ["No xpath provided"])

        new_action = action_class(**kwargs)
        return_data = None
        if receiver.__getattribute__(SCRAPPER) is not None:
            mang_conn: Connection = receiver.__getattribute__(MANAGER_END)
            mang_conn.send(new_action)
            action_event: threading.Event = receiver.__getattribute__(ACTION_READY_EVENT)
            action_event.set()
            return_data = mang_conn.recv()
        receiver.__getattribute__(INSTRUCTIONS).append(new_action)

        if return_data is None:
            return message.respond_message(CLIMessages.OK)
        elif isinstance(return_data[1], list):
            return message.respond_message(return_data[0], return_data[1])
        else:
            return message.respond_message(return_data[0], [return_data[1]])


    @staticmethod
    def action_find(message: Message) -> Message:
        """
        message_data = "command", "xpath", ["frame"]
        """
        return ScrapeCommander.base_action(
            message, 
            FindElementsAction, 
            search_term=message.message_data[1], 
            frame=None if len(message.message_data) < 3 else message.message_data[2]
        )

    @staticmethod
    def action_click(message: Message) -> Message:
        """
        message_data = "command", "xpath", ["frame"]
        """
        return ScrapeCommander.base_action(message, ClickAction, xpath=message.message_data[1], frame=None if len( message.message_data ) < 3 else message.message_data[2])

    @staticmethod
    def action_type(message: Message) -> Message:
        """
        message_data = "command", "xpath", "type data", ["frame"]
        """
        return ScrapeCommander.base_action(message, TypingAction,
                                           xpath=None if len(message.message_data) == 0 else message.message_data[1],
                                           text="" if len(message.message_data) < 3 else message.message_data[2],
                                           frame=None if len(message.message_data) < 4 else message.message_data[3])

    @staticmethod
    def action_url(message: Message) -> Message:
        """
        A function that will spin up a web driver thread to run concurrenly with main execution
        """
        receiver = message.destMessenger
        if not isinstance(receiver, ScrapeCommander):
            return message.respond_message(CLIMessages.ERROR, ["Cannot Handle ScrapeCommander Commands"])

        if len(message.message_data) == 0:
            return message.respond_message(CLIMessages.ERROR, ["No url provided"])

        url = message.message_data[1]
        action_ready_event = threading.Event()
        (manager_end, scrapper_end) = Pipe()
        receiver.__setattr__(SCRAPPER, threading.Thread(target=Scrapper(scrapper_end, action_ready_event, url, *receiver.__getattribute__(INSTRUCTIONS)).start))
        receiver.__getattribute__(SCRAPPER).start()
        receiver.__setattr__(ACTION_READY_EVENT, action_ready_event)
        receiver.__setattr__(MANAGER_END, manager_end)

        return message.respond_message(CLIMessages.OK)

    @staticmethod
    def action_start(message: Message) -> Message:
        receiver = message.destMessenger
        if not isinstance(receiver, ScrapeCommander):
            return message.respond_message(CLIMessages.ERROR, ["Cannot Handle ScrapeCommander Commands"])

        if (driver := receiver.__getattribute__(SCRAPPER)) is not None:
            driver.scrape()
            return message.respond_message(CLIMessages.OK)
        return message.respond_message(CLIMessages.ERROR, ["No URL set for this scrape job"])

    def __init__(self, command_managers: list["CommandMessenger"] = []) -> None:
        super().__init__(command_managers)
        self.name = "ScrapeCommander"
        self.instructions = []
        self.scrapper = None
        self.commands = {
            "click": ScrapeCommander.action_click,
            "type" : ScrapeCommander.action_type,
            "url" : ScrapeCommander.action_url,
            "start" : ScrapeCommander.action_start,
            "find": ScrapeCommander.action_find
        }

    def stop(self, message: Message) -> Message:
        if self.scrapper is not None:
            self.__getattribute__(ACTION_READY_EVENT).set()
            self.__getattribute__(MANAGER_END).send(CLIMessages.STOP)
        return message.respond_message(CLIMessages.STOPPED)

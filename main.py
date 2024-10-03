# from selenium import webdriver
import argparse
from uuid import uuid4

from messages import Message, MessageTypes, Messenger

# from actions.scrappingmanager.scrapper import Scrapper
# from actions.scrappingmanager.scrapmanager import ScrapeCommander


def main():
    parser = argparse.ArgumentParser(
        prog='Power Usage Collector',
        description='Collects usage from your power usage meter'
    )

    parser.add_argument('--skip-web-scrape', '-s', '--skip', action='store_true', help='Skips web scrape')
    parser.add_argument('--headless', action='store_true', help='Makes scrape headless')
    args = parser.parse_args()

    def test(m: Message) -> Message:
        new_data = m.message_data
        new_data["data"].append("(test)")
        return m.respond_message(MessageTypes.COMMAND_RESULT, new_data)

    mssngr = Messenger(commands={
        "echo": test,
        "stop": lambda m: m.respond_message(MessageTypes.STOP)
    })
    mssngr.start()
    my_uuid = uuid4()
    while True:
        user_input = input(">")
        command = user_input.split(" ")[0]
        data = user_input.split(" ")[1:]
        msg = Message(my_uuid, mssngr.id, MessageTypes.COMMAND, {"command": command, "data": data})
        mssngr.get_connection().send(msg)
        msg = mssngr.get_connection().recv()
        if msg.message_type == MessageTypes.STOP:
            print("Stopping...")
            mssngr.get_connection().send(Message(my_uuid, mssngr.id, MessageTypes.STOPPED, {}))
            mssngr.join(timeout=1.0)
            break
        elif msg.message_type == MessageTypes.COMMAND_RESULT:
            print(" ".join(msg.message_data["data"]))
        elif msg.message_type == MessageTypes.ERROR:
            print(f"\033[1;31m{ " ".join(msg.message_data["data"]) }\033[m")

if __name__ == '__main__':
    main()

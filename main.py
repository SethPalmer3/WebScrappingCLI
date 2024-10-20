# from selenium import webdriver
import argparse
from uuid import uuid4
import dill

from messages import Message, MessageTypes, Messenger
from messages.messagetypes import MessageData

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

    # Scrapper.SKIPWEBSCRAPE = args.skip_web_scrape
    # Scrapper.HEADLESS = args.headless

    mssngr = Messenger()
    mssngr.commands = {
        "echo": lambda x: x.respond_message(MessageTypes.COMMAND_RESULT, {MessageData.RESULT: x.message_data[MessageData.DATA]}),
    }
    mssngr.start()
    conn = mssngr.get_connection()
    while True:
        usr_input = input(">> ")
        mssg = Message(None, mssngr.id, MessageTypes.COMMAND, {
            MessageData.COMMAND: usr_input.split(' ')[0],
            MessageData.DATA: ' '.join(usr_input.split(' ')[1:])
        })
        pckl = dill.dumps(mssg)
        conn.send(pckl)
        return_message: Message = dill.loads(conn.recv())
        print(return_message.message_data)


if __name__ == '__main__':
    main()

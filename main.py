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

    # Scrapper.SKIPWEBSCRAPE = args.skip_web_scrape
    # Scrapper.HEADLESS = args.headless

    mssngr = Messenger()
    mssngr.commands = {
        "echo": lambda x: x.respond_message(MessageTypes.COMMAND_RESULT),
    }
    mssngr.start()
    while True:
        usr_input = input(">> ")
        mssg = Message(None, mssngr, MessageTypes.COMMAND, {
            "command": usr_input.split(' ')[0]
        })
        conn = mssngr.get_connection()
        conn.send(mssg)

if __name__ == '__main__':
    main()

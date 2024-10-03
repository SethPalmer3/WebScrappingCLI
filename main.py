# from selenium import webdriver
import argparse

from .messages import Messenger, MessageTypes, Message

from actions.scrappingmanager.scrapper import Scrapper
from actions.scrappingmanager.scrapmanager import ScrapeCommander


def main():
    parser = argparse.ArgumentParser(
        prog='Power Usage Collector',
        description='Collects usage from your power usage meter'
    )

    parser.add_argument('--skip-web-scrape', '-s', '--skip', action='store_true', help='Skips web scrape')
    parser.add_argument('--headless', action='store_true', help='Makes scrape headless')
    args = parser.parse_args()

    Scrapper.SKIPWEBSCRAPE = args.skip_web_scrape
    Scrapper.HEADLESS = args.headless

    displayer = Displayer(">> ", " -> ")
    commander = CommandMessenger([DummyCommandMessenger(), ScrapeCommander()])
    usr_msngr = UserInterfaceMessenger(displayer, commander)
    usr_msngr.listen()


if __name__ == '__main__':
    main()

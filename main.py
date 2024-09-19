from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import calendar
import time
import os
import argparse

from actions.webactions.interactingactions.clickaction import ClickAction
from actions.webactions.interactingactions.typingaction import TypingAction
from actions.nonwebactions.customactions.customaction import CustomAction
from actions.nonwebactions.nonwebaction import NonWebAction
from actions.action import Action

from constants import *

class UsageAction(NonWebAction):
    def __init__(self, filepath, rate):
        self.filepath = filepath
        self.rate = rate

    def replace_old_file(self):
        if not os.path.exists(self.filepath):
            return

        (base, extension) = os.path.splitext(self.filepath)
        if os.path.exists(base + "(1)" + extension):
            os.remove(self.filepath)
            os.rename(base + "(1)" + extension, self.filepath)


    def preform_action(self, prev_action_output, driver=None):
        print("Calcualting usage")
        self.replace_old_file()

        with open(self.filepath) as f:
            lines = f.readlines()   

        current_day_of_month = datetime.now().day
        total = 0.0
        for line in lines[1:]:
            newline = line.replace('"', '')
            (usage_date, usage, *c) = newline.split(",")
            (year, month, day) = usage_date.split("-")
            current_year = datetime.now().year
            current_month = datetime.now().month
            current_day = datetime.now().day
            if int(year) <= current_year and int(month) == current_month and int(day) <= current_day:
                total += float(usage) * self.rate

        num_days_in_month = calendar.monthrange(current_year, current_month)[1]
        estimated_usage_rate = total / current_day_of_month
        estimated_usage_rate = round(estimated_usage_rate, 2)
        estimated_usage = num_days_in_month * estimated_usage_rate
        print(f"Estimated usage: {estimated_usage}")

        return total

def calculate_usage(filepath, rate):
    print("Calcualting usage")

    with open(filepath) as f:
        lines = f.readlines()   

    current_day_of_month = datetime.now().day
    total = 0.0
    for line in lines[1:]:
        newline = line.replace('"', '')
        (usage_date, usage, *c) = newline.split(",")
        (year, month, day) = usage_date.split("-")
        current_year = datetime.now().year
        current_month = datetime.now().month
        current_day = datetime.now().day
        if int(year) <= current_year and int(month) == current_month and int(day) <= current_day:
            total += float(usage) * rate

    num_days_in_month = calendar.monthrange(current_year, current_month)[1]
    estimated_usage_rate = total / current_day_of_month
    estimated_usage_rate = round(estimated_usage_rate, 2)
    estimated_usage = num_days_in_month * estimated_usage_rate

    print(f"Estimated usage: {estimated_usage}")

    return total

def replace_old_file(filepath):
    if not os.path.exists(filepath):
        return

    (base, extension) = os.path.splitext(filepath)
    if os.path.exists(base + "(1)" + extension):
        os.remove(filepath)
        os.rename(base + "(1)" + extension, filepath)

class UsageScrapper:
    SKIPWEBSCRAPE = False
    HEADLESS = True
    def __init__(self, url, *args):
        self.url = url
        self.actions = list(args)

    def scrape_usage(self):
        print("Starting scrape...")
        pass_value = None
        if UsageScrapper.SKIPWEBSCRAPE:
            for action in self.actions:
                if isinstance(action, NonWebAction):
                    pass_value = action.preform_action(pass_value)
                    if pass_value is not None:
                        print(pass_value)
            return

        options = webdriver.FirefoxOptions()
        if UsageScrapper.HEADLESS:
            options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=options)
        self.driver.get(self.url)
        for action in self.actions:
            if isinstance(action, Action):
                try:
                    pass_value = action.preform_action(pass_value, self.driver)
                    if pass_value is not None:
                        print(pass_value)
                except Exception as e:
                    print(e)
                    self.driver.close()
                    break
            else:
                raise TypeError("Actions must be of type Action")
        self.driver.close()


def main():
    parser = argparse.ArgumentParser(
        prog='Power Usage Collector',
        description='Collects usage from your power usage meter'
    )

    parser.add_argument('--skip-web-scrape', '-s', '--skip', action='store_true', help='Skips web scrape')
    parser.add_argument('--headless', action='store_true', help='Makes scrape headless')
    args = parser.parse_args()

    UsageScrapper.SKIPWEBSCRAPE = args.skip_web_scrape
    UsageScrapper.HEADLESS = args.headless
    
    scrapper = UsageScrapper(URL,
                             TypingAction(SIGNINXPATH, USERNAME, frame=LOGINFRAME),
                             TypingAction(PASSWORDXPATH, PASSWORD, frame=LOGINFRAME),
                             TypingAction(PASSWORDXPATH, Keys.RETURN, frame=LOGINFRAME),
                             ClickAction(USAGEBUTTONXPATH, wait=30),
                             ClickAction(DOWNLOADBUTTONXPATH, wait=30),
                             CustomAction(replace_old_file, filepath=DOWNLOADPATH + f"\\{FILENAME}"),
                             CustomAction(calculate_usage, filepath=DOWNLOADPATH + f"\\{FILENAME}", rate=CURRENT_RATE),
                             # UsageAction(DOWNLOADPATH + f"\\{FILENAME}", CURRENT_RATE)
                             )

    scrapper.scrape_usage()

if __name__ == '__main__':
    main()

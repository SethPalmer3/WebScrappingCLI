import os, calendar
from datetime import datetime
import threading
from typing import Any
from selenium import webdriver
from actions.action import Action
from actions.nonwebactions.nonwebaction import NonWebAction
from cli.interface.messages import CLIMessages

from multiprocessing.connection import Connection

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

class Scrapper:
    SKIPWEBSCRAPE = False
    HEADLESS = True
    def __init__(self, connection: Connection, event: threading.Event, url, *args):
        super().__init__()
        self.url = url
        self.connection = connection
        self.event = event
        self.actions = list(args)
    
    def start(self):
        context = []
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=options)
        self.driver.get(self.url)
        self.prev_data=None
        while True:
            self.event.wait()
            new_action = self.connection.recv()
            if isinstance(new_action, CLIMessages) and new_action == CLIMessages.STOP:
                break
            ret_data = self.step(new_action)
            print(ret_data)
            self.connection.send(ret_data)
            self.event.clear()
        self.driver.close()

    def step(self, action: Action) -> tuple[CLIMessages, Any]:
        if self.driver is None:
            return (CLIMessages.ERROR, "Driver is not set")
        try:
            self.prev_data = action.preform_action(self.prev_data, self.driver)
            if isinstance(self.prev_data, list):
                return (CLIMessages.DATA, self.prev_data)
            return (CLIMessages.OK, self.prev_data)
        except Exception as e:
            return (CLIMessages.ERROR, str(e))

    def scrape(self):
        print("Starting scrape...")
        pass_value = None
        if Scrapper.SKIPWEBSCRAPE:
            for action in self.actions:
                if isinstance(action, NonWebAction):
                    pass_value = action.preform_action(pass_value)
                    if pass_value is not None:
                        print(pass_value)
            return

        options = webdriver.FirefoxOptions()
        if Scrapper.HEADLESS:
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

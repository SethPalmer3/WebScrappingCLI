from ..webaction import WebAction
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class FindElementsAction(WebAction):
    def __init__(self, xpath):
        self.xpath = xpath

    def preform_action(self, prev_action_output, driver):
        return driver.find_element(By.XPATH, prev_action_output)

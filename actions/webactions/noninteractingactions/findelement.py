from ..webaction import WebAction
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


ALL_LOOKUPS = [By.ID, By.XPATH, By.NAME, By.TAG_NAME, By.LINK_TEXT, By.CLASS_NAME, By.CSS_SELECTOR, By.PARTIAL_LINK_TEXT]

class FindElementsAction(WebAction):
    def __init__(self, search_term, frame=None):
        self.search_term = search_term
        self.frame = frame

    def preform_action(self, prev_action_output, driver):
        possible_elements = []
        for lookfor in ALL_LOOKUPS:
            try:
                for e in driver.find_elements(lookfor, self.search_term):
                    if e not in possible_elements:
                        possible_elements.append(f"{e.tag_name}:{e.id}")
            except Exception:
                continue
        return possible_elements

from .interactingaction import InteractingAction

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ClickAction(InteractingAction):
    def __init__(self, xpath, tries=10, wait=10, frame=None):
        self.xpath = xpath
        self.wait = wait
        self.frame = frame
        self.tries = tries
        self.action_message = "Clicking"

    def interact_action(self, driver):
        while self.tries > 0:
            try:
                driver.find_element(By.XPATH, self.xpath).click()
                return
            except Exception as e:
                print(e)
                driver.execute_script("window.scrollBy(0, 100);")
                self.tries -= 1
        
        raise TimeoutError(f"Failed to click <{self.xpath}>")

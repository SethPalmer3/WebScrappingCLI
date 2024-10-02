from typing import Any
from ..webaction import WebAction

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class InteractingAction(WebAction):

    def __init__(self, xpath, wait=10, frame=None):
        self.xpath = xpath
        self.wait = wait
        self.frame = frame
        self.action_message = "Interacting with"

    def interact_action(self, driver):
        pass

    def preform_action(self, prev_action_output, driver) -> Any:
        if self.frame:
            print(f"Switching to frame")
            driver.switch_to.frame(self.frame)
        else:
            driver.switch_to.default_content()

        try:
            print(f"Waiting for <{self.xpath}> to be visible ...")
            WebDriverWait(driver, self.wait).until(
                EC.presence_of_element_located((By.XPATH, self.xpath))
            )
        except Exception as e:
            raise e
        elem = driver.find_element(By.XPATH, self.xpath)

        print(f"Found <{elem.tag_name}>{elem.text}</{elem.tag_name}>")
        print(f"{self.action_message} <{elem.tag_name}>{elem.text}</{elem.tag_name}>")

        self.interact_action(driver)

        if self.frame:
            print(f"Switching back to default content.")
            driver.switch_to.default_content()

        return None

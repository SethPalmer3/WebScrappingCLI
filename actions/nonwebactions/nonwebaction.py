from ..action import Action

class NonWebAction(Action):
    def __init__(self):
        pass

    def preform_action(self, prev_action_output, driver=None) -> any:
        pass

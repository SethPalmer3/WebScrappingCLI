from ..nonwebaction import NonWebAction

class CustomAction(NonWebAction):
    def __init__(self, func, **kwargs):
        self.func = func
        self.params = kwargs

    def preform_action(self, prev_action_output, driver=None) -> any:
        if self.params:
            self.func(**self.params)
        else:
            return self.func(prev_action_output)

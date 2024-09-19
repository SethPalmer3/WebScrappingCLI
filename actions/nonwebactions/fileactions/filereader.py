from .nonwebaction import NonWebAction

class FileReadAction(NonWebAction):
    def __init__(self, path):
        self.path = path

    def preform_action(self, prev_action_output, driver=None):
        with open(self.path, "r") as f:
            return f.read()

from .nonwebaction import NonWebAction

class FileWriteAction(NonWebAction):
    def __init__(self, path, text, replace=False):
        self.path = path
        self.text = text
        self.replace = replace

    def replace_old_file(self):
        if not os.path.exists(self.filepath):
            return

        (base, extension) = os.path.splitext(self.filepath)
        if os.path.exists(base + "(1)" + extension):
            os.remove(self.filepath)
            os.rename(base + "(1)" + extension, self.filepath)

    def preform_action(self, prev_action_output, driver=None):
        with open(self.path, "w") as f:
            return f.write(self.text)

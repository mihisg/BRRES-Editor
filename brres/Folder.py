class Folder:

    def __init__(self, name, *files):
        self.name = name
        self.files = []
        for i in files:
            self.files.append(i)

from utils import *

class Question:
    def __init__(self, lines, file, test_cases):
        self.lines = lines

        self.title = lines[0]
        self.contents = lines[1:]

        self.file = file
        self.test_cases = test_cases

    def __str__(self):
        return "\n".join(self.lines)
from utils import *
from Question import *


class Assignment:
    def __init__(self):
        self.questions, self.total = self.parse(MARKING_SCHEME)

        self.marked_by = MARKED_BY
        self.email = EMAIL

    def __str__(self):
        return f"ASSIGNMENT {ASSIGNMENT_NUM}\n\n" + "\n\n".join([str(q) for q in self.questions])

    def __repr__(self):
        return str(self)

    @staticmethod
    def parse(txt):
        questions = {}

        with open(txt, "r") as f:
            data = f.read()

        total = re.findall(r"Total: \[\/(\d+)\]", data)
        if total:
            total = int(total[0])

        data = data.split("\n\n")

        for q in data:
            name = q.split(":")[0]
            if "Total" in name:
                continue

            num = "".join(re.findall(r'\d+', name))

            filename = f"a{ASSIGNMENT_NUM}_p{num}.py" if num else name
            if filename not in TEST_CASES:
                TEST_CASES[filename] = False

            question = Question(q.split("\n"), filename, TEST_CASES[filename])
            questions[question.file] = question
        return questions, total

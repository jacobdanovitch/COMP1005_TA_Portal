from utils import *
import json
from flask import Markup

class Assignment:
    def __init__(self, marking_scheme):
        with open(marking_scheme, "r") as f:
            self.contents = json.load(f)
            self.q2f = {
                p: (f"a{ASSIGNMENT_NUM}_p{i+1}.py" if "Problem" in p else p)
                for i, p in enumerate(self.contents.keys())
            }

        self.marked_by = MARKED_BY
        self.email = EMAIL

    def question_to_file(self, q):
        return self.q2f[q]

    def __str__(self):
        return f"ASSIGNMENT {ASSIGNMENT_NUM}\n\n" + json.dumps(self.contents, indent=2)

    def __repr__(self):
        return str(self)

    def get_questions(self):
        return [q for q in self.contents if q != "Total"]

    @staticmethod
    def semicolon_sep_to_ul(x):
        spl = re.split("\s*;\s*", x)
        if len(spl) == 1:
            return spl[0]

        return "<ul>"+"".join([Markup(f"<li>{p}</li>") for p in spl])+"</ul>"
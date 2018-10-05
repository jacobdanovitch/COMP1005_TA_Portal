import utils

from pexpect.popen_spawn import PopenSpawn
from glob import glob
from pathlib import Path
import re
from IPython.display import Markdown, clear_output
import time


class Submission:
    def __init__(self, path, assignment):
        self.path = path
        self.files = [Path(p) for p in glob(f"{path}/*.py")]

        self.assignment = assignment
        self.marks = {}

    def print(self):
        name, num = self.parse_name_and_num()
        header = f"## {name}\t{num}"

        files = f"<i>Files:\t\t{[f.name for f in self.files]}</i>"

        utils.printmd(header)
        utils.printmd(files)
        utils.printmd("<hr/>")

    def __repr__(self):
        return str(self)

    def print_solution(self, q, i):
        utils.printmd(f"Running file **{q.file}** ({i+1}/{len(self.files)}) ...\n\n")

        utils.printmd("**Code:**")
        utils.printmd(f"```python\n{self.get_file(q.file)}\n```")

        utils.printmd("<hr/>\n\n")

        utils.printmd("**Output of tests:**")
        outputs = self.run_file(q)
        for o in outputs:
            print(o)

        utils.printmd("<hr/>")

    def grade(self):
        for i, x in enumerate(self.assignment.questions.items()):
            f, q = x

            if ".py" in f:
                self.print_solution(q, i)

            self.assign_marks(q)

            prompt = "Press enter " + "when you are ready to move to the next question." if not (i + 1) == len(
                self.assignment.questions) else "to see the final mark."
            utils.printmd(f"\n<hr/>\n{prompt}")
            input(">>> ")

            clear_output(wait=True)
            time.sleep(1)

        print("Marks:")

    def assign_marks(self, q):
        utils.printmd(f"**Assigning marks for {q.file}.**")
        print("Enter 'q', 'quit', or 'exit' at any time. ...\n\n")
        for part in q.contents:
            utils.printmd(f"**{part}**")

            _in, valid = utils.parse_float(input(">>> "))
            while not valid:
                print("Please input a number.")
                _in, valid = utils.parse_float(input(">>> "))

            self.marks[part] = float(_in)

    def display_final_marks(self):
        tbl = f"# Assignment {utils.ASSIGNMENT_NUM}: {' '.join(self.parse_name_and_num())}\n\n| Mark | Criteria |\n"
        tbl += "| --- | --- |\n"
        for cr, mk in self.marks.items():
            row = f"| {mk} | {cr} |\n"
            tbl += row

        earned = sum(self.marks.values())
        pct = earned/self.assignment.total

        tbl += f"|**{earned}** | **{self.assignment.total} ({pct}%)**|\n"
        tbl += "<hr/>"

        remark = ""
        if pct == 100:
            remark = "Perfect!"
        elif pct > 0.90:
            remark = "Great job!"
        elif pct > 0.8:
            remark = "Nice work!"


        tbl += f"{remark} Please contact {utils.NAME} at {utils.EMAIL} if you have any additional questions."

        utils.printmd(tbl)

        print("Save to file? [y/n]")
        if input(">>> ").lower() == "y":
            fname = f"{self.path}/feedback.md"
            with open(fname, "w") as f:
                f.write(tbl)

            print(f"Saved to {fname}. Open in a text editor to add any additional comments.")


    def run_file(self, q):
        outputs = []

        for test in [str(t) for t in q.test_cases]:
            p = PopenSpawn(f"python {self.get_path(q.file)}")
            p.sendline(test)
            outputs.append(str(p.read().decode('utf-8')))

        return outputs

    def parse_name_and_num(self):
        name = re.findall(r"^[^_]+", self.path.name)[0]
        num = re.findall(r"(?<=_)(\d*)(?=_)", self.path.name)[0]
        return name, num

    def get_file(self, f):
        return self.get_path(f).open().read()

    def get_path(self, f):
        for file in self.files:
            if f in str(file):
                return file
        return False

    @staticmethod
    def to_file(file):
        pass

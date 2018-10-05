import os
from sys import exit
from zipfile import ZipFile as _zip
from glob import glob, iglob
import shutil
from pathlib import Path
import re
from IPython.display import Markdown, display


### CONFIG

EXCLUDED = [".ipynb_checkpoints", "soln", "Assignment Marking.ipynb"]
SOLN_DIR = "."
MARKING_SCHEME = "marking.txt"

ASSIGNMENT_NUM = 1

NAME = "Jacob Danovitch"

first, last = NAME.split()
EMAIL = f"{first}.{last}@carleton.ca".lower()

TEST_CASES = {
    "a1_p1.py": ["-4", "15", "26.5"],
    "a1_p2.py": ["-4", "15", "26.5"],
    "a1_p3.py": [["14", "19", "20", "20", "27", "9", "30", "45"]],
    "a1_p4.py": ["25", "-25"]
}


###


### Util functions  

def extract_subdirs():
    for d in glob('./**/', recursive=True):
        parts = Path(d).parts

        if len(parts) > 1 and "_MACOSX" not in d:
            for f in os.listdir(path=d):
                source = Path(d + f)
                target = Path("".join(list(parts)[:-1]) + f"/{f}")
                shutil.move(source, target)


def recursive_unzip(dr):
    for filename in iglob(dr, recursive=True):
        DEST_PATH = os.path.dirname(filename)

        _zip(filename).extractall(path=DEST_PATH)
        os.remove(filename)


def get_first_unmarked():
    for directory in os.listdir():
        if directory not in EXCLUDED:
            assignment_path = f"./{directory}/"
            feedback_file = re.search(r"feedback.*", ", ".join(os.listdir(path=assignment_path)))

            if not bool(feedback_file):
                return Path(directory)
    return False

def parse_float(_in):
    if _in.lower() in ["q", "quit", "exit"]:
        exit()

    try:
        return float(_in), True
    except:
        return _in, False


def printmd(md):
    display(Markdown(md))


def parse_name_and_num(path):
    name = re.findall(r"^[^_]+", path)[0]
    num = re.findall(r"(?<=_)(\d*)(?=_)", path)[0]
    return name, num

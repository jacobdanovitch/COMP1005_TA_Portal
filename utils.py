from sys import exit
import re
from IPython.display import Markdown, display

from pexpect.popen_spawn import PopenSpawn

from configs.config import MARKING_SCHEME, EMAIL, TEST_CASES, ASSIGNMENT_NUM, MARKED_BY


def parse_float(_in):
    if _in.lower() in ["q", "quit", "exit"]:
        exit()

    try:
        return float(_in), True
    except:
        return _in, False


def run_file(f, test):
    p = PopenSpawn(f"python {f}")
    if type(test) == type([]):
        p.send("\n".join(test))
    else:
        p.send(test)
    p.sendeof()

    out = p.read().decode('utf-8')
    if not out:
        return f"No output received from file {f}."

    return out

def parse_name_and_num(path):
    try:
        # name = re.findall(r"^[^_]+", path)[0]
        # num = re.findall(r"(?<=_)(\d*)(?=_)", path)[0]
        s = path.split("_")
        name = " ".join(s[:2])
        num = None
        return name, num
    except IndexError as e:
        raise IndexError(f"Invalid name and num for {path}.").with_traceback(e.__traceback__)

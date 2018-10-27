import os
from sys import exit, stderr
from pygments import highlight, lexer, format
from pygments.formatters.html import HtmlFormatter
from pygments.lexers.python import Python3Lexer, PythonConsoleLexer, Python3TracebackLexer
from pexpect.popen_spawn import PopenSpawn
from flask import Markup
from configs.config import MARKING_SCHEME, EMAIL, TEST_CASES, ASSIGNMENT_NUM, MARKED_BY
import re
from glob import glob
from pathlib import Path

from subprocess import run, PIPE

def log(msg):
    print(str(msg), file=stderr)


def parse_float(_in):
    if _in.lower() in ["q", "quit", "exit"]:
        exit()

    try:
        return float(_in), True
    except:
        return _in, False


def run_file(f, test):
    log(f)
    """
    p = PopenSpawn(f"python {f}")
    
        p.send("\n".join(test))
    else:
        p.send(test)
    p.sendeof()
    """
    if isinstance(test, list):
        test = "\n".join(test)

    p = run(f"python {f}", stdout=PIPE, stderr=PIPE, input=test, encoding='ascii')

    returncode = p.returncode
    out = p.stdout if (returncode == 0) else p.stderr

    return returncode, out


def execute_files(file_dir):
    files = []

    file_list = [Path(p) for p in glob(os.path.join(file_dir, "*.py"))]

    for file in file_list:
        with file.open() as py:
            code = Markup(highlight(py.read(), Python3Lexer(), HtmlFormatter()))
            log(code)
        outputs = []

        for test in TEST_CASES[file.name.replace(".py", "")]:
            returncode, out = run_file(file, test)

            Lex = PythonConsoleLexer if (returncode == 0) else Python3TracebackLexer

            out = Markup(highlight(out, Lex(), HtmlFormatter()))
            if not returncode:
                out = "Code completed with no errors." + out

            outputs.append(out)

        files.append((file, code, outputs))
    return files


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

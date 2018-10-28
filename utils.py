import json
import os
from sys import exit, stderr
from pygments import highlight, lexer, format
from pygments.formatters.html import HtmlFormatter
from pygments.lexers.python import Python3Lexer, PythonConsoleLexer, Python3TracebackLexer
from flask import Markup
from configs.config import MARKING_SCHEME, EMAIL, TEST_CASES, ASSIGNMENT_NUM, MARKED_BY, ROOT_DIR
import re
from glob import glob
from pathlib import Path
from zipfile import ZipFile as _zip
from subprocess import run, PIPE
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {"zip"}


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
    if isinstance(test, list):
        test = "\n".join(test)

    try:
        p = run(f"python {f}", stdout=PIPE, stderr=PIPE, input=test, encoding='ascii', timeout=5)

        returncode = p.returncode
        out = p.stdout if (returncode == 0) else p.stderr

        return returncode, out
    except Exception as e:
        return 1, str(e.with_traceback(e.__traceback__))


def execute_files(file_list):
    files = []

    for file in file_list:
        with file.open() as py:
            code = Markup(highlight(py.read(), Python3Lexer(), HtmlFormatter()))
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
        log(s)
        name = " ".join(s[:2])
        num = None  # re.search(r"", s[1]).group()
        return name, num
    except IndexError as e:
        raise IndexError(f"Invalid name and num for {path}.").with_traceback(e.__traceback__)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def process_zip(file, file_dir):
    if not allowed_file(file.filename):
        return False, f"Invalid file extension for file: {file.filename}."
    zipped = _zip(file)

    if not zipped.filelist:
        return False, "File list is empty."

    to_upload = []

    for z in zipped.filelist:
        if z and ".py" in z.filename:
            f = Path(z.filename)
            name = f.stem

            if f.parent.name:  # Ignore if the file is in a subdiretory like MACOSX
                continue

            if name not in TEST_CASES:
                return False, f"Invalid file name {z.filename}. Please double check that the student has appropriately named the files.\n{TEST_CASES}"

            filename = secure_filename(z.filename)
            to_upload.append(filename)

    if to_upload:
        name, num = parse_name_and_num(file.filename)
        zipped.extractall(path=file_dir, members=to_upload)
    else:
        return False, "No valid files to upload."

    return True, ""

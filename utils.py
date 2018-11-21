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


import a4test
import runpy
from collections import OrderedDict
# from difflib import Differ
import difflib 

from diff_match_patch import diff_match_patch

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

    test_name = "phrases.txt"
    phrases = open("phrases.txt", "r").read().split("\n")

    for file in file_list:
        with file.open() as py:
            text = py.read()
            code = Markup(highlight(text, Python3Lexer(), HtmlFormatter()))
            
            attempt = runpy.run_path(file)
            
        functions = OrderedDict([
            ("loadTextFile", test_name),
            ("countWords", test_name),
            ("countSentences", test_name),
            ("removePunctuation", "\n".join(phrases)),
            ("wordFrequency", test_name),
            ("countUniqueWords", test_name),
            ("kWords", (test_name, "time")),
            ("longestWord", test_name),
            ("writeLines", (test_name, ["Test", "Does", "this", "Work"])),
            ("reverseFile", test_name),
            ("followsWord", (test_name, "time"))
        ])

        answers = {f: None for f in functions.keys()}

        for f, args in functions.items():
            try:
                if isinstance(args, tuple):
                    answers[f] = attempt[f](*args)
                else:
                    answers[f] = attempt[f](args)
            except Exception as e:
                log(f"Failed at function {f} with args {args}: {e}")
            
            with open("phrases_copy.txt", "r") as f:
                with open("phrases.txt", "w") as f2:
                    f2.write(f.read())

        outputs = []


        for test in phrases: # TEST_CASES[f"a{ASSIGNMENT_NUM}_p1"]:
            # Just for A4

            returncode, out = run_file(file, test)


            Lex = PythonConsoleLexer if (returncode == 0) else Python3TracebackLexer

            out = Markup(highlight(out, Lex(), HtmlFormatter()))
            if returncode == 0:
                out = "Code completed with no errors." + out

            outputs.append(out)

        graded, solns = a4test.grade(answers.values())
        outputs = zip(answers.keys(), graded, solns)

        diff = SideBySideDiff()

        mapStr = lambda lst: list(map(str, lst))

        to_diff = zip(mapStr(answers.values()), mapStr(solns))
        diffs = [diff.render(a, b) for a, b in to_diff]  

        fmt_ans = lambda x, i: f"<span style='background-color: {'#e6ffe6' if x else '#ffe6e6'}'>{'Correct' if x else 'Incorrect'}</span><br/>"
        
        create_modal = lambda i: f"""
            <div class='ui basic modal' data-outputID='{i}'>
                <i class="close icon"></i>
                <div class="ui icon header">
                    Output
                </div>
                <div class="content">
                    <p>Hi</p>
                </div>
            </div>
            """


        create_div = lambda func, a, i: f"<p style='cursor: pointer' data-outputID='{i}' class='output'>{func}: {fmt_ans(a, i)}</p>{create_modal(i)}" #onclick='showOutput({i})'

        outputs = [create_div(f, a, i) for i, (a, f) in enumerate(zip(graded, answers.keys()))]

        files.append((file, code, outputs))
    return files


class SideBySideDiff(diff_match_patch):

    def content(self, diffs):
        """
        Returns HTML representation of differences
        """
        old = []
        new = []
        for (flag, data) in diffs:
            text = (data.replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
                    .replace("\n", "<br>"))

            if flag == self.DIFF_DELETE:
                old.append(f"<del style='background:#ffe6e6;'>{text}</del>")
            elif flag == self.DIFF_INSERT:
                new.append(f"<ins style='background:#e6ffe6;'>{text}</ins>")
            elif flag == self.DIFF_EQUAL:
                # pass
                add = f"<span style='font-size: small;'>{text}</span>"
                old.append(add)
                new.append(add)
        
        style = "margin-left: 5%; float: left; width: 45%; overflow: auto; display: block; background-color: #fff;"
        fmt = lambda html: f"<div style='{style}'>{''.join(html)}</div>"
        
        return f"<div style='max-height: 100px; overflow-y: scroll;'>{fmt(old)}{fmt(new)}</div><hr/>"

    def old_content(self, diffs):
        """
        Returns HTML representation of 'deletions'
        """
        html = []
        for (flag, data) in diffs:
            text = (data.replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
                    .replace("\n", "<br>"))

            if flag == self.DIFF_DELETE:
                html.append(f"<del style='background:#ffe6e6;'>{text}</del>")
            elif flag == self.DIFF_EQUAL:
                html.append(f"<span>{text}</span>")
        
        style = "style='margin-left: 5%; float: left; width: 45%; overflow: auto; display: block; background-color: #fff;'"
        return f"<div style={style}>{''.join(html)}</div>"

    def new_content(self, diffs):
        """
        Returns HTML representation of 'insertions'
        """
        html = []
        for (flag, data) in diffs:
            text = (data.replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
                    .replace("\n", "<br>"))
            if flag == self.DIFF_INSERT:
                html.append(f"<ins style='background:#e6ffe6;'>{text}</ins>")
            elif flag == self.DIFF_EQUAL:
                html.append(f"<span>{text}</span>")
        return "".join(html)
    
    def render(self, lhs, rhs):
        result = self.diff_main(lhs, rhs) 
        self.diff_cleanupSemantic(result)

        return self.content(result)# f"<div>{self.old_content(result)}{self.new_content(result)}</div>"




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

            """
            if name not in TEST_CASES:
                return False, f"Invalid file name {z.filename}. Please double check that the student has appropriately named the files.\n{TEST_CASES}"
            """

            filename = secure_filename(z.filename)
            to_upload.append(filename)

    if to_upload:
        name, num = parse_name_and_num(file.filename)
        zipped.extractall(path=file_dir, members=to_upload)
    else:
        return False, "No valid files to upload."

    return True, ""

import os
from flask import Flask, request, redirect, url_for, render_template, Markup
from werkzeug.utils import secure_filename

from pathlib import Path
from pexpect.popen_spawn import PopenSpawn

from pygments import highlight, lexer, format
from pygments.lexers.python import Python3Lexer
from pygments.lexers.shell import BashLexer
from pygments.formatters.html import HtmlFormatter

from itertools import chain

import utils
from Assignment import *

UPLOAD_FOLDER = '/tmp/'
ALLOWED_EXTENSIONS = {"py"}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 15 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        for file in request.files.getlist("file"):
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for("marking"))

    return render_template("base.html")


@app.route('/files')
def list_files():
    """Endpoint to list files on the server."""
    files = []

    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.isfile(path):
            files.append(filename)
    return "".join(files)


@app.route("/marking/", methods=["GET"])
def marking():
    scripts = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if ".py" in f]
    files = []

    for f in scripts:
        fname = f"{app.config['UPLOAD_FOLDER']}{f}"
        with open(fname, "r") as py:
            code = Markup(highlight(py.read(), Python3Lexer(), HtmlFormatter()))
            outputs = []

            for test in TEST_CASES[f]:
                out = Markup(highlight(run_file(fname, test), BashLexer(), HtmlFormatter()))
                outputs.append(out)

            files.append((f, code, outputs))

    return render_template("marking.html", files=files, css=HtmlFormatter().get_style_defs(), assignment=Assignment())

@app.route("/feedback/", methods=["POST"])
def show_feedback():
    if request.method == "POST":
        a = Assignment()

        data = [float(x[1]) if x[1].isnumeric() else 0 for x in request.values.items() if x[1] != "Create Feedback"]

        questions = [q.contents for _, q in a.questions.items()]
        questions = list(chain.from_iterable(questions))

        assert len(data) == len(questions), "Questions and marks are not the same length"

        grade = sum(data)
        data.append(grade)
        pct = grade/a.total*100

        questions.append(f"/{a.total} Total ({pct:.2f}%)")

        return render_template("feedback.html", data=dict(zip(questions, data)), remarks="Nice job! " if pct > 80 else "")
    return "failure"



def run_file(f, test):
    p = PopenSpawn(f"python {f}")
    if type(test) == type([]):
        p.send("\n".join(test))
    else:
        p.send(test)
    p.sendeof()
    return p.read().decode('utf-8')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

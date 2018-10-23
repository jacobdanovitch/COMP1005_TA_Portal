import os
import tempfile
from pathlib import Path
from itertools import chain
from zipfile import ZipFile as _zip

from flask import Flask, request, redirect, url_for, render_template, Markup
from werkzeug.utils import secure_filename

from pygments import highlight, lexer, format
from pygments.lexers.python import Python3Lexer
from pygments.lexers.shell import BashLexer
from pygments.formatters.html import HtmlFormatter

from utils import *
from Assignment import *

UPLOAD_FOLDER = '/tmp/'
ALLOWED_EXTENSIONS = {"zip"}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 15 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("base.html")


@app.route("/process_upload", methods=["POST"])
def process_upload():
    if request.method == 'POST':
        errors = []
        for file in request.files.getlist("file"):
            successful_unzip, message = process_zip(file)
            if not successful_unzip:
                errors.append(message)

            if errors:
                return "\n\n".join(errors)

            name, num = parse_name_and_num(file.filename)
            return redirect(url_for("marking", name=name))


@app.route("/marking", methods=["GET", "POST"])
def marking():
    name = request.args["name"]
    return render_template("marking.html", name=re.sub(r"(?<!-.)-", ", ", name, count=1).replace("-", " "),
                           files=execute_files(name), css=HtmlFormatter().get_style_defs(),
                           assignment=Assignment())


@app.route("/feedback/<name>", methods=["POST"])
def show_feedback(name):
    if request.method == "POST":
        a = Assignment()

        data = [float(x[1]) if x[1] else 0 for x in request.values.items() if x[1] != "Create Feedback"]

        questions = [q.contents for _, q in a.questions.items()]
        questions = list(chain.from_iterable(questions))

        assert len(data) == len(questions), "Questions and marks are not the same length"

        grade = sum(data)
        data.append(grade)
        pct = grade / a.total * 100

        questions.append(f"/{a.total} Total ({pct:.2f}%)")

        return render_template("feedback.html", marked_by=a.marked_by, email=a.email, data=dict(zip(questions, data)),
                               name=name,
                               remarks="Nice job! " if pct > 80 else "")
    return "failure"


def process_zip(file):
    if not allowed_file(file.filename):
        return False, f"Invalid file extension for file: {file.filename}."
    zipped = _zip(file)

    to_upload = []
    for z in zipped.filelist:
        if z and ".py" in z.filename:
            f = Path(z.filename)
            name = f.stem

            if f.parent.name:  # Ignore if the file is in a subdiretory like MACOSX
                continue

            if name not in TEST_CASES:
                return False, f"Invalid file name {f.parent.name}. Please check that the student has appropriately named the files."

            filename = secure_filename(z.filename)
            to_upload.append(filename)

    if to_upload:
        name, num = parse_name_and_num(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], name)
        zipped.extractall(path=path, members=to_upload)
    else:
        return False, "No valid files to upload."

    return True, ""


@app.route("/files", methods=["GET"])
def list_files():
    if os.environ.get("FLASK_ENV") == "development":
        return str(os.listdir(app.config['UPLOAD_FOLDER']))
    return "access denied"


def execute_files(file_dir):
    files = []
    for file in os.listdir(os.path.join(app.config['UPLOAD_FOLDER'], file_dir)):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file_dir, file)
        with open(filepath, "r") as py:
            code = Markup(highlight(py.read(), Python3Lexer(), HtmlFormatter()))
        outputs = []

        for test in TEST_CASES[file.replace(".py", "")]:
            out = Markup(highlight(run_file(filepath, test), BashLexer(), HtmlFormatter()))
            outputs.append(out)

        files.append((file, code, outputs))
    return files


# DELET
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

import os
import re
import tempfile
from pathlib import Path
from itertools import chain
from zipfile import ZipFile as _zip

from flask import Flask, request, redirect, url_for, render_template, Markup, flash, Response
from werkzeug.utils import secure_filename

from pygments import highlight, lexer, format
from pygments.lexers.python import Python3Lexer
from pygments.lexers.shell import BashLexer
from pygments.formatters.html import HtmlFormatter

from glob import glob

from utils import *
from Assignment import *

UPLOAD_FOLDER = '/tmp/'
ALLOWED_EXTENSIONS = {"zip"}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 15 * 1024 * 1024
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = '12345'


def allowed_file(filename):
    """
    if filename.endswith('.py') and f"a{ASSIGNMENT_NUM}p" not in filename:
        return False
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("base.html")


@app.route("/process_upload", methods=["POST"])
def process_upload():
    if request.method == 'POST':
        uploads = request.files.getlist("file")

        if not uploads:
            flash("No file selected.")
            return redirect(url_for("index"))

        errors = []
        for file in uploads:
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
                           files=execute_files(os.path.join(app.config['UPLOAD_FOLDER'], name.replace(" ", "-"))), css=HtmlFormatter().get_style_defs(),
                           assignment=Assignment(MARKING_SCHEME))


@app.route("/feedback/<name>", methods=["POST"])
def show_feedback(name):
    if request.method == "POST":
        a = Assignment(MARKING_SCHEME) #TODO: fix this at some point

        data = [float(val) if val else 0.0
                for (field, val) in request.values.items()
                if field != "submit"]

        questions = [v['contents'] for k,v in a.contents.items() if k != "Total"]
        questions = list(chain.from_iterable(questions))
        log(questions)
        questions  = [f"/{q['mark']} - {q['description']}" for q in questions]

        grade = sum(data)
        data.append(f"<b>Total: {grade}</b>")
        total = a.contents["Total"]
        pct = grade / total* 100

        questions.append(f"<b>/{total} ({pct:.2f}%)</b>")

        return render_template("feedback.html",
                               author=(a.marked_by, a.email),
                               data=dict(zip(questions, data)),
                               name=name,
                               remarks="Nice job! " if pct > 80 else "")
    return "failure"


def process_zip(file):
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
        path = os.path.join(app.config['UPLOAD_FOLDER'], name.replace(" ", "-"))
        zipped.extractall(path=path, members=to_upload)
    else:
        return False, "No valid files to upload."

    return True, ""


@app.route("/files", methods=["GET"])
def list_files():
    if os.environ.get("FLASK_ENV") == "development" or True:
        path = os.path.join(app.config['UPLOAD_FOLDER'], "tmp")
        files = os.listdir(path)# glob(path, recursive=True)
        log(files)
        return str(path)
    return "access denied"



# DELET
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

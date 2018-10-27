from itertools import chain
from flask import Flask, request, redirect, url_for, render_template, flash, session
from base64 import b64encode

from utils import *
from Assignment import *

UPLOAD_FOLDER = '/tmp/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 15 * 1024 * 1024
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = '12345'

ROOT = os.path.dirname(__file__)
FROM_UPLOADS = lambda x: os.path.join(os.getcwd(), UPLOAD_FOLDER, x)


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

        file = uploads[0]

        name, num = parse_name_and_num(file.filename)
        successful_unzip, message = process_zip(file, FROM_UPLOADS(name.replace(" ", "-")))
        if not successful_unzip:
            return message

        return redirect(url_for("marking", name=name))


@app.route("/marking", methods=["GET", "POST"])
def marking():
    name = request.args["name"]

    file_dir = FROM_UPLOADS(name.replace(" ", "-"))
    file_list = [Path(p) for p in glob(f"{file_dir}/*.py")]
    out = execute_files(file_list)
    return render_template("marking.html",
                           name=re.sub(r"(?<!-.)-", ", ", name, count=1).replace("-", " "),
                           files=out,
                           css=HtmlFormatter().get_style_defs(),
                           assignment=Assignment(MARKING_SCHEME))


@app.route("/feedback/<name>", methods=["POST"])
def show_feedback(name):
    if request.method == "POST":
        a = Assignment(MARKING_SCHEME)  # TODO: fix this at some point

        data = [float(val) if val else 0.0
                for (field, val) in request.values.items()
                if field != "submit"]

        questions = [v['contents'] for k, v in a.contents.items() if k != "Total"]
        questions = list(chain.from_iterable(questions))
        log(questions)
        questions = [f"/{q['mark']} - {q['description']}" for q in questions]

        grade = sum(data)
        data.append(f"<b>Total: {grade}</b>")
        total = a.contents["Total"]
        pct = grade / total * 100

        questions.append(f"<b>/{total} ({pct:.2f}%)</b>")

        return render_template("feedback.html",
                               author=(a.marked_by, a.email),
                               data=dict(zip(questions, data)),
                               name=name,
                               remarks="Nice job! " if pct > 80 else "")
    return "failure"


@app.route("/files", methods=["GET"])
def list_files():
    if os.environ.get("FLASK_ENV") == "development" or True:
        path = os.path.join(app.config['UPLOAD_FOLDER'])
        files = glob(path, recursive=True)
        log(files)
        return str(path)
    return "access denied"


# DELET
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

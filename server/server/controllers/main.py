from sys import stdout, stderr

from flask import Blueprint, render_template, flash, request, redirect, url_for, jsonify
from flask.ext.login import login_user, logout_user, login_required
from flask_cors import CORS, cross_origin

from server.extensions import cache
from server.forms import LoginForm
from server.models import User, FileUpload

main = Blueprint('main', __name__)
cors = CORS(main)


@main.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response


@main.route('/upload',methods=['POST', 'OPTIONS'])
# @cross_origin
def upload():
    uploads = request.files.getlist("filepond")
    if not uploads:
        raise FileNotFoundError(f"No file was uploaded. {request.files[0]}")

    print("File uploaded successfully.")
    print(str(uploads), file=stderr)
    f = FileUpload(uploads[0], "~/tmp")
    print("File successfully processed.")
    return jsonify(f.file_list[0].open().read())
    

@main.route('/test', )
def test():
    return "Hello"


@main.route('/')
@cache.cached(timeout=1000)
def home():
    return render_template('index.html')



"""
@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).one()
        login_user(user)

        flash("Logged in successfully.", "success")
        return redirect(request.args.get("next") or url_for(".home"))

    return render_template("login.html", form=form)


@main.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out.", "success")

    return redirect(url_for(".home"))


@main.route("/restricted")
@login_required
def restricted():
    return "You can only see this if you are logged in!", 200
"""
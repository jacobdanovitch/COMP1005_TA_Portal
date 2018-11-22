from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash

import os
from pathlib import Path
from zipfile import ZipFile as _zip

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, value):
        return check_password_hash(self.password, value)

    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    def is_active(self):
        return True

    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User %r>' % self.username



ALLOWED_EXTENSIONS = set(".zip")

class FileUpload:
    def __init__(self, file, root_dir):
        self.file = file # Path(file)
        self.dir = os.path.join(root_dir, self.make_filename())

        self.file_list = []

        self.process_zip()

    def process_zip(self):
        if not self:
            return False, f"Invalid file extension for file: {self.file.filename}."
        
        zipped = _zip(self.file)

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

                to_upload.append(f.name)
                self.file_list.append(Path(os.path.join(self.dir, f.name)))

        if to_upload:
            zipped.extractall(path=self.dir, members=to_upload)
        else:
            return False, "No valid files to upload."

        return True, to_upload
    
    def __bool__(self):
        return FileUpload.allowed_file(self.file.filename) 

    def make_filename(self):
        name, _ = FileUpload.parse_name_and_num(self.file.filename)
        return "_".join(name.split(" "))

    @staticmethod
    def allowed_file(filename):
        # return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
        return str(filename).endswith(".zip")

    @staticmethod
    def parse_name_and_num(path):
        try:
            # name = re.findall(r"^[^_]+", path)[0]
            # num = re.findall(r"(?<=_)(\d*)(?=_)", path)[0]
            s = path.split("_")
            name = " ".join(s[:2])
            num = None  # re.search(r"", s[1]).group()
            return name, num
        except IndexError as e:
            raise IndexError(f"Invalid name and num for {path}.").with_traceback(e.__traceback__)
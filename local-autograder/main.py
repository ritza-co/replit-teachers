import datetime
import os
import pytest
import shutil

from flask import Flask
from flask import request
from werkzeug.utils import secure_filename

app = Flask(__name__)

def extract_student_number(f):
    """Gets the student number from the first line of the file"""
    sn = f.readline().decode("utf8").strip("\n")
    sn = sn.replace(" ", "").replace("#", "")
    return sn

def save_submission(f, studentnumber):
    """Saves a copy of the students submission to a subfolder"""
    dirname = studentnumber
    i = 1
    while os.path.exists(dirname):
        dirname = f"{studentnumber}_{i}"
        i += 1
    os.mkdir(dirname)
    code_destination = f"{dirname}/main{dirname}.py"
    test_destination = f"{dirname}/test_solution{dirname}.py"
    conf_destination = f"{dirname}/conftest.py"

    with open("test_solution.py") as tf:
        s = tf.read()

    s = f"import main{dirname} as main" + s
    with open(test_destination, "w") as tf:
        tf.write(s)

    shutil.copyfile("conftest.template", conf_destination)
    f.save(code_destination)
    return dirname

def run_tests(subdir):
    pytest.main([subdir, "-p", "no:cacheprovider"])


@app.route("/", methods=["GET","POST"])
def submit():
    author = "Unknown author"
    if request.method == "POST":
        try:
            codefile = request.files['codefile']
            sn = extract_student_number(codefile)
            saved_dir = save_submission(codefile, sn)
            run_tests(saved_dir)
        except Exception as e:
            print("Something went wrong")
            print(e)
            with open("errors.txt", "a") as f:
                f.write(f"received submission from {author} at {datetime.datetime.now().isoformat()} but something went wrong\n")
                f.write(str(e) + "\n")
                f.write("----------\n")
    return "OK"


if __name__ == "__main__":
    app.run("0.0.0.0")


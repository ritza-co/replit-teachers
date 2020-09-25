# Building a centralised autograder with Repl.it

In a [previous guide](#) we built a basic autograding solution that could automatically run and test your students' assignments. However, there were still some manual steps involved: you needed to navigate to each students fork of the assignment and kick of the tests manually.


In this guide, we'll show you how to take it a step further and build a centralised grading server. Your students will be able to submit their assignments to this server, and each submission will automatically kick of the tests, assign a grade, and create a summary report of submissions and grades for you to review.

Note that you'll need a subscription to [Teams for Education](#) to follow this guide as its presented, but you should also be able to adapt it to run using a normal Repl.it account if you need.

In this guide, we assume that your students are learning Python. We'll give an example Python assignment and an example testing suite using [PyTest](). We'll use Flask to create the centralised grading server.

## Overview of how the solution works

The basic workflow is similar to in the previous guide, but this time you won't need to look at each student's fork individually. Instead, students will submit them to a centralised server, and you can view their code their, or just look at the summary report it will generate.

![](https://i.ritzastatic.com/fa45c40179924e2fa23b61f19c63d980/solution-overview.png)

After a student forks the assignment, they will be able to write their code, test it on their own, and then submit it when they are satisfied with their answers. 

The grading server will not be visible to students, so they will still not be able to view each other's works or grades.

## Setting up the grading server

We'll start by creating the grading server. We don't want to share this code for students, so create a normal team Repl (not a template).

Press the `+` button in the top right corner, choose Python, call your repl "grading-server", choose your team account as the owner, and set the repl to "private".

![](https://i.ritzastatic.com/a49c5ac633374f96a41301934a2d4e58/create-server.png)

Our grading server will consist of a few different components, namely:

* A Flask server that can receive files that students submit
* PyTest code to test the student's submission
* Configuration for PyTest to extract information about how many tests were passed and calculate a grade
* A report file to keep a summary of all submissions and grades

### Creating the server in main.py

In `main.py` add the following code 

```python
import datetime
import os
import pytest
import shutil

from flask import Flask
from flask import request
from werkzeug.utils import secure_filename

app = Flask(__name__)
```

This brings in the imports that we need and initialses a Flask application.

Immediately below this, add three helper functions that we'll use in the main submission process.

```python
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
```

The first function, `extract_student_number` reads the first line of the submitted code file and looks for a student number. In the template we prepare later, we'll show students how to format this correctly

The second function `save_submission` creates a new directory on the server using the student number and populates it with the following files:

* The file that the student submitted
* The tests that we need to run
* The configuration for these tests

If the student has previously made a submission, it will add "-1" to the end of the directory, or keep incrementing this number for each resubmission so you can keep track of each submission a student makes.

The last function, `run_tests()`, calls PyTest. Instead of invoking PyTest from the command line as we did in the previous guide, this calls PyTest from within our Python code so that we can programmatically extract the results and save them to the report.

Finally, add the following code, also to `main.py`, below what you already added.

```python
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
```

This waits for a file submission and then tries to grade it. If the assignment is not in the correct format or if anything else goes wrong, it will log an error to a file called "errors.txt".

### Creating the tests

For demonstration, we're going to assume that the homework assignment requires the students to write two functions:

* `add(a, b)` which sums the two input integers and returns the result and
* `subtract(a, b)` which subtracts b from a and returns the result.

You can adapt this to your actual homework assignment as needed, but we recommend that you first make sure that everything is working with this simple example before you write a more advanced set of tests.

Create a new file called `test_solution.py` and add the following code.

```python
def test_add_two_pos():
    assert main.add(1,2) == 3

def test_add_one_neg_one_pos():
    assert main.add(-3, 1) == -2

def test_subtract_two_pos():
    assert main.subtract(5, 3) == 2

def test_subtract_two_neg():
    assert main.subtract(-2, -3) == 1
```

Each student's file will have a different name (e.g. `mainJS1337A_1.py`) so we don't hardcode the import for `main.py`. The server will logic will take care of adding the correct import line when it creates a copy of this file for each submission.


### Creating the configuration for PyTest

Finally, we need to create a special file that PyTest will trigger automatically when we call it from our `main.py` file. Create a file called `conftest.template` and add the following code. 

```python
import datetime

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    stats = terminalreporter.stats
    num_passed = len(stats.get("passed", []))
    num_failed = len(stats.get("failed", []))
    score = int(num_passed / (num_passed + num_failed) * 100)
    student_number = config.args[0]
    fdate = datetime.datetime.now().strftime("%d %B %Y %I:%M%p")

    report = f"""### {student_number} submitted at {fdate}
* **Passed:** {num_passed}
* **Failed:** {num_failed}
* **Score:** {score}%
"""
    with open("report.md", "a") as f:
        f.write(report)
```

The variables are automatically passed in by PyTest and contain information about which tests passed and which failed. This code only extracts a basic summary of how many tests passed and how many failed and we give the student a grade based on the percentage of tests that they passed.

The logic in `main.py` that you created earlier will copy a new version of this for each submission with a unique name. This is important to stop the tests conflicting with each other as PyTest keeps a local cache of tests for efficiency.

That's it for our server. Press the "Run" button and your server should start running and display an "OK" message, as shown below. 

Take a note of the URL which is based on your team and project name as we'll need to add this to the student assignment that we create in the next step.

![](https://i.ritzastatic.com/47e1bcf63eb946adacb4f500e5e45204/running-server-and-url.png)


## Setting up the assignment 

Now that we have a server, we need to build the other half: the assignment template for students to fork and submit.

### Create a new template 

On your teams page, create a new template. This will be specific to a single assignment for your students so call it something like "Grade 10 Python homework week 1" so you can keep track of different assignments for different classes.

![](https://i.ritzastatic.com/175ab1509be64763bcb7f38662dad9af/create-template.png)

### Add the code for the assignment

Our assignment needs the following three components:

* The starter code and instructions for students to work on
* A basic testing harness so that students can test their work (unlike in the previous guide, students won't have access to the full test suite that we use for grading)
* Code to submit the assignment to the central server

In the `main.py` file, add the following code.

```python
# JS1337A
# Ensure the above line contains exactly your student number.
# 
# You can test your code by pressing the run button. 
# Once you are happy with it, uncomment the "`MODE = "SUBMIT"` line 
# and press the Run button again to submit
# -----------------------------------------------------------------

MODE = "TEST"
# MODE = "SUBMIT"

def add(a, b):
    """Add a and b and return the sum"""
    pass

def subtract(a, b):
    """Subtract b from a and return the result"""
    pass

def test():
    r = add(1, 2)
    print(f'add(1, 2) returns {r}')
    r = subtract(5, 2)
    print(f'subtract(5, 2) returns {r}')

def main():
    if MODE == "SUBMIT":
        from submit import submit
        submit()
    else:
        test()

if __name__ == "__main__":
    main()
```

Change the comment on the very first line to match the format that your students are used to identifying themselves by. This will be used in the report that the server generates and also for the directory names that it uses to store the students' code.

The two global variables at the top indicate whether the student is ready to submit or not. By default, the code is in testing mode and when the student presses the "run" button, it will run their code and display the results to them. 

Once they uncomment the `# MODE = "SUBMIT"` line, it changes to submission mode. Now when the student hits the run button, it'll submit the code to our server.

The `add()` and `subtract()` functions are starter code for the student to work from. The `test()` function runs these functions with some sample inputs and shows the results to the student.

The `main()` function checks what mode we are in and either runs the code locally or submits it to the server.

### Creating the submission script

Create a new file in the template called `submit.py` and add the following code.

```python
import requests

# CHANGE THE FOLLOWING LINE TO YOUR URL
url = "https://HomeworkGrader.ritza.repl.co"

def submit():
    with open("main.py", "rb") as f:
        files = {'codefile': f}
        r = requests.post(url, files=files)
        if r.ok:
            print("Your code has been submitted")
        else:
            print("Sorry, something went wrong")
```

Change the url to the one that you copied in the final step of the server set up, as this is where the students' assignments will be submitted.

### Testing it all out

To make sure that everything works as expected, run the template. It's still in test mode, so it should run the two functions with the example inputs and display the output. Because we only have the starter code, we can see that the functions don't work yet.

![](https://i.ritzastatic.com/ead348c62baa4a28a08b86a42d8a6325/running-template-starter.png)

Now fill out the two functions so that they look as follows. Note that we have deliberate error in the `subtract()` function to make sure that our grading is working as expected.

```python
def add(a, b):
    """Add a and b and return the sum"""
    return a + b

def subtract(a, b):
    """Subtract b from a and return the result"""
    return b - a
```

Hit run again and you should see that the functions return results now.

![](https://i.ritzastatic.com/84fff66b30da42b89bba6b86428fa138/running-template-completed-errors.png)

Uncomment the `# MODE = "SUBMIT"` line and press "Run" again. This time it should submit the solution to the grader and return a confirmation message.

![](https://i.ritzastatic.com/900076ca08094f929a0a387c39bfcb62/submission-confirmed.png)

Fix the subtract function by swapping `b` and `a` as follows and submit it one more time by pressing the Run button. This lets us test that resubmissions are working.

```python
def subtract(a, b):
    """Subtract b from a and return the result"""
    return a - b
```

Finally, change all of the code back to how it was as this is the version that students will fork and we don't want them to have the solutions. Recomment out the `MODE = "SUBMIT"` line and remove the return statements, replacing them with `pass` instead.

```python
MODE = "TEST"
# MODE = "SUBMIT"

def add(a, b):
    """Add a and b and return the sum"""
    pass

def subtract(a, b):
    """Subtract b from a and return the result"""
    pass
```

### Viewing the submitted code and report

Navigate back to your `grading-server` project and you should see some new files and folders that have been created by the grading project.

Each of the submission generated a new subfolder with the student number in the first line of the submission file.  Because they were the same, the second one had `_1` appended to it.

In each of these folders, you can see the code that was submitted.

You can also see `report.md` has been generated, with details of the two submissions (who submitted them and when) and their calculated grades.

![](https://i.ritzastatic.com/1ea3403b1f18430ab434284c9d080933/example-report.png)


## Where next?

Now you have a robot to take care of most of your grading for you which should save you a bunch of time! In this guide, we showed you how to set up an autograder, but you might like to extend it on your own with some additional features. For example, you could

* Create a more sophisticated directory and reporting structure so that different assignments can be submitted to the same server without all being mixed up into a single directory and single report.
* Set up a service like [UpTimerRobot](https://uptimerobot.com/) to keep an eye on your grading server and notify you if it becomes unavailable (this also stops Repl.it shutting it down from inactivity)
* Return the grades to students so that they see "You scored 75%" after submitting instead of just "Your code has been submitted".

We've focussed on Python in this guide, but you should be able to adapt it to testing and grading submissions in JavaScript, Java, or other languages with some work. In future guides, we'll give examples of how to do this.

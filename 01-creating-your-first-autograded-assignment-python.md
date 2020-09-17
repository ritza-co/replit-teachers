# Create your first autograded Python homework with Repl.it

**Note: you need a subscription to Repl.it's [Teams for Education](https://blog.repl.it/teams-for-education) as well as a team where you have owner or admin privileges in order to follow this guide.**

If you teach a programming course and wish that you could build a robot to grade your students' homework for you, you can! In this guide, you'll see exactly how to set it up with some real-world examples. 

Autograding is done by having unit tests automatically execute your students' code with pre-specified inputs and checking if the outputs are as expected. 

Specifically, we'll cover:
* Setting up templates and permissions on Repl.it Teams for Education  
* Creating a skeleton assignment for your students to work on
* Creating tests to check your students submissions automatically
* Running these tests with PyTest.

## What is autograding and how can it help you?

Autograding comes in a variety of different forms. 

* **No autograding:** Without any autograding, your students submit code and you have to inspect it line by line and manually specify inputs. 
* **Partial auto-grading:** To save time, you might have a script that runs your students code with a pre-specified set of inputs to see exactly how it works and where it breaks, but you still need to decide what grade to award based this.
* **Full autograding:** You have a sophisticated testing suite and the students' grades are determined by how many tests their code passes.

In this guide, we'll show you how to set up a system that implements the completely hands-off version: **full autograding**. 

In theory, students could receive their grade automatically too, minutes after they submit. In the version we build though, only you, the teacher, will get the summary of grades, so that you can check these, add any personalised comments, and then share with your students at your convenience.

## Understanding Repl.it teams: admins, members, and templates
Before we get started with building the autograded solution, you should have a good understanding of some concepts from Repl.it teams. Specifically, we'll be using different roles (admin and member) and **templates**. You can skip this section if you've already familiar with how these work.

### The admin and member roles in Repl.it teams

If you're using teams for education, you should make sure that you're added as an 'owner' or 'admin' role while all of your students are 'members'.

This means that you will be able to see all submissions (called 'forks') of the homework, while your students will only be able to see the skeleton (or 'template' as described below) that you provide.

![](https://static.ritza.co/repl/01-member-roles.png)

### Understanding templates

Templates let you create a repl that might have different variants. For example, you can add the homework questions and skeleton code to a template and each student can then easily create their own version of this.

* Admins and owners can edit the main copy of the template: any changes they make will be seen by any student who creates a copy.
* Once the tempalte is published, members (students) can only see the template and create their own copy to work on their submission. They cannot edit the main copy.
* People outside the team cannot see the template at all.

## Create your first template

Create a template for the homework assignment you want to prepare and add some details to help you and your students identify it. You can also specify what programming language to use. In this exampe, we'll use Python.

![](https://static.ritza.co/repl/02-create-a-template.png)

Hit the create button and you'll be taken to a normal repl but with some additional features. Note the 'publish template' button in the top right that we'll use later.

## Writing a skeleton homework assignment

In the `main.py` file, write the instructions as comments and any skeleton code that you want your students to use. 

An example of this is:

```python
## Week 2 assignment
# Fix the functions so that they work as expected
# ---------------------------------------------------

def add(a, b):
    """adds two numbers: a and b"""
    pass

def subtract(a, b):
    """subtract two numbers: b from a"""
    pass

```

In this example, we are only asking them to create two basic functions, `add` and `subtract`.

### Adding tests

Now create a new file called `test_main.py` and add the following code

```python
import main

def test_add():
    assert main.add(1, 2) == 3

def test_subtract():
    assert main.subtract(4, 2) == 2

```

This imports the skeleton functions from the `main.py` file and calls them with some test data. The first one checks that we get `3` when calling `add(1, 2)` and the second that we get `2` when calling `subtract(4,2)`.

Of course these tests won't pass at the moment beause the functions haven't been written yet, but let's run them to check that everything is working.

## Installing PyTest

![](https://static.ritza.co/repl/installing-pytest-pm.png)

To run the tests, we'll use `pytest`, which is a Python package. Install it by 

1. Clicking on the package icon in the left menu bar
2. typing `pytest` into the search box
3. Clicking on `pytest` from the results.
4. Click the plus button to install the package

![](https://static.ritza.co/repl/05-clicking-install.png)

## Running the tests

PyTest looks for test code automatically (files and functions that start with `test_`, like we used above), so you don't need to configure anything else.

Open the command shell by pressing `Cmd + Shift + S` on MacOS or `Ctrl + Shift + S` on other computers. Note that this is different from the Python output pane that's open by default. The command shell will open up below the Python one, as shown here.

![](https://static.ritza.co/repl/06-opening-shell.png)

Type in `pytest` and press Enter. This will invoke PyTest, look for the tests we wrote, and run them. You should see output similar to that shown below.

![](https://static.ritza.co/repl/07-failed-tests.png)

PyTest is designed to help software engineers find bugs more than it is for grading homework so you'll see it produces a lot of output to pinpoint exactly what went wrong. The last two lines of summary are the most interesting for our purposes though: we can see our first test returned `None` while we were expecting `3` and our second test also returned `None` while we were expecting 2.

This means that our set up is working: it's the students' job to fix the functions so that they pass these tests.

Before students can see and submit this homework you need to 'publish' it. Do that now by pressing the button in the top right.

![](https://static.ritza.co/repl/08-publishing-template.png)

Now slide the button across to 'published' and your students can access the template.

![](https://static.ritza.co/repl/09-publishing-2.png)

## Submitting your homework as a student

To experience the process from your students perspective, sign into a normal 'member' account that's part of your team plan. You can use a different web browser or incognito window to stay signed into your teacher account at the same time.

You'll see all of your published templates but no 'edit' button. Instead there'll be a 'fork template' button which is the first thing your student needs to press to begin the homework assignment.

![](https://static.ritza.co/repl/10-forking-a-template.png)

The student can now make changes to the code. In this example, she fills out the return statements. Note how `a` and `b` are in the wrong order in the subtract function: the correct answer is `return a - b`. 

![](https://static.ritza.co/repl/11-adding-changes-student.png)

Once the student is satisfied, she can press the 'submit' button in the top right.

## Viewing all submissions as a teacher

Back in your teacher account, navigate to the team dashboard and find the relevant template. Press the 'View forks' button.

![](https://static.ritza.co/repl/12-viewing-forks.png)

You'll be taken to a page where you can see all versions of this assignment. In this example, we only see one (from the test we created above). Once your students start forking the assignment you'll see more, and each of them will be labeled as "submitted" or "unsubmitted", depending on whether or not the student has pressed the submit button.

![](https://static.ritza.co/repl/13-forks.png)

Open the fork, open the command shell and run `pytest` again. You should see one test pass and one fail. The subtract function is calculating `2-4` instead of `4-2` and getting the wrong answer.

![](https://static.ritza.co/repl/14-one-fail.png)

Once your students have each created a fork and submitted an assignemtn, you can open each of the students forks and run `pytest` to easily see a summary of how many tests they passed and what mistakes they made. If you want, you can simply use the percentage of the tests passed as a grade: for example, our imaginary student would be awarded 50% for passing 1/2 tests.

While this is a semi-automated solution, you are still required to open each solution manually in order to kick of the tests. In [Creating a centralised grading application with Repl.it](#), we look at taking autograding a step further to avoid this.

## Conclusion

In this guide we showed you how to set up a basic auto-graded Python assignment. Unit tests are pretty powerful and you can use them to do more than just check basic inputs and outputs. For example, it's possible to check how many times a function was called (e.g. to check if students are using `open()` correctly), to check if specific Exceptions are raised, and more.

We focused on using PyTest and Python, but all languages have their own unit testing frameworks. You can use [JUnit](https://junit.org) for Java or [Jest](https://jestjs.io/) for JavaScript in similar ways.











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

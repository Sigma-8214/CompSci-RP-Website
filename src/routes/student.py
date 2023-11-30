import random
from flask import render_template, session, flash, redirect, url_for

from app import app
from database import Student


# route for the student view
@app.route("/student")
@app.route("/s")
def student():
    # first check if the student is logged in
    if "student" in session:
        # if logged in, display the student's info
        found_student = Student.query.filter_by(name=session["student"]).first()
        return render_template(
            "student.html",
            student=found_student,
            random_tail_length=random.randint(1, 10),
        )

    # user is not logged in -> login page
    flash("You are not logged in!")
    return redirect(url_for("login"))

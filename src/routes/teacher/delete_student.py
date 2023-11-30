from flask import render_template, flash, redirect, url_for, request, session

from app import app, db
from database import Student


@app.route("/deletestudent", methods=["POST", "GET"])
def deletestudent():
    if "teacher" in session:
        if request.method == "POST":
            # get the student id from the form
            student_id = request.form["studentid"]

            # delete the student from the database
            Student.query.filter_by(_id=student_id).delete()
            db.session.commit()
            flash("Student deleted!")
        return redirect(url_for("teacher"))
    else:
        # user is not logged in -> login page
        flash("You are not logged in!")
        return redirect(url_for("login"))

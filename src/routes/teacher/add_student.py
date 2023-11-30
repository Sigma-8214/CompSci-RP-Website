from flask import render_template, flash, redirect, url_for, request, session

from app import app, db
from database import Student
from send_mail import sendNewUserEmail


# route for adding a student to the table
@app.route("/addstudent", methods=["POST", "GET"])
def addstudent():
    if "student" in session:
        return redirect(url_for("student"))

    if "teacher" in session:
        # get the form data
        name_in = request.form["name"]
        period_in = request.form["period"]
        email_in = request.form["email"].lower()
        send_email_toggle_in = request.form.get("sendEmailToggle")

        # make sure the email does not already exist in the database
        emails_found = Student.query.filter_by(email=email_in).first()
        if emails_found:
            flash("Email already exists!")
            return redirect(url_for("teacher"))

        # create a new student object
        new_student = Student(name_in, int(period_in), email_in)

        # add the new student to the database
        db.session.add(new_student)
        db.session.commit()
        print("added to database")

        if send_email_toggle_in:
            # send the new student's password to their email
            sendNewUserEmail(email_in, new_student.password)

        flash("Added new student.")
        return redirect(url_for("teacher"))

    # user is not logged in -> login page
    flash("You are not logged in!")
    return redirect(url_for("login"))

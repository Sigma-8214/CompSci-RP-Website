from flask import render_template, session, flash, redirect, url_for, request

from app import app, db
from database import Student
from send_mail import sendNewUserEmail


# route for the register page
# *to be used only by students
@app.route("/signup", methods=["POST", "GET"])
@app.route("/register", methods=["POST", "GET"])
def register():
    # first check if the user is logged in
    if "student" in session:
        # redirect to the student view
        flash("You are already logged in!")
        return redirect(url_for("student"))

    elif "teacher" in session:
        # redirect to the teacher view
        flash("You are already logged in!")
        return redirect(url_for("teacher"))

    # user is not logged in

    # check if the user is trying to register
    if request.method != "POST":
        # user is not trying to register
        # display the register page
        return render_template("register.html")

    session.permanent = True

    # user is trying to register

    # get the form data
    name_in = request.form["name"]
    period_in = request.form["period"]
    email_in = request.form["email"].lower()

    # make sure the email does not already exist in the database
    emails_found = Student.query.filter_by(email=email_in).first()
    if emails_found:
        flash("Email already exists!")
        return redirect(url_for("register"))

    # create a new student object
    new_student = Student(name_in, int(period_in), email_in)

    # add the new student to the database
    db.session.add(new_student)
    db.session.commit()
    print("added to database")

    # send the new student's password to their email
    sendNewUserEmail(email_in, new_student.password)

    flash("Registered! Your password has been sent to your school email.")
    print("redirecting to login page")
    return redirect(url_for("login"))

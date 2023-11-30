from flask import render_template, session, flash, redirect, url_for, request

from app import app
from database import Student
from config import teacher_password


# route for the home page (it's just the login page)
@app.route("/", methods=["POST", "GET"])
@app.route("/home", methods=["POST", "GET"])
@app.route("/login", methods=["POST", "GET"])
def login():
    # first check if you're already logged in
    if "student" in session:
        # redirect to the student view
        flash("You are already logged in!")
        return redirect(url_for("student"))
    elif "teacher" in session:
        # redirect to the teacher view
        flash("You are already logged in!")
        return redirect(url_for("teacher"))

    # user is not logged in
    # check if the user is trying to log in
    if request.method != "POST":
        # user is not trying to log in -> display the login page
        return render_template("login.html")

    # get the form data
    password = request.form["password"]

    # prompt password again if it's not a number
    if not password.isdigit():
        flash("Please enter a number!")
        return redirect(url_for("login"))

    # prompt password again if it's not 6 digits
    if len(password) != 6:
        flash("Please enter a 6-digit number!")
        return redirect(url_for("login"))

    # check if the teacher is trying to log in
    if password == teacher_password:
        # log the teacher in
        session["teacher"] = "teacher"
        flash("Logged in!")
        return redirect(url_for("teacher"))

    # if password found, log the user in
    found_user = Student.query.filter_by(password=password).first()
    if found_user:
        # log the student in
        print("logging in student")
        session["student"] = found_user.name
        # flash("Logged in!")
        return redirect(url_for("student"))

    # if password not found, display an error message
    else:
        flash("Password not found!")
        return redirect(url_for("login"))

from flask import render_template, flash, redirect, url_for, request

from app import app
from database import Student
from send_mail import sendForgotPasswordEmail


@app.route("/forgotpassword", methods=["GET", "POST"])
@app.route("/forgot", methods=["GET", "POST"])
def forgotpassword():
    if request.method != "POST":
        return render_template("forgotpassword.html")

    # get the email from the form
    email_in = request.form["email"]

    # make sure the email exists in the database
    user_found = Student.query.filter_by(email=email_in).first()
    if user_found:
        # send the user an email containing their password
        sendForgotPasswordEmail(email_in, user_found.password)
        flash("An email containing your password has been sent to you!")
        return redirect(url_for("login"))
    else:
        flash("The email you entered is not registered!")
        return redirect(url_for("forgotpassword"))

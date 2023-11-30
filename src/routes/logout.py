from flask import session, flash, redirect, url_for

from app import app


@app.route("/logout")
def logout():
    # first check if the user is logged in
    if "student" in session:
        # log the student out
        session.pop("student", None)
        flash("Logged out!")
        return redirect(url_for("login"))

    if "teacher" in session:
        # log the teacher out
        session.pop("teacher", None)
        flash("Logged out!")
        return redirect(url_for("login"))

    # user is not logged in
    flash("You are not logged in!")
    return redirect(url_for("login"))

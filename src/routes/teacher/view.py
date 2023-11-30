from flask import render_template, flash, redirect, url_for, request, session

from app import app, db
from database import Student


# route for the teacher view
@app.route("/teacher", methods=["POST", "GET"])
@app.route("/t", methods=["POST", "GET"])
def teacher():
    # first check if the teacher is logged in
    if "teacher" in session:
        # if logged in, first check if the save button was pressed
        if request.method == "POST":
            users = []
            for i in range(len(Student.query.all())):
                str_id = "studentid" + str(i)
                str_name = "studentname" + str(i)
                str_period = "studentperiod" + str(i)
                str_email = "studentemail" + str(i)
                str_password = "studentpassword" + str(i)
                str_rp = "studentrp" + str(i)

                id_input = request.form[str_id]

                name_input = request.form[str_name]

                try:
                    period_input = int(request.form[str_period])
                except:
                    # someone put an "e" in the period input (we don't know how to prevent them from doing it)
                    flash(
                        f"Please enter a valid period number for {name_input} (id: {id_input})"
                    )
                    return redirect(url_for("teacher"))

                # make sure period is a number between 1 and 8, inclusive
                if period_input < 1 or period_input > 8:
                    flash(
                        f"Please enter a valid period number for {name_input} (id: {id_input})"
                    )
                    return redirect(url_for("teacher"))

                email_input = request.form[str_email]

                # first check if the email has been changed/edited
                if email_input != Student.query.filter_by(_id=id_input).first().email:
                    # make sure email is unique
                    emails_found = Student.query.filter_by(email=email_input).first()
                    # also making sure the matching email is not the same student
                    if emails_found and emails_found._id != id_input:
                        flash(
                            f"The email you're trying to change for {name_input} (id: {id_input}) is already taken by {emails_found.name} (id: {emails_found._id})"
                        )
                        return redirect(url_for("teacher"))

                    # make sure email is valid
                    # for now, just checking if it's empty
                    if email_input == "":
                        flash(
                            f"Please enter a valid email for {name_input} (id: {id_input})"
                        )
                        return redirect(url_for("teacher"))

                password_input = request.form[str_password]
                # LOGIC FOR VALIDATING NEW PASSWORD:
                # 1. check if the password has been changed/edited
                if (
                    password_input
                    != Student.query.filter_by(_id=id_input).first().password
                ):
                    # 2. make sure password is made up of only numbers
                    if not password_input.isdigit():
                        flash(
                            f"Please enter a valid password for {name_input} (id: {id_input})"
                        )
                        return redirect(url_for("teacher"))
                    # 3. remove leading zeroes
                    password_input = str(int(password_input))
                    # 4. make sure password is 6 digits or less
                    if len(password_input) > 6:
                        flash(
                            f"Please enter a valid password for {name_input} (id: {id_input})"
                        )
                        return redirect(url_for("teacher"))
                    # 4a. if it's less than 6 digits, add leading zeroes
                    if len(password_input) < 6:
                        password_input = password_input.zfill(6)
                    # 5. make sure password is unique (doesn't already belong to another student)
                    password_found = Student.query.filter_by(
                        password=password_input
                    ).first()
                    # also making sure the matching password is not the same student
                    if password_found and password_found._id != id_input:
                        flash(
                            f"The password you're trying to change for {name_input} (id: {id_input}) is already taken by {password_found.name} (id: {password_found._id})"
                        )
                        return redirect(url_for("teacher"))

                try:
                    rp_input = int(request.form[str_rp])
                except:
                    # someone put an "e" in the rp input (we don't know how to prevent them from doing it)
                    flash(
                        f"Please enter a valid number of RP for {name_input} (id: {id_input})"
                    )
                    return redirect(url_for("teacher"))

                users.append(
                    [
                        id_input,
                        name_input,
                        period_input,
                        email_input,
                        password_input,
                        rp_input,
                    ]
                )

            # update the database
            for i in range(len(users)):
                # using the id for the filter because that can't be changed
                found_user = Student.query.filter_by(_id=users[i][0]).first()

                # IF YOU MAKE ALL TABLE CELLS INTO INPUTS, UNCOMMENT THIS
                found_user.name = users[i][1]
                found_user.period = users[i][2]
                found_user.email = users[i][3]
                found_user.password = users[i][4]
                found_user.rp = users[i][5]

                db.session.commit()

            flash("Saved!")
            return redirect(url_for("teacher"))

        # display the table of students
        # sort the students by period, then name when you pass it to the html
        return render_template(
            "teacher.html", students=Student.query.order_by(Student._id).all()
        )

    else:
        # user is not logged in -> login page
        flash("You are not logged in!")
        return redirect(url_for("login"))

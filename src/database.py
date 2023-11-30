from flask_sqlalchemy import SQLAlchemy
import random

from app import db


class Student(db.Model):
    # create columns
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    period = db.Column(db.Integer())
    email = db.Column(db.String(100))
    password = db.Column(db.String(6))
    rp = db.Column(db.Integer())

    def __init__(self, name, period, email):
        self.name = name
        self.period = period
        self.email = email

        # password is initialized to a random 6-digit number
        random_password = random.randint(000000, 999999)

        # make sure the password is unique
        # get all the passwords from the database
        passwords = Student.query.with_entities(Student.password).all()
        # check if the random password is already in the database
        while str(random_password) in passwords:
            random_password = random.randint(000000, 999999)

        # add leading zeroes to the password if it's less than 6 digits
        random_password = str(random_password)
        while len(random_password) < 6:
            random_password = "0" + random_password

        # set the password
        self.password = random_password

        self.rp = 0

    def __repr__(self):
        return f"Name ({self.name}), Password ({self.password}), Points ({self.rp}), Email ({self.email}), Period ({self.period})\n"

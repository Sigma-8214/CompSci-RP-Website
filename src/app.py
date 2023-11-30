from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import secret_key, db_address

app = Flask(__name__)
app.instance_path = "./instance"
app.template_folder = "../templates"
app.static_folder = "../static"
app.secret_key = secret_key

# settings for sql database
app.config["SQLALCHEMY_DATABASE_URI"] = db_address
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# create the database object
db = SQLAlchemy(app)

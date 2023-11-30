from flask import Response

from app import app
from main import VERSION

AUTHORS = "Originally By Matthias Masiero and Jaiman Munshi\nUpdated by Connor Slade"


@app.get("/version")
def version():
    res = Response(f"CompSci-RP-Website v{VERSION}\n{AUTHORS}")
    res.mimetype = "text/plain"
    return res

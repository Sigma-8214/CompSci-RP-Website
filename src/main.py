from config import debug, host, port
from app import app, db
import routes

VERSION = "0.1.0"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(host=host, port=port, debug=debug)

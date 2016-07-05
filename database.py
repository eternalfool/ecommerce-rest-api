from flask_sqlalchemy import SQLAlchemy

db = None


def init(app):
    global db
    db = SQLAlchemy(app)

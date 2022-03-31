
from main import app
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy(app)



class Users(db.Model):
    """ Class that stores the user's usernames"""

    id =  db.Column("id", db.Integer, primary_key=True)
    user_name = db.Column("username", db.String(100))
    messasges =  db.relationship("Message_history", backref="author", lazt="dynamic")

    #id is automatically created as it is the primary key
    def __init__(self, user_name):
        """Initialises a new user"""

        self.user_name = user_name


class Message_history(db.Model):
    """ Class that stores the user's usernames"""

    __bind_key__ = 'messages'
    id =  db.Column("id", db.Integer, primary_key=True)
    message = db.Column("messages", db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))


    #id is automatically created as it is the primary key
    def __init__(self, message):
        """Initialises a new message"""

        self.message = message

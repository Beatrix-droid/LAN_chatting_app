

from config import *
from flask import (Flask, flash, redirect, render_template, request, session,
                   url_for)

from flask_socketio import SocketIO, send, emit
from flask_sqlalchemy import SQLAlchemy

from flask_session import Session


app = Flask(__name__)
socketio = SocketIO(app)

#loading the config file

if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")
#with this can leave code alone and control the config environment outside of the application
#using the terminal


app.static_folder = "static"



#print(app.config)
db = SQLAlchemy(app)
Session(app)



class Users(db.Model):
    """ Class that stores the user's usernames"""

    id =  db.Column("id", db.Integer, primary_key=True)
    user_name = db.Column("username", db.String(100))


    #id is automatically created as it is the primary key
    def __init__(self, user_name):
        """Initialises a new user"""

        self.user_name = user_name


class Message_history(db.Model):
    """ Class that stores the user's usernames"""

    __bind_key__ = 'messages'
    id =  db.Column("id", db.Integer, primary_key=True)
    message = db.Column("messages", db.String(100))


    #id is automatically created as it is the primary key
    def __init__(self, message):
        """Initialises a new message"""

        self.message = message




#creating the routes
@app.route('/login')
def login_form():
    """returns the login page """

    return render_template('login.html')


@app.route('/chat-page', methods=["POST", "GET"])
def chat_page():
    """Adds new users to the db, checks if existing users are in teh db, and redirects all
    these usersto the chatting page"""

    if request.method == "POST":
        username = request.form.get("user_name")

        session["user"] = username
        new_user = Users(user_name=username)

        #checking if the user is in the database. There will only be one user with
        #that name so hence why we are only interested in grabbing the first entry of the db
        found_user = Users.query.filter_by(user_name=username).first()
        if found_user:
            flash("username already exists, please pick another one")
            return redirect(url_for("login_form"))

        else:
            #push user to database:
            try:
                db.session.add(new_user)
                db.session.commit()
                return render_template('chat-page.html', Uname=username)
            except:
                return "there was an error adding the user"

        #request method = GET
    else:
        if "user" in session:
            flash("already logged in")
            return render_template("chat-page-html", Uname= session["user"])

        else:
            flash("You are not logged in!")
            return render_template("login.html")


@app.route("/logout")
def logout():
    """Logs out users from the chatpage and deletes them from the database"""

    if "user" in session:
        username = session.pop("user")
        #deleting the user from the database:
        delete_user = Users.query.filter_by(user_name=username).first_or_404()
        db.session.delete(delete_user)
        db.session.commit()
        flash("You have been logged out!")
    return redirect(url_for("login_form"))


@app.route("/view")
def view():
    """Displays the list of users that are logged into the database"""

    return render_template("views.html", values=Users.query.all())


@app.route("/messages")
def view_massages():
    """Displays the list of users that are logged into the database"""

    return render_template("messages.html", items=Message_history.query.all())


@app.route("/delete")
def delete():
    """A temporary route that clears the database whilst I work on fixing the session bug."""

    Users.query.delete()
    db.session.commit()



@socketio.on("event")
def connect(sid, session):
    username = session["user"]

    socketio.save_session(sid, {'username': username})


@socketio.on("event")
def disconnect(sid):
    if "user" in session:
        username = session.pop("user")
        #deleting the user from the database:
        delete_user = Users.query.filter_by(user_name=username).first_or_404()
        db.session.delete(delete_user)
        db.session.commit()
        send(f'{username }disconnected ', broadcast=True)


@socketio.on("join")
def handle_message(msg):
    username = session.get('user')
    emit('status', {'msg':  username + ' has entered the chat.'})


@socketio.on('text')
def text(message):
    username = session.get('user')
    emit('message', {'msg': username + ' : ' + message['msg']}, broadcast= True)




if __name__ == "__main__":
    #this will create the database if it doesn't already exist when we the run the program
    db.create_all()
    socketio.run(app)

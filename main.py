from flask import Flask, render_template, request, flash, session, redirect, url_for
from datetime import timedelta
from flask_session import Session
from flask_socketio import SocketIO, send, emit
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

socketio = SocketIO(app)

            #name of table we will be referencing
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
app.static_folder = "static"
app.secret_key = "My_secret_key"
app.config["SECRET KEY"] = "another_secret!"
app.config["SESSION_TYPE"] = "filesystem"

db = SQLAlchemy(app)
Session(app)
app.permanent_session_lifetime = timedelta(minutes=5)



#creating the database model containing username
class Users(db.Model):
    _id =  db.Column("id", db.Integer, primary_key=True)
    user_name = db.Column("username", db.String(100))

    #id is automatically created as it is the primary key
    def __init__(self, user_name):
        self.user_name = user_name


#creating the routes
@app.route('/login')
def login_form():
    return render_template('login.html')


@app.route('/chat-page', methods=["POST", "GET"])
def chat_page():
    if request.method == "POST":
        username = request.form.get("user_name")
        session["user"] = username
        new_user = Users(user_name=username)
        #push user to database:

        found_user = Users.query.filter_by(user_name=username).first()
        if found_user:
            session["user"] = found_user.user_name

        else:
            try:
                db.session.add(new_user)
                db.session.commit()
                flash("login successful")
                return render_template('chat-page.html', Uname=username)
            except:
                return "there was an error adding the user"
        #request method = GET
    else:
        if "user" in session:
            flash("already logged in")
            return render_template("chat-page-html", Uname= session["user"])

             #checking if the user is in the database. There will only be one user with
            #that name so hence why we are only interested in grabbing the first entry of the db

        else:
            flash("You are not logged in!")
            return render_template("login.html")

@app.route("/logout")
def logout():
    if "user" in session:
        session.pop("user", None)
        flash("You have been logged out!")
    return render_template("login.html")

@app.route("/view")
def view():
    return render_template("views.html", values=Users.query.all())



#defining the socket functions

# function to send messages to the entire group
@socketio.on("message")
def handle_message(msg):
	print("message: " + msg)
	send(msg, broadcast=True)


if __name__ == "__main__":
    #this will create the database if it doesn't already exist when we the run the program
    db.create_all()
    socketio.run(app)

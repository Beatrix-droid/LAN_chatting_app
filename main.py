
from flask import Flask, render_template, request, flash, session, redirect, url_for
from flask_session import Session
from flask_socketio import SocketIO, send, emit
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
Session(app)
socketio = SocketIO(app)
db = SQLAlchemy(app)

                #name of table we will be referencing
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
app.static_folder = "static"
app.secret_key = "My_secret_key"
app.config["SECRET KEY"] = "another_secret!"
app.config["SESSION_TYPE"] = "filesystem"


#creating the database model containing username
class Users(db.Model):
    _id =  db.Column("id", db.Integer, primary_key=True)
    user_name = db.Column("username", db.String(100))

    #id is automatically created as it is the primary key
    def __init__(self, user_name):
        self.user_name = user_name






#creating the routes
@app.route('/login', methods=["POST", "GET"])
def login_form():

    if request.method == "POST":
        username = request.form.get("user_name")
        session["user"] = username
        return redirect(url_for('chat_page'))
    else:
        if "user" in session:
            username = session["user"]
            flash("already logged in")
            return redirect(url_for('chat_page'))

        return render_template('login.html')



@app.route('/chat-page', methods=["POST", "GET"])
def chat_page():
       if "user" in session:
            username = session["user"]
            return render_template('chat-page.html', Uname=username)
       else:
           return redirect(url_for('login_form'))


@app.route("/logout")
def logout():
	session.pop("user", None)
	flash("You have been logged out!")
	return redirect(url_for('login_form'))


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

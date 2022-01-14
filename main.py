from flask import Flask, render_template, request, flash, session, redirect
from flask_session import Session
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.static_folder = "static"
app.secret_key = "My_secret_key"
app.config["SECRET KEY"] = "another_secret!"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
socketio = SocketIO(app)


@app.route('/')
def login_form():
	return render_template('index.html')


@app.route('/chat-page', methods=["POST"])
def chat_page():
    username = request.form.get("user_name")
    session["user"] = username
    return render_template('chat-page.html', Uname=username)


@app.route("/logout")
def logout():
	session.pop("user", None)
	flash("You have been logged out!")
	return redirect("/")


# function to send messages to the entire group
@socketio.on("message")
def handle_message(msg):
	print("message: " + msg)
	send(msg, broadcast=True)


if __name__ == "__main__":
	socketio.run(app)

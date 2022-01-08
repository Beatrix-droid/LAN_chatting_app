from flask import Flask, render_template, request, flash, session
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.static_folder = "static"
app.secret_key = "My_secret_key"
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
	return render_template("index.html")


# decorator to define a default error handler for SocketIO events
@socketio.on_error_default
def error_handler(e):
	print("An Error has occurred:" + str(e))


# function to send messages to the entire group
@socketio.on("message")
def handle_message(message):
	send(message, broadcast=True)


# displayign when a client has connected and disconnected
@socketio.on('connect')
def test_connect():
	emit('my response', {'data': 'Connected'})


@socketio.on('disconnect')
def test_disconnect():
	print('Client disconnected')





if __name__ == "__main__":
	socketio.run(app)

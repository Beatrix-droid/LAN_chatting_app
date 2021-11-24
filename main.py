from flask import Flask, render_template, request, flash, session

app = Flask(__name__)
app.static_folder = "static"
app.secret_key = "My_secret_key"


@app.route('/')
def login_form():
		return render_template('index.html')


@app.route('/chat-page', methods=["POST"])
def chat_page():
	username = request.form.get("user_name")
	session["user"] = username
	#flash(f'Hello {username}You were successfully logged in')
	return render_template('chat-page.html', Uname=username)


@app.route("/logout")
def logout():
	session.pop("user", None)
	flash("You have been logged out!")
	return render_template("index.html")


if __name__ == "__main__":
	app.run()

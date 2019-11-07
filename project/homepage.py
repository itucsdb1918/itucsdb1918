from flask import Flask, render_template, escape, request

app = Flask(__name__)


@app.route("/")
def index():
	user_logged_in = True
	return render_template('homepage.html', user_logged_in=user_logged_in)



if __name__ == '__main__':
		app.run(debug=True)

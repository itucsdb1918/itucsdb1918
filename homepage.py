from flask import Flask, render_template, escape, request

app = Flask(__name__)


@app.route("/")
def index():
	return "itucsdb1918 team's project InterBooks' homepage"




	
if __name__ == "__main__":
		app.run(debug=True)


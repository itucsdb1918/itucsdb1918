from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def homepage():
	#return "itucsdb1918 team's project InterBooks' homepage"
    	return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

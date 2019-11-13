from flask import Flask, render_template
from dbRemote import Database

app = Flask(__name__)

db = Database()

@app.route('/')
def homepage():
	#return "itucsdb1918 team's project InterBooks' homepage"
    	return render_template('index.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup_success')
def signup_success():
    return render_template('signup_success.html')

if __name__ == '__main__':
    app.run(debug=True)

##BACKUP

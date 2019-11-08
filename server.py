#from flask import Flask, render_template, escape, request
#from flask import *

from flask import Flask ,redirect, render_template,flash,url_for


app = Flask(__name__)

status=0

@app.route('/')
@app.route('/Home')
def homepage():
    global status
    return render_template('index.html',Status =status,title = "Home Page")


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

"""
@app.route('/')
def index():
	return render_template('index.html',title = "Home Page")
	#return "itucsdb1918 team's project InterBooks' homepage"
	#return render_template("project/homepage.html")
	#return render_template("project/templates/index.html")


if __name__ == '__main__':
	app.run(debug=True)
"""

#from flask import Flask, render_template
from flask import *
from dbRemote import Database
from forms import signUp, logIn

app = Flask(__name__)

db = Database()

@app.route('/')
def homepage():
    return render_template('index.html')
    #return redirect(url_for("login"))


@app.route('/login',methods = ["GET","POST"])
def login():
    formLogIn = logIn(request.form)
    if request.method == "POST" and formLogIn.validate():
        return redirect(url_for("homepage"))
    else:
        return render_template('login.html', form = formLogIn)


@app.route('/signup',methods = ["GET","POST"])
def signup():
    formSignUp = signUp(request.form)
    if request.method == "POST" and formSignUp.validate():
        return redirect(url_for("homepage"))
    else:
        return render_template('signup.html', form = formSignUp)



@app.route('/signup_success')
def signup_success():
    return render_template('signup_success.html')




if __name__ == '__main__':
    app.run(debug=True)

##BACKUP

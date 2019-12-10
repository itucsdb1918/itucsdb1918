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
    db.userid = 0
    formLogIn = logIn(request.form)
    print("Control1")
    if request.method == "POST" and formLogIn.validate():
        db.userid = db.loginCheck(formLogIn.username.data,formLogIn.password.data)
        if db.userid > 0:
            #flash('You loggin in successfully', 'success')
            return redirect(url_for("homepage"))

    print("Control2")
    return render_template('login.html', form = formLogIn)

    """
    else:
        return render_template('login.html', form = formLogIn)
    """

@app.route('/signup',methods = ["GET","POST"])
def signup():
    formSignUp = signUp(request.form)
    if request.method == "POST" and formSignUp.validate():
        #flash(f'Account created for {formSignUp.username.data}!', 'success')
        db.userid =  db.addNewUser(formSignUp)
        if db.userid > 0:
            return redirect(url_for("homepage"))

    return render_template("signup.html", form = formSignUp)




@app.route('/signup_success')
def signup_success():
    #return render_template('signup_success.html')
    return redirect(url_for("login"))



if __name__ == '__main__':
    app.run(debug=True)

##BACKUP

#from flask import Flask, render_template
from flask import Flask,redirect,render_template,url_for,session,request
from dbRemote import Database
from forms import signUp, logIn

app = Flask(__name__)
app.config['SECRET_KEY'] = '68461841as98d4asg86fd4h86as4as'

db = Database()

@app.route('/')
@app.route('/homepage',methods = ["GET","POST"])
def homepage():
    return render_template('index.html')
    #return redirect(url_for("login"))


@app.route('/login',methods = ["GET","POST"])
def login():
    db.userid = 0
    formLogIn = logIn()

    if request.method == "POST" and formLogIn.validate_on_submit():
        db.userid = db.loginCheck(formLogIn.username.data,formLogIn.password.data)
        if db.userid > 0:
            #flash('You loggin in successfully', 'success')
            return redirect(url_for("homepage"))


    return render_template('login.html', form = formLogIn)


@app.route('/signup',methods = ["GET","POST"])
def signup():
    formSignUp = signUp()
    if request.method == "POST" and formSignUp.validate_on_submit():
        #flash(f'Account created for {formSignUp.username.data}!', 'success')
        db.userid =  db.addNewUser(formSignUp)
        if db.userid > 0:
            return redirect(url_for("homepage"))

    return render_template("signup.html", form = formSignUp)


@app.route('/signup_success')
def signup_success():
    #return render_template('signup_success.html')
    return redirect(url_for("login"))


@app.route('/profile',methods = ["GET","POST"])
def profile():
    uid = db.userid
    profile = db.profile(uid)
    return render_template('profile.html', Status=db.userid, title = "Profile", profile=profile)


if __name__ == '__main__':
    app.run(debug=True)



##BACKUP

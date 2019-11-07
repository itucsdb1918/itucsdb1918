from flask import Flask, redirect, render_template, flash, url_for
from forms import RegistrationForm, LoginForm

app = Flask(__name__)


status = 0


@app.route('/')
def homepage():
    global status
    return render_template('index.html', Status=status, title="Home Page")
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

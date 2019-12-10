from wtforms import Form,StringField, PasswordField, SubmitField, BooleanField, validators
from wtforms.validators import DataRequired, Length, Email, EqualTo


class signUp(Form):
    username = StringField(u'User Name', validators=[validators.input_required(),validators.Length(min = 2, max = 20)])
    password = PasswordField("Password:",validators=[
        validators.DataRequired(message = "Please determine a password"),
        validators.EqualTo(fieldname = "confirm",message = "Passwords are not matched!")
    ])
    confirm = PasswordField("Valid Password")
    firstname  = StringField(u'First Name', validators=[validators.input_required(),validators.Length(min = 2)])
    lastname  = StringField(u'Last Name', validators=[validators.input_required(),validators.Length(min = 2)])
    email = StringField(u'E-mail', validators=[validators.input_required(),validators.Email(message = "Please enter a valid e-mail address!")])
    schoolname = StringField(u'School Name', validators=[validators.input_required(),validators.Length(min = 2)])
    campusname = StringField(u'Campus Name', validators=[validators.input_required(),validators.Length(min = 2)])
    submit = SubmitField('Sign Up')

class logIn(Form):
    username = StringField(u'User Name', validators=[validators.input_required()])
    password = PasswordField("Password:",validators=[validators.DataRequired()])
    submit = SubmitField('Log In')

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, RadioField, validators
from wtforms.validators import DataRequired, Length, Email, EqualTo



class signUp(FlaskForm):
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

class updateProfileForm(FlaskForm):
    username = StringField(u'User Name', validators=[validators.input_required(),validators.Length(min = 2, max = 20)])
    firstname  = StringField(u'First Name', validators=[validators.input_required()])
    lastname  = StringField(u'Last Name', validators=[validators.input_required()])
    email = StringField(u'E-mail', validators=[validators.input_required(),validators.Email(message = "Please enter a valid e-mail address!")])
    schoolname = StringField(u'School Name', validators=[validators.input_required()])
    campusname = StringField(u'Campus Name', validators=[validators.input_required()])


class logIn(FlaskForm):
    username = StringField(u'User Name', validators=[validators.input_required()])
    password = PasswordField("Password:",validators=[validators.DataRequired()])
    submit = SubmitField('Log In')


class updateSchoolForm(FlaskForm):
    schoolid  = StringField(u'School ID that you want to update', validators=[validators.input_required()])
    schoolname  = StringField(u'School Name', validators=[validators.input_required()])
    schooltype  = StringField(u'School Type', validators=[validators.input_required()])
    schoolcountry = StringField(u'School Country', validators=[validators.input_required()])
    schoolcity = StringField(u'School City', validators=[validators.input_required()])
    schoolphonenumber = StringField(u'School Phone Number', validators=[validators.input_required()])

class newSchoolForm(FlaskForm):
    schoolname  = StringField(u'School Name', validators=[validators.input_required()])
    schooltype  = StringField(u'School Type', validators=[validators.input_required()])
    schoolcountry = StringField(u'School Country', validators=[validators.input_required()])
    schoolcity = StringField(u'School City', validators=[validators.input_required()])
    schoolphonenumber = StringField(u'School Phone Number', validators=[validators.input_required()])

class rmSchoolForm(FlaskForm):
    schoolname  = StringField(u'School Name that you want to delete', validators=[validators.input_required()])

class UpdateBookForm(FlaskForm):
    bookId = StringField('Book ID', validators=[validators.input_required()])
    oldBookName = StringField('Old Book Name', validators=[validators.input_required()])
    bookName = StringField('Book Name', validators=[validators.input_required()])
    bookWriter = StringField('Author', validators=[validators.input_required()])
    pages = StringField('Number of Pages', validators=[validators.input_required()])
    publisher = StringField('Publisher', validators=[validators.input_required()])
    pressYear = StringField('Press Year', validators=[validators.input_required()])
    bookType = RadioField('Book Type', choices=[('Normal','Normal sized book'),('Mini','Mini book')], validators=[validators.input_required()])


class AddBookToWishlist(FlaskForm):
    bookName = StringField('Book Name', validators=[validators.input_required()])
    bookWriter = StringField('Author', validators=[validators.input_required()])
    pages = StringField('Number of Pages', validators=[validators.input_required()])
    publisher = StringField('Publisher', validators=[validators.input_required()])
    pressYear = StringField('Press Year', validators=[validators.input_required()])
    bookType = RadioField('Book Type', choices=[('Normal','Normal sized book'),('Mini','Mini book')], validators=[validators.input_required()])
    addBook = SubmitField('Add to Wishlist')



class AddBookToAvailableBooksList(FlaskForm):
    bookName = StringField('Book Name', validators=[validators.input_required()])
    author = StringField('Author', validators=[validators.input_required()])
    pages = StringField('Total Pages', validators=[validators.input_required()])
    publisher = StringField('Publisher', validators=[validators.input_required()])
    pressyear = StringField('Press Year', validators=[validators.input_required()])
    bookType = RadioField('Book Type', choices=[('Normal','Normal sized book'),('Mini','Mini book')], validators=[validators.input_required()])
    additionalInfo = TextAreaField('Anything you want to add')
    addBook = SubmitField('Add to List')



class UpdateAvailableBookForm(FlaskForm):
    oldBookName = StringField('Book Name', validators=[validators.input_required()])
    oldAuthor = StringField('Author', validators=[validators.input_required()])
    bookName = StringField('Book Name', validators=[validators.input_required()])
    author = StringField('Author', validators=[validators.input_required()])
    pages = StringField('Total Pages', validators=[validators.input_required()])
    publisher = StringField('Publisher', validators=[validators.input_required()])
    pressyear = StringField('Press Year', validators=[validators.input_required()])
    bookType = RadioField('Book Type', choices=[('Normal','Normal sized book'),('Mini','Mini book')], validators=[validators.input_required()])
    additionalInfo = TextAreaField('Anything you want to add')
    addBook = SubmitField('Add to List')


class SendMessageForm(FlaskForm):
    receiverName = StringField('Receiver name', validators=[validators.input_required()])
    receiverSurname = StringField('Receiver surname', validators=[validators.input_required()])
    topic = StringField('Topic', validators=[validators.input_required()])
    message = TextAreaField('Message', validators=[validators.input_required()])
    priority = StringField('Priority', validators=[validators.input_required()])



class UpdateMessageForm(FlaskForm):
    messageId = StringField('Message ID', validators=[validators.input_required()])
    topic = StringField('Topic', validators=[validators.input_required()])
    message = TextAreaField('Message', validators=[validators.input_required()])
    priority = StringField('Priority', validators=[validators.input_required()])

class InterchangeUserInfoForm(FlaskForm):
    name = StringField('Name', validators=[validators.input_required()])
    surname = StringField('Surname', validators=[validators.input_required()])

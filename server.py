#from flask import Flask, render_template
from flask import Flask,redirect,render_template,url_for,session,request,flash
from dbRemote import Database
from forms import signUp, logIn, AddBookToWishlist
from model.user import User

app = Flask(__name__)
app.config['SECRET_KEY'] = '68461841as98d4asg86fd4h86as4as'

db = Database()
user = User()

@app.route('/')
@app.route('/homepage',methods = ["GET","POST"])
def homepage():
    return render_template('index.html')
    #return redirect(url_for("login"))


@app.route('/login',methods = ["GET","POST"])
def login():
    db.userid = 0
    # Create a form object
    formLogIn = logIn()
    #if request.method == "POST" and formLogIn.validate_on_submit():
    if request.method == "POST":
        # Get user id from database after successful login operation
        db.userid = db.loginCheck(formLogIn.username.data,formLogIn.password.data)[0]
        user.setId(db.userid)

        # Get User's profile informations and save it into user object to use it everywhere later
        profile = db.getProfileInformations(db.userid)
        print('PROFILE OBJECT: {}'.format(profile))
        user.setUsername(profile['username'])
        user.setFirstname(profile['firstname'])
        user.setLastname(profile['lastname'])
        user.setEmail(profile['email'])
        user.setPassword(profile['password'])
        user.setSchoolName(profile['schoolname'])
        user.setCampusName(profile['campusname'])
        user.setWishlistId(profile['wishlistid'])

        # If there is an ID returned, then navigate user to the homepage
        if db.userid > 0:
            return redirect(url_for("homepage"))


    return render_template('login.html', form = formLogIn)


@app.route('/signup',methods = ["GET","POST"])
def signup():
    formSignUp = signUp()
    if request.method == "POST":
    #if request.method == "POST" and formSignUp.validate_on_submit():
        db.userid =  db.addNewUser(formSignUp)
        if db.userid > 0:
            return redirect(url_for("homepage"))# Go to login after signup

    return render_template("signup.html", form = formSignUp)


@app.route('/signup_success')
def signup_success():
    #return render_template('signup_success.html')
    return redirect(url_for("login"))


@app.route('/profile',methods = ["GET","POST"])
def profile():
    uid = db.userid
    profile = db.getProfileInformations(uid)
    return render_template('profile.html', Status=db.userid, title = "Profile", profile=profile)


@app.route('/wishlist',methods = ["GET","POST"])
def wishlist():
    # Get wishlistId from user object
    wid = user.getWishlistId()

    formWishlist = AddBookToWishlist()

    if request.method == "POST":
        if request.form["btn"] == "w0" : #REMOVE FROM WISHLIST
            wl = db.rmWishlist(wid)
            return render_template('wishlist.html', Status=db.wishlistid, title = "Wishlist", wl=wl, wishlist=wishlist, shape = len(wl), form = formWishlist)

        elif  request.form["btn"] == "p0" : # SHOW WISHLIST
            wl = db.getWishlist(wid)
            wishlist = []
            for item in wl:
                wishlist.append(item)
            return render_template('wishlist.html', Status=db.wishlistid, title = "Wishlist", wl=wl, wishlist=wishlist, shape = len(wl), form = formWishlist)

        elif  request.form["btn"] == "add" :
            wl = db.getWishlist(wid)
            bookName = formWishlist.bookName.data
            bookWriter = formWishlist.bookWriter.data
            bookPages = formWishlist.pages.data

            newBook = [bookName, bookWriter, bookPages]
            wishlist = []
            for item in wl:
                wishlist.append(item)

            #book1984 = ["1984", "George Orwell"]
            #db.isBookExist(book1984)

            if not db.isBookExist(newBook):
                # Add book into the book_info_list table
                newBookId = db.insertBookToBookInfoList(name=newBook[0], author=newBook[1], pages=int(newBook[2]))

                # Also add book into the wish_list table
                db.insertBookToWishlist(user.getWishlistId(), newBookId)

                # Add book to the wishlist
                wishlist.append(newBook)

            return render_template('wishlist.html', Status=db.wishlistid, title = "Wishlist", wl=wl,wishlist=wishlist, shape = len(wl), form = formWishlist)


    wl = db.getWishlist(wid)
    return render_template('wishlist.html', Status=db.wishlistid, title = "Wishlist", wl=wl, shape = len(wl))




if __name__ == '__main__':
    app.run(debug=True)



##BACKUP

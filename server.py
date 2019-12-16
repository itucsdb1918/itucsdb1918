#from flask import Flask, render_template
from flask import Flask,redirect,render_template,url_for,session,request,flash
from dbRemote import Database
from forms import signUp, logIn, AddBookToWishlist, AddBookToAvailableBooksList,updateSchoolForm,rmSchoolForm,newSchoolForm
from model.user import User

app = Flask(__name__)
app.config['SECRET_KEY'] = '68461841as98d4asg86fd4h86as4as'

db = Database()

@app.route('/')
@app.route('/homepage',methods = ["GET","POST"])
def homepage():
    ielist = db.getInterchangeEventList()
    #print("IELIST : {}".format(ielist))

    if db.userid > 0:
        return render_template('index.html', ielist = ielist)

    else:
        flash("Please log in to see interchange event list!",category="message")
        return render_template('index.html')


@app.route('/flow',methods = ["GET","POST"])
def flow():
    ielist = db.getInterchangeEventList()
    flowlist = db.getMyFlow(db.userid)

    return render_template('flow.html', ielist = ielist, lendered = flowlist[0], borrowed = flowlist[1])



@app.route('/login',methods = ["GET","POST"])
def login():
    db.userid = 0
    # Create a form object
    formLogIn = logIn()
    #if request.method == "POST" and formLogIn.validate_on_submit():
    if request.method == "POST":
        # Get user id from database after successful login operation
        db.userid = db.loginCheck(formLogIn.username.data,formLogIn.password.data)[0]


        # Get current user
        currentUser = db.getCurrentUser(db.userid)
        #print('CURRENT USER: {}'.format(currentUser.getUsername()))


        db.wishlistid = currentUser.getWishlistId()
        #print('WISHLIST ID: {}'.format(db.wishlistid))

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
    updateSchool= updateSchoolForm()
    rmform = rmSchoolForm()
    newschool = newSchoolForm()
    schoollist = db.getSchoolInfo()

    if db.userid is 0 or db.userid is None:
         return redirect(url_for("login"))

    if db.userid is 1:
        schoollist = db.getSchoolInfo()

    currentUser = db.getCurrentUser(db.userid)
    db.userid = currentUser.getId()
    print("PROFILE UID: {}".format(db.userid))

    # DELETE BUTTON AREA
    if request.method == "POST":
        if request.form["btn"] == "d0" : #REMOVE FROM WISHLIST
            db.userid = db.rmCurrentUser(db.userid)

        if request.form["btn"] == "newschool":
            db.addNewSchool(newschool)
            if db.userid is 1:
                schoollist = db.getSchoolInfo()
                profile = db.getProfileInformations(db.userid)
                return render_template('profile.html', Status=db.userid, title = "Profile", profile=profile, schoollist = schoollist, form = updateSchool, rmform = rmform,newschool = newschool,uid = db.userid)

        if request.form["btn"] == "removeID":
            db.rmSchoolInfo(rmform)
            if db.userid is 1:
                schoollist = db.getSchoolInfo()
                profile = db.getProfileInformations(db.userid)
                return render_template('profile.html', Status=db.userid, title = "Profile", profile=profile, schoollist = schoollist, form = updateSchool, rmform = rmform,newschool = newschool,uid = db.userid)

        if request.form["btn"] == "updateID":
            db.updateSchoolInfo(updateSchool)
            if db.userid is 1:
                schoollist = db.getSchoolInfo()
                profile = db.getProfileInformations(db.userid)
                return render_template('profile.html', Status=db.userid, title = "Profile", profile=profile, schoollist = schoollist, form = updateSchool, rmform = rmform,newschool = newschool,uid = db.userid)

    profile = db.getProfileInformations(db.userid)

    return render_template('profile.html', Status=db.userid, title = "Profile", profile=profile, schoollist = schoollist, form = updateSchool, rmform = rmform,newschool = newschool,uid = db.userid)






@app.route('/wishlist',methods = ["GET","POST"])
def wishlist():
    currentUser = db.getCurrentUser(db.userid)
    # Get wishlistId from user object
    wid = currentUser.getWishlistId()
    print('INSIDE wishlist func: wid={}'.format(wid))

    formWishlist = AddBookToWishlist()

    if request.method == "POST":
        bookname = request.form.get("bookname")
        author = request.form.get("author")
        pages = request.form.get("pages")


        if request.form["btn"] == "removeValue" : #REMOVE FROM WISHLIST
            #wl = db.rmWishlist(wid)
            #print('REMOVE BOOK NAME: {}'.format(request.form['bookname']))
            print('BOOK NAME: {} , AUTHOR: {}, PAGES: {}'.format(bookname, author, pages))
            book = [bookname, author, 0]
            bookId = db.getBookId(book)
            print('BOOK ID IS {}'.format(bookId))
            db.deleteBookFromWishlist(db.wishlistid, bookId)

            wl = db.getWishlist(wid)
            wishlist = []
            for item in wl:
                wishlist.append(item)
            return render_template('wishlist.html', Status=db.wishlistid, title = "Wishlist", wl=wl, wishlist=wishlist, shape = len(wl), form = formWishlist)

        elif  request.form["btn"] == "p0" : # SHOW WISHLIST
            wl = db.getWishlist(wid)
            wishlist = []
            for item in wl:
                wishlist.append(item)
            return render_template('wishlist.html', Status=db.wishlistid, title = "Wishlist", wl=wl, wishlist=wishlist, shape = len(wl), form = formWishlist)

        elif  request.form["btn"] == "available" : # SHOW WISHLIST
            availableList = []
            #wl = db.getWishlist(wid)
            #wishlist = []
            #for item in wl:
            #    wishlist.append(item)
            return render_template('availablebooks.html', availableList=availableList)


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
                db.insertBookToWishlist(currentUser.getWishlistId(), newBookId)

                # Add book to the wishlist
                wishlist.append(newBook)

            return render_template('wishlist.html', Status=db.wishlistid, title = "Wishlist", wl=wl,wishlist=wishlist, shape = len(wl), form = formWishlist)


    wl = db.getWishlist(wid)
    return render_template('wishlist.html', Status=db.wishlistid, title = "Wishlist", wl=wl, shape = len(wl), form = formWishlist)
    # TODO: ADD wishlist parameter to render_template function

@app.route('/availablebooks',methods = ["GET","POST"])
def availablebooks():
    # FILL AVAILABLE LIST WITH CURRENT ITEMS AT DB
    availableList = []
    dbAvailableList = db.getAvailableBookList(db.userid)
    for item in dbAvailableList:
        availableList.append(item)

    formAvailableBooks = AddBookToAvailableBooksList()

    # FILL AVAILABLE LIST USING DB METHOD HERE


    if  request.form["btn"] == "addAvailable" :
        userId = db.userid
        bookname = formAvailableBooks.bookName.data
        author = formAvailableBooks.author.data
        totalpages = formAvailableBooks.pages.data
        publisher = formAvailableBooks.publisher.data
        pressyear = formAvailableBooks.pressyear.data
        booktype = formAvailableBooks.bookType.data
        additionalinfo = formAvailableBooks.additionalInfo.data

        newBook = [bookname, author, int(totalpages), publisher, booktype, int(pressyear), additionalinfo]

        if not db.isBookExistInAvailableBookList(bookname, author):
            # Also add book into the available_book_list table
            db.insertBookToAvailableBookList(userId, newBook)
            # Add new book to the end of available list
            availableList.append(newBook)

        #Clear form
        formAvailableBooks.bookName.data = ""
        formAvailableBooks.author.data = ""
        formAvailableBooks.pages.data = ""
        formAvailableBooks.publisher.data = ""
        formAvailableBooks.pressyear.data = ""
        formAvailableBooks.bookType.data = ""
        formAvailableBooks.additionalInfo.data = ""


        return render_template('availablebooks.html', form=formAvailableBooks, availableList=availableList)


    return render_template('availablebooks.html', form=formAvailableBooks, availableList=availableList)


if __name__ == '__main__':
    app.run(debug=True)



##BACKUP

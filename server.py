#from flask import Flask, render_template
from flask import Flask,redirect,render_template,url_for,session,request,flash
from dbRemote import Database
from forms import signUp, logIn, AddBookToWishlist, AddBookToAvailableBooksList,UpdateAvailableBookForm,SendMessageForm, UpdateMessageForm, updateSchoolForm,rmSchoolForm,newSchoolForm,updateProfileForm,UpdateBookForm,InterchangeUserInfoForm
from model.user import User

app = Flask(__name__)
app.config['SECRET_KEY'] = '68461841as98d4asg86fd4h86as4as'

db = Database()

@app.route('/')
@app.route('/homepage',methods = ["GET","POST"])
def homepage():
    userId = db.userid

    """if session['userId'] is not None:
        userId = session['userId']

    if userId > 0:
        allAvailableBooks = db.getAllAvailableBooks()
        userId = session['userId']

        # SET USER'S FULL NAME AT THE FIRST INDEX WHICH CONTAINS ID CURRENTLY
        for item in allAvailableBooks:
            user = db.getProfileInformations(userid = item[0])
            userName = user[3]
            userSurname = user[4]
            fullname = userName + ' ' +userSurname
            item[0] = fullname

        return render_template('index.html', allAvailableBooks = allAvailableBooks)

    else:
        flash("Please log in to see interchange event list!",category="message")
        return render_template('index.html')"""

    if db.userid > 0:
        allAvailableBooks = db.getAllAvailableBooks()
        userId = db.userid

        # SET USER'S FULL NAME AT THE FIRST INDEX WHICH CONTAINS ID CURRENTLY
        for item in allAvailableBooks:
            user = db.getProfileInformations(userid = item[0])
            userName = user[3]
            userSurname = user[4]
            fullname = userName + ' ' +userSurname
            item[0] = fullname

        return render_template('index.html', allAvailableBooks = allAvailableBooks)

    else:
        flash("Please log in to see interchange event list!",category="message")
        return render_template('index.html')


@app.route('/flow',methods = ["GET","POST"])
def flow():
    ielist = db.getInterchangeEventList()
    flowlist = db.getMyFlow(db.userid)

    if request.method == "POST":
        db.rmInterchangeEventList(request.form['deleteFlow'])
        ielist = db.getInterchangeEventList()
        flowlist = db.getMyFlow(db.userid)
        return render_template('flow.html', ielist = ielist, lendered = flowlist[0], borrowed = flowlist[1])

    return render_template('flow.html', ielist = ielist, lendered = flowlist[0], borrowed = flowlist[1])


@app.route('/login',methods = ["GET","POST"])
def login():
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
        """session['wishlistId'] = db.wishlistid"""
        #print('WISHLIST ID: {}'.format(db.wishlistid))

        # If there is an ID returned, then navigate user to the homepage
        if db.userid > 0:
            """session['userId'] = db.userid"""
            return redirect(url_for("homepage"))


    return render_template('login.html', form = formLogIn)


@app.route('/signup',methods = ["GET","POST"])
def signup():
    formSignUp = signUp()
    if request.method == "POST":
    #if request.method == "POST" and formSignUp.validate_on_submit():
        db.userid =  db.addNewUser(formSignUp)
        if db.userid > 0:
            """session['userId'] = db.userid"""
            return redirect(url_for("homepage"))# Go to login after signup

    return render_template("signup.html", form = formSignUp)


@app.route('/signup_success')
def signup_success():
    #return render_template('signup_success.html')
    return redirect(url_for("login"))


@app.route('/profile',methods = ["GET","POST"])
def profile():

    """userId = session['userId']"""
    userId = db.userid
    if userId is 0 or userId is None:
        return redirect(url_for("login"))


    updateSchool= updateSchoolForm()
    rmform = rmSchoolForm()
    newschool = newSchoolForm()
    updateprof = updateProfileForm()
    schoollist = db.getSchoolInfo()
    userlist = db.getUsers()

    if db.userid is 0 or db.userid is None:
         return redirect(url_for("login"))

    if db.userid is 1:
        schoollist = db.getSchoolInfo()

    currentUser = db.getCurrentUser(db.userid)
    db.userid = currentUser.getId()

    print("PROFILE UID: {}".format(userId))

    # DELETE BUTTON AREA
    if request.method == "POST":
        if request.form["btn"] == "d0" : #REMOVE FROM WISHLIST
            db.userid = db.rmCurrentUser(db.userid) # returns zero
            """session['userId'] = db.userid # set to zero"""

        if request.form["btn"] == "newschool":
            db.addNewSchool(newschool)
            if db.userid is 1:
                schoollist = db.getSchoolInfo()
                profile = db.getProfileInformations(db.userid)
                #profile = db.getProfileInformations(session['userId'])
                return render_template('profile.html', Status=db.userid, title = "Profile", profile=profile, schoollist = schoollist, form = updateSchool, rmform = rmform,newschool = newschool,uid = db.userid,userlist = userlist,updateprof = updateprof)

        if request.form["btn"] == "removeID":
            db.rmSchoolInfo(rmform)
            if db.userid is 1:
                schoollist = db.getSchoolInfo()
                profile = db.getProfileInformations(db.userid)
                #profile = db.getProfileInformations(session['userId'])
                return render_template('profile.html', Status=db.userid, title = "Profile", profile=profile, schoollist = schoollist, form = updateSchool, rmform = rmform,newschool = newschool,uid = db.userid,userlist = userlist,updateprof = updateprof)

        if request.form["btn"] == "updateID":
            db.updateSchoolInfo(updateSchool)
            if db.userid is 1:
                schoollist = db.getSchoolInfo()
                profile = db.getProfileInformations(db.userid)
                #profile = db.getProfileInformations(session['userId'])
                return render_template('profile.html', Status=db.userid, title = "Profile", profile=profile, schoollist = schoollist, form = updateSchool, rmform = rmform,newschool = newschool,uid = db.userid,userlist = userlist, updateprof = updateprof)


        if request.form["btn"] == "updateProfile":
            print("00000000000000000000000000000000000000000000000000")
            db.updateProfile(updateprof,db.userid)
            #db.updateProfile(updateprof,session['userId'])
            if db.userid is 1:
                schoollist = db.getSchoolInfo()
                profile = db.getProfileInformations(db.userid)
                #profile = db.getProfileInformations(session['userId'])
                return render_template('profile.html', Status=db.userid, title = "Profile", profile=profile, schoollist = schoollist, form = updateSchool, rmform = rmform,newschool = newschool,uid = db.userid,userlist = userlist, updateprof = updateprof)

    profile = db.getProfileInformations(db.userid)
    #profile = db.getProfileInformations(session['userId'])
    return render_template('profile.html', Status=db.userid, title = "Profile", profile=profile, schoollist = schoollist, form = updateSchool, rmform = rmform,newschool = newschool,uid = db.userid,userlist = userlist, updateprof = updateprof)



@app.route('/books',methods = ["GET","POST"])
def books():
    booklist = db.getBookList()
    updBookForm = UpdateBookForm()

    print("BOOKS: {}".format(booklist))

    if request.method == "POST":
        print(request.form['btn'])

        if request.form['btn'] == 'updateBook':
            db.updateBook(updBookForm)
            booklist = db.getBookList()
            return render_template('books.html', booklist = booklist, updBookForm = updBookForm)
        # IT IS DELETE
        else:
            #db.rmBook(request.form['deleteBook'])
            db.rmBook(request.form['btn'])
            booklist = db.getBookList()
            return render_template('books.html', booklist = booklist, updBookForm = updBookForm)

    return render_template('books.html', booklist = booklist, updBookForm = updBookForm)





@app.route('/wishlist',methods = ["GET","POST"])
def wishlist():
    currentUser = db.getCurrentUser(db.userid)
    # Get wishlistId from user object
    """wishlistId = session['wishlistId']"""
    wishlistId = db.wishlistid

    #print('INSIDE wishlist func: wid={}'.format(wishlistId))

    wl = db.getWishlist(wishlistId)
    wishlist = []
    for item in wl:
        wishlist.append(item)

    formWishlist = AddBookToWishlist()
    userInfoForm = InterchangeUserInfoForm()

    if request.method == "POST":
        bookname = request.form.get("bookname")
        author = request.form.get("author")
        pages = request.form.get("pages")
        publisher = request.form.get("publisher")
        type = request.form.get("type")
        year = request.form.get("year")



        if request.form["btn"] == "removeValue" : #REMOVE FROM WISHLIST (BY USING INTERCHANGED BUTTON)
            #wl = db.rmWishlist(wishlistId)
            #print('REMOVE BOOK NAME: {}'.format(request.form['bookname']))
            print('BOOK NAME: {} , AUTHOR: {}, PAGES: {}'.format(bookname, author, pages))
            book = [bookname, author, 0]
            bookId = db.getBookId(book)
            print('BOOK ID IS {}'.format(bookId))
            db.deleteBookFromWishlist(wishlistId, bookId)

            wishlist = db.getWishlist(wishlistId)

            # Add this operation to interchange event list
            borrowerName = userInfoForm.name.data
            borrowerSurname = userInfoForm.surname.data

            borrowerId = db.getUserIdByNameAndSurname(borrowerName, borrowerSurname)
            #If user does not exist, then return
            if borrowerId is None:
                return render_template('wishlist.html', wishlist=wishlist, form = formWishlist, userForm=userInfoForm)

            lenderId = db.userid

            newEvent = [lenderId, borrowerId, bookname, author, int(pages), publisher]

            #print('LID:{}, BID:{}, name:{}, author:{}, pages:{}, publisher:{}'.format(lenderId, borrowerId, bookname, author, int(pages), publisher))
            db.insertEventToInterchangeEventList(newEvent)

            return render_template('wishlist.html', wishlist=wishlist, form = formWishlist, userForm=userInfoForm)

        elif  request.form["btn"] == "p0" : # SHOW WISHLIST
            wl = db.getWishlist(wishlistId)
            wishlist = []
            for item in wl:
                wishlist.append(item)
            return render_template('wishlist.html', wishlist=wishlist, form = formWishlist, userForm=userInfoForm)

        elif  request.form["btn"] == "available" : # SHOW AVAILABLE LIST
            availableList = []
            return render_template('availablebooks.html', availableList=availableList)


        elif  request.form["btn"] == "add" :
            bookName = formWishlist.bookName.data
            bookWriter = formWishlist.bookWriter.data
            bookPages = formWishlist.pages.data
            publisher = formWishlist.publisher.data
            bookType = formWishlist.bookType.data
            pressYear = formWishlist.pressYear.data

            newBook = [bookName, bookWriter, bookPages, publisher, bookType, pressYear]

            #book1984 = ["1984", "George Orwell"]
            #db.isBookExist(book1984)

            if not db.isBookExist(newBook):
                # Add book into the book_info_list table
                newBookId = db.insertBookToBookInfoList(name=newBook[0], author=newBook[1], pages=int(newBook[2]), publisher = newBook[3], type = newBook[4], year = int(newBook[5]))

                print('Wishlist id is {}, book id is {}'.format(wishlistId, newBookId))
                # Also add book into the wish_list table
                db.insertBookToWishlist(wishlistId, newBookId)

                # Add book to the wishlist
                wishlist = db.getWishlist(wishlistId)

            return render_template('wishlist.html', wishlist=wishlist, form = formWishlist, userForm=userInfoForm)


    wishlist = db.getWishlist(wishlistId)
    return render_template('wishlist.html', wishlist=wishlist, form = formWishlist, userForm=userInfoForm)


@app.route('/availablebooks',methods = ["GET","POST"])
def availablebooks():
    # FILL AVAILABLE LIST WITH CURRENT ITEMS AT DB
    """userId = session['userId']"""
    userId = db.userid
    availableList = []
    dbAvailableList = db.getAvailableBookList(db.userid)
    for item in dbAvailableList:
        availableList.append(item)


    formAvailableBooks = AddBookToAvailableBooksList()
    formUpdateBooks = UpdateAvailableBookForm()

    if request.method == "POST":

        if  request.form["btn"] == "addAvailable" :
            #print('ADD AVAILABLE CALLED')
            bookname = formAvailableBooks.bookName.data
            author = formAvailableBooks.author.data
            totalpages = formAvailableBooks.pages.data
            publisher = formAvailableBooks.publisher.data
            pressyear = formAvailableBooks.pressyear.data
            booktype = formAvailableBooks.bookType.data
            additionalinfo = formAvailableBooks.additionalInfo.data

            newBook = [bookname, author, int(totalpages), publisher, int(pressyear), booktype, additionalinfo]

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


            return render_template('availablebooks.html', form=formAvailableBooks, formUpdateBooks = formUpdateBooks, availableList=availableList)


        # If user clicks the update button, then fill the form with clicked book informations
        elif  request.form["btn"] == "saveAvailable" :
            oldBookName = formUpdateBooks.oldBookName.data
            oldAuthorName = formUpdateBooks.oldAuthor.data
            newBookName = formUpdateBooks.bookName.data
            newAuthorName = formUpdateBooks.author.data
            newPages = formUpdateBooks.pages.data
            newPublisher = formUpdateBooks.publisher.data
            newBookType = formUpdateBooks.bookType.data
            newPressYear = formUpdateBooks.pressyear.data
            newAdditionalInfo = formUpdateBooks.additionalInfo.data

            newBook = [newBookName, newAuthorName, int(newPages), newPublisher, newBookType, int(newPressYear), newAdditionalInfo]

            db.updateBookAtAvailableBookList(userId, oldBookName, oldAuthorName, newBook)

            return render_template('availablebooks.html', form=formAvailableBooks, formUpdateBooks= formUpdateBooks, availableList=availableList)

    return render_template('availablebooks.html', form=formAvailableBooks, formUpdateBooks=formUpdateBooks, availableList=availableList)

@app.route('/messages',methods = ["GET","POST"])
def messages():
    messages = []
    sentMessages = []

    sendMessageForm = SendMessageForm()
    updateMessageForm = UpdateMessageForm()

    messages = db.getIncomingMessagesByUserId(db.userid)
    sentMessages = db.getSentMessagesByUserId(db.userid)

    #testMessage = ["Emre", "Reyhanlioglu", "Test topic", "Test message", "16.12.2019: 16:39", "High", "4"]
    #sentMessages.append(testMessage)

    #testMessage = ["Emre R", "Test topic", "Test message", "16.12.2019: 16:39", "High"]
    #messages.append(testMessage)


    if request.method == "POST":
        if  request.form["btn"] == "sendMessage" :
            receiverName = sendMessageForm.receiverName.data
            receiverSurname = sendMessageForm.receiverSurname.data
            topic = sendMessageForm.topic.data
            message = sendMessageForm.message.data
            priority = sendMessageForm.priority.data

            checkedUserId = db.getUserIdByNameAndSurname(receiverName, receiverSurname)
            if checkedUserId is None:
                print('USER DOES NOT EXIST')
                return render_template('messages.html', messages = messages, sendMessageForm = sendMessageForm, updateMessageForm=updateMessageForm, sentMessages = sentMessages)

            senderId = db.userid
            senderUser = db.getProfileInformations(senderId)
            senderName = senderUser[3]
            senderSurname = senderUser[4]

            receiverId = db.getUserIdByNameAndSurname(receiverName, receiverSurname)

            newMessage = [senderId, receiverId, senderName, senderSurname, topic, message, priority]

            db.insertMessage(newMessage)
            messages = db.getIncomingMessagesByUserId(db.userid)
            sentMessages = db.getSentMessagesByUserId(db.userid)

            return render_template('messages.html', messages = messages, sendMessageForm = sendMessageForm, updateMessageForm=updateMessageForm, sentMessages = sentMessages)

        elif  request.form["btn"] == "updateMessage" :
            #print('UPDATE MESSAGE CALLED')
            messageId = int(updateMessageForm.messageId.data)

            topic = updateMessageForm.topic.data
            message = updateMessageForm.message.data
            priority = updateMessageForm.priority.data

            newMessage = [topic, message, priority]

            db.updateMessageByMessageId(messageId, newMessage)

            #UPDATE UI AFTER EDITING A MESSAGE
            sentMessages = db.getSentMessagesByUserId(db.userid)
            messages = db.getIncomingMessagesByUserId(db.userid)

            return render_template('messages.html', messages = messages, sendMessageForm = sendMessageForm, updateMessageForm=updateMessageForm, sentMessages = sentMessages)

        else:
            deletedMessageId = int(request.form['btn'])
            #print('DELETED MESSAGE ID is {}'.format(deletedMessageId))
            db.deleteMessageById(deletedMessageId)

            messages = db.getIncomingMessagesByUserId(db.userid)

            return render_template('messages.html', messages = messages, sendMessageForm = sendMessageForm, updateMessageForm=updateMessageForm, sentMessages = sentMessages)




    return render_template('messages.html', messages = messages, sendMessageForm = sendMessageForm, updateMessageForm=updateMessageForm, sentMessages = sentMessages)



if __name__ == '__main__':
    app.run(debug=True)



##BACKUP

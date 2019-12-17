import psycopg2
import psycopg2.extras
from model.user import User


class Database:
    def __init__(self, dbname="daj9gh29vue350", user="crcwonmkxgjemv",
                    password="c6326c163f00c313adc58d3edc0e8a15db6fb938b9eb6e4468f1d1c6a13b15e7",
                    host="ec2-46-137-159-254.eu-west-1.compute.amazonaws.com"):
        self.con = psycopg2.connect(database=dbname, user=user, password=password, host=host)
        self.cur = self.con.cursor()
        self.userid = 0
        self.wishlistid = 0

    def getCurrentUser(self,userid):
        queryRes = []
        isDone = False

        # Qery returns null SOMETIMES, while loop solved the problem by BUSY WAITING. It is not an efficient way but it works
        while not isDone:
            with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                query = "SELECT userid, username, email, password, firstname, lastname, schoolid, campusname, wishlistid FROM user_list WHERE userid = {}".format(userid)
                cursor.execute(query)
                res = cursor.fetchone()

                if res is not None:
                    currentUser = User(id=res[0],username=res[1],email=res[2],password=res[3],firstname=res[4],lastname=res[5],schoolid=res[6],campusName=res[7],wishlistId=res[8])
                    isDone = True
                    return currentUser



    def addNewUser(self,form):
        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT email FROM user_list WHERE email = '%s';" %(form.email.data)
            cursor.execute(query)
            queryRes = cursor.fetchone()


        if queryRes is None:
            with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                query = "SELECT schoolid FROM school_list WHERE schoolname = '%s';"%(form.schoolname.data)
                cursor.execute(query)
                sid = cursor.fetchone()

            with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                query = "INSERT INTO user_list (username,password,firstname,lastname,email,schoolid,campusname)VALUES ('%s','%s','%s','%s','%s','%s', '%s');"%(form.username.data,form.password.data,form.firstname.data,form.lastname.data,form.email.data,sid[0],form.campusname.data)
                cursor.execute(query)

            with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                query = "SELECT userid  FROM user_list WHERE email='%s';" %(form.email.data)
                cursor.execute(query)
                queryRes = cursor.fetchone()
                return queryRes[0]

        return 0

    def updateProfile(self,form,uid):
        queryRes = []
        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT schoolid FROM school_list WHERE schoolname = '%s'"%(form.schoolname.data)
            cursor.execute(query)
            queryRes = cursor.fetchone()

        if queryRes is None:
            return 0
        else:
            with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                query = "UPDATE user_list SET username = '%s', firstname = '%s', lastname = '%s', email = '%s', schoolid = '%d' ,campusname = '%s' WHERE userid = '%d';"%(form.username.data,form.firstname.data,form.lastname.data,form.email.data,queryRes[0],form.campusname.data,uid)
                cursor.execute(query)


    def rmCurrentUser(self,userid):

        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "DELETE FROM user_list WHERE userid = {}".format(userid)
            cursor.execute(query)

        return 0

    def getUsers(self):
        queryRes = []
        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT userid,username,firstname,lastname,email,schoolname,campusname,wishlistid FROM user_list JOIN school_list ON (user_list.schoolid = school_list.schoolid)"
            cursor.execute(query)
            queryRes = cursor.fetchall()

        return queryRes

    def loginCheck(self,username,password):
        userid = 0
        queryRes = []

        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT userid, username, password, wishlistid FROM user_list WHERE username='%s' and password = '%s';" %(username,password)
            cursor.execute(query)
            queryRes = cursor.fetchone()

        if queryRes is not None:
            userid = queryRes[0]
            wishlistid = queryRes[3]

        return (userid,wishlistid)


    def getInterchangeEventList(self):
        ielistResult = []

        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT username FROM user_list JOIN interchange_event_list ON (interchange_event_list.lenderid = user_list.userid)"
            cursor.execute(query)
            lenderName = cursor.fetchall()

        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT username FROM user_list JOIN interchange_event_list ON (interchange_event_list.borrowerid = user_list.userid)"
            cursor.execute(query)
            borrowerName = cursor.fetchall()


        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT interchangeid, time, bookname, bookauthor, totalpages FROM interchange_event_list"
            cursor.execute(query)
            ieID = cursor.fetchall()


        for i in range(len(ieID)):
            ielistResult.append([ieID[i][0],ieID[i][1],lenderName[i][0],borrowerName[i][0],ieID[i][2],ieID[i][3],ieID[i][4]])

        return ielistResult

    def rmInterchangeEventList(self,ielid):
        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "DELETE FROM interchange_event_list WHERE interchangeid = {}".format(ielid)
            cursor.execute(query)


    def insertEventToInterchangeEventList(self, newEvent):
        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = """INSERT INTO interchange_event_list
            (lenderid, borrowerid, bookname, bookauthor, totalpages, publisher) VALUES
            ('%d', '%d', '%s','%s', '%d', '%s');""" %(newEvent[0], newEvent[1],newEvent[2],newEvent[3],newEvent[4],newEvent[5])
            cursor.execute(query)




    def getMyFlow(self,userid):
        borrowed = []
        lendered = []

        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT interchangeid, username AS lendername, (SELECT username FROM user_list JOIN interchange_event_list ON (interchange_event_list.borrowerid = user_list.userid) WHERE borrowerid = {} LIMIT 1) as borrowername,  time, bookname, bookauthor, totalpages, publisher FROM interchange_event_list JOIN user_list ON (interchange_event_list.lenderid = user_list.userid) where borrowerid = {} ORDER BY time".format(userid,userid)
            cursor.execute(query)
            borrowed = cursor.fetchall()

        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT interchangeid, username AS borrowername, (SELECT username FROM user_list JOIN interchange_event_list ON (interchange_event_list.lenderid = user_list.userid) WHERE lenderid = {} LIMIT 1) as lendername,  time, bookname, bookauthor, totalpages, publisher FROM interchange_event_list JOIN user_list ON (interchange_event_list.borrowerid = user_list.userid) where lenderid = {} ORDER BY time".format(userid,userid)
            cursor.execute(query)
            lendered = cursor.fetchall()

        return (borrowed,lendered)

    def addNewSchool(self,form):
        queryRes = []
        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT * FROM school_list WHERE schoolname = '%s';"%(form.schoolname.data)
            cursor.execute(query)
            queryRes = cursor.fetchone()


        if queryRes is None:
            with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                query = "INSERT INTO school_list(schoolname,schooltype,schoolcountry,schoolcity,schoolphonenumber) VALUES ('%s','%s','%s','%s','%s');"%(form.schoolname.data,form.schooltype.data,form.schoolcountry.data,form.schoolcity.data,form.schoolphonenumber.data)
                cursor.execute(query)

            with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                query = "SELECT * FROM school_list"
                cursor.execute(query)
                queryRes = cursor.fetchall()


    def getSchoolInfo(self):
        queryRes = []
        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT schoolid, schoolname, schooltype, schoolcountry, schoolcity, schoolphonenumber FROM school_list ORDER BY schoolname"
            cursor.execute(query)
            queryRes = cursor.fetchall()

            #print('Query result {}'.format(queryRes))
        return queryRes


    def rmSchoolInfo(self,form):
        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "DELETE FROM school_list WHERE schoolname = '%s';"%(form.schoolname.data)
            cursor.execute(query)

        print("DELETED")

    def updateSchoolInfo(self,form):
        queryRes = []
        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            #query = "SELECT * FROM school_list WHERE '%s';"%(form.schoolid.data)
            query = "SELECT * FROM school_list WHERE schoolid = {}".format(form.schoolid.data)
            cursor.execute(query)
            queryRes = cursor.fetchone()

        print("SCHOOL FOUND: {}".format(queryRes))

        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "UPDATE school_list SET schoolname = '%s', schooltype = '%s', schoolcountry = '%s', schoolcity = '%s', schoolphonenumber = '%s' WHERE schoolid = '%s';"%(form.schoolname.data,form.schooltype.data,form.schoolcountry.data,form.schoolcity.data,form.schoolphonenumber.data,queryRes[0])
            cursor.execute(query)





    def getProfileInformations(self,userid):
        queryRes = []

        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT userid, username, password, firstname, lastname, email, schoolname, campusname, wishlistid FROM user_list JOIN school_list ON (user_list.schoolid = school_list.schoolid) WHERE userid={}".format(userid)
            cursor.execute(query)
            queryRes = cursor.fetchone()

            print('Query result {}'.format(queryRes))
        return queryRes

    def getWishlist(self,wishlistid):
        queryRes = []
        #print('wishlist id is -> {}'.format(wishlistid))
        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT bookname, bookauthor, totalpages, publisher, booktype, pressyear FROM book_info_list JOIN wish_list ON (book_info_list.bookid = wish_list.bookid) WHERE wishlistid = {}".format(wishlistid)
            cursor.execute(query)
            queryRes = cursor.fetchall()
        #print("QUERY RESULT: {}".format(queryRes))
        return queryRes

    def deleteBookFromWishlist(self, wishlistid, bookid):
        queryRes = []
        queryDel = []

        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "DELETE FROM wish_list WHERE wishlistid = {} AND bookid = {}".format(wishlistid, bookid)
            cursor.execute(query)
            #queryDel = cursor.fetchall()

        print("QUERY DEL RESULT: {}".format(queryDel))

        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT bookname, bookauthor, totalpages FROM book_info_list JOIN wish_list ON (book_info_list.bookid = wish_list.bookid) WHERE wishlistid = {}".format(wishlistid)
            cursor.execute(query)
            queryRes = cursor.fetchall()
        #print("QUERY RESULT: {}".format(queryRes))
        return queryRes

        print("QUERY RESULT: {}".format(queryRes))
        return queryRes

    # This method searchs a book in book_info_list table and returns true if book exist, otherwise returns false
    def isBookExist(self, book):
        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT * FROM book_info_list WHERE bookname = '%s' AND bookauthor = '%s';" %(book[0], book[1])
            cursor.execute(query)
            queryRes = cursor.fetchall()

        print("isBookExist: Query Result is {}".format(queryRes))

        if not queryRes:
            print('Book {} does not exist'.format(book[0]))
            return False
        else:
            print('Book {} found in the list'.format(book[0]))
            return True

    # This method returns book id if exist, otherwise returns -1
    def getBookId(self, book):
        if not self.isBookExist(book):
            print('getBookId: Book {} does not exist'.format(book[0]))
            return -1

        else:
            with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                query = "SELECT bookid FROM book_info_list WHERE bookname = '%s' AND bookauthor = '%s';" %(book[0], book[1])
                cursor.execute(query)
                queryRes = cursor.fetchone()

            print('Book id is {}'.format(queryRes))
            return queryRes[0];


    # This method returns bookId if the bok inserted successfully
    def insertBookToBookInfoList(self, name, author, pages, publisher, type, year):
        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "INSERT INTO book_info_list (bookname, bookauthor, totalpages, publisher, booktype, pressyear) VALUES('%s', '%s', '%d','%s', '%s', '%d');" %(name, author, pages,publisher, type, year)
            cursor.execute(query)
        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT bookid FROM book_info_list WHERE bookname='%s' AND bookauthor='%s' AND totalpages='%d'" %(name, author, pages)
            cursor.execute(query)
            queryRes = cursor.fetchone()
            #print('INSERT BOOK RESULT: {}'.format(queryRes))
            return queryRes[0] # RETURNING THE BOOK ID WHICH IS JUST CREATED


    def insertBookToWishlist(self, wishlistId, bookId):
        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "INSERT INTO wish_list  (wishlistid, bookid) VALUES('%d', '%d');" %(wishlistId, bookId)
            cursor.execute(query)


    def insertBookToAvailableBookList(self, userId, book):
        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = """INSERT INTO available_book_list
            (userid, bookname, bookauthor, totalpages, publisher, pressyear, booktype, additionalinfo) VALUES
            ('%d', '%s', '%s','%d','%s', '%d', '%s', '%s');
            """ %(userId, book[0], book[1], book[2], book[3], book[4], book[5], book[6])
            cursor.execute(query)



    def updateBookAtAvailableBookList(self, userId, oldName, oldAuthor, newBook):
        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = """UPDATE available_book_list SET
            bookname = '%s', bookauthor = '%s', totalpages = '%d', publisher = '%s',
            booktype = '%s', pressyear = '%d', additionalInfo = '%s' WHERE
            userid = '%d' AND bookname = '%s' AND bookauthor = '%s';
            """ %(newBook[0],newBook[1],newBook[2],newBook[3],newBook[4],newBook[5],newBook[6], userId, oldName, oldAuthor)  # book[2], book[3], book[4], book[5], book[6]
            cursor.execute(query)


    def getAllAvailableBooks(self):
        queryRes = []
        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT userid, bookname, bookauthor, totalpages, publisher, pressyear, booktype, additionalinfo FROM available_book_list"
            cursor.execute(query)
            queryRes = cursor.fetchall()
        return queryRes


    def getAvailableBookList(self, userId):
        queryRes = []
        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT bookname, bookauthor, totalpages, publisher, pressyear, booktype, additionalinfo FROM available_book_list WHERE userid = {}".format(userId)
            cursor.execute(query)
            queryRes = cursor.fetchall()
        print("AVAILABLE BOOK RESULT: {}".format(queryRes))
        return queryRes


    def isBookExistInAvailableBookList(self, bookname, author):
        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT * FROM available_book_list WHERE bookname = '%s' AND bookauthor = '%s';" %(bookname, author)
            cursor.execute(query)
            queryRes = cursor.fetchall()

        if not queryRes:
            return False
        else:
            return True

    def insertMessage(self, messageInfo):
        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = """INSERT INTO message_list
            (senderid, receiverid, sendername, sendersurname, topic, message, priority) VALUES
            ('%d', '%d', '%s','%s', '%s', '%s', '%s');
            """ %(messageInfo[0],messageInfo[1],messageInfo[2],messageInfo[3],messageInfo[4],messageInfo[5],messageInfo[6])
            cursor.execute(query)


    def getMessageByMessageId(self, messageId):
        queryRes = []
        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT sendername, sendersurname, topic, message, timestamp, priority, messageid FROM message_list WHERE messageid = '%d'"%(messageId)
            cursor.execute(query)
            queryRes = cursor.fetchall()

        return queryRes



    def updateMessageByMessageId(self, messageId, newMessage):
        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = """UPDATE message_list SET
            topic = '%s', message = '%s', priority = '%s' WHERE
            messageid = '%d';
            """ %(newMessage[0],newMessage[1],newMessage[2], messageId)
            cursor.execute(query)



    def deleteMessageById(self, messageId):
        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "DELETE FROM message_list WHERE messageid = '%d'"%(messageId)
            cursor.execute(query)


    def getIncomingMessagesByUserId(self, userId):
        queryRes = []
        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT sendername, sendersurname, topic, message, timestamp, priority, messageid FROM message_list WHERE receiverid = '%d' ORDER BY timestamp, priority DESC"%(userId)
            cursor.execute(query)
            queryRes = cursor.fetchall()

        print("MESSAGES: {}".format(queryRes))
        return queryRes


    def getSentMessagesByUserId(self, userId):
        queryRes = []
        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT sendername, sendersurname, topic, message, timestamp, priority, messageid FROM message_list WHERE senderid = '%d' ORDER BY timestamp, priority DESC"%(userId)
            cursor.execute(query)
            queryRes = cursor.fetchall()

        print("MESSAGES: {}".format(queryRes))
        return queryRes


    def getUserIdByNameAndSurname(self, name, surname):
        queryRes = []
        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT userid FROM user_list WHERE firstname = '%s' AND lastname = '%s'"%(name, surname)
            cursor.execute(query)
            queryRes = cursor.fetchone()

        if queryRes is None:
            return None

        return queryRes[0]



    # This method returns all the books in book_info_list table
    def getBookList(self):
        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT bookid,bookname, bookauthor, totalpages,publisher, booktype, pressyear FROM book_info_list"
            cursor.execute(query)
            queryRes = cursor.fetchall()
        #print("QUERY RESULT: {}".format(queryRes))
        return queryRes

    def rmBook(self,bookid):
        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "DELETE FROM book_info_list WHERE bookid = {}".format(bookid)
            cursor.execute(query)


    def updateBook(self,form):
        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "UPDATE book_info_list SET bookname = '%s', bookauthor = '%s', totalpages = '%d', publisher = '%s', booktype = '%s', pressyear = '%d' WHERE bookid = '%d' AND bookname = '%s';"%(form.bookName.data,form.bookWriter.data,int(form.pages.data),form.publisher.data,form.bookType.data,int(form.pressYear.data),int(form.bookId.data),form.oldBookName.data)
            cursor.execute(query)

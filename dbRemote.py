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

            """print(form.schoolname.data)
            with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                query = "SELECT schoolid FROM school_list WHERE schoolname = {}".format(form.schoolname.data)
                cursor.execute(query)
                sid = cursor.fetchone()

                print(sid)"""

            with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                query = "INSERT INTO user_list (username,password,firstname,lastname,email,schoolid,campusname)VALUES ('%s','%s','%s','%s','%s','%s', '%s');"%(form.username.data,form.password.data,form.firstname.data,form.lastname.data,form.email.data,1,form.campusname.data)
                cursor.execute(query)

            with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                query = "SELECT userid  FROM user_list WHERE email='%s';" %(form.email.data)
                cursor.execute(query)
                queryRes = cursor.fetchone()
                return queryRes[0]

        return 0

    def rmCurrentUser(self,userid):

        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "DELETE FROM user_list WHERE userid = {}".format(userid)
            cursor.execute(query)

        return 0

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



    def getProfileInformations(self,userid):
        queryRes = []

        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT userid, username, password, firstname, lastname, email, schoolname, campusname, wishlistid FROM user_list WHERE userid={}".format(userid)
            cursor.execute(query)
            queryRes = cursor.fetchone()

            print('Query result {}'.format(queryRes))
        return queryRes

    def getWishlist(self,wishlistid):
        queryRes = []
        print('wishlist id is -> {}'.format(wishlistid))
        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT bookname, bookauthor, totalpages FROM book_info_list JOIN wish_list ON (book_info_list.bookid = wish_list.bookid) WHERE wishlistid = {}".format(wishlistid)
            cursor.execute(query)
            queryRes = cursor.fetchall()
        print("QUERY RESULT: {}".format(queryRes))
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
    def insertBookToBookInfoList(self, name, author, pages):
        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "INSERT INTO book_info_list (bookname, bookauthor, totalpages) VALUES('%s', '%s', '%d');" %(name, author, pages)
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

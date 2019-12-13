import psycopg2
import psycopg2.extras


class Database:
    def __init__(self, dbname="daj9gh29vue350", user="crcwonmkxgjemv",
                    password="c6326c163f00c313adc58d3edc0e8a15db6fb938b9eb6e4468f1d1c6a13b15e7",
                    host="ec2-46-137-159-254.eu-west-1.compute.amazonaws.com"):
        self.con = psycopg2.connect(database=dbname, user=user, password=password, host=host)
        self.cur = self.con.cursor()
        self.userid = 0
        self.wishlistid = 0


    def addNewUser(self,form):
        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT email FROM user_list WHERE email = '%s';" %(form.email.data)
            cursor.execute(query)
            queryRes = cursor.fetchone()

        if queryRes is None:
            with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                query = "INSERT INTO user_list (username,password,firstname,lastname,email,schoolname,campusname)VALUES ('%s','%s','%s','%s','%s','%s', '%s');"%(form.username.data,form.password.data,form.firstname.data,form.lastname.data,form.email.data,form.schoolname.data,form.campusname.data)
                cursor.execute(query)

            with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                query = "SELECT userid  FROM user_list WHERE email='%s';" %(form.email.data)
                cursor.execute(query)
                queryRes = cursor.fetchone()
                return queryRes[0]

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


    def getProfileInformations(self,userid):
        queryRes = []

        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT userid, username, firstname, lastname, email, schoolname, campusname FROM user_list WHERE userid = {}".format(userid)
            cursor.execute(query)
            queryRes = cursor.fetchone()

            print('Query result {}'.format(queryRes))
        return queryRes

    def getWishlist(self,wishlistid):
        queryRes = []

        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT bookname, bookauthor, totalpages FROM book_info_list JOIN wish_list ON (book_info_list.bookid = wish_list.bookid) WHERE wishlistid = {}".format(wishlistid)
            cursor.execute(query)
            queryRes = cursor.fetchall()
        #print("QUERY RESULT: {}".format(queryRes))
        return queryRes

    def rmWishlist(self,wishlistid):
        queryRes = []
        queryDel = []

        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "DELETE FROM wish_list WHERE wishlistid = {}".format(wishlistid)
            cursor.execute(query)
            #queryDel = cursor.fetchall()

        #print("QUERY DEL RESULT: {}".format(queryDel))

        with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT bookname, bookauthor, totalpages FROM book_info_list JOIN wish_list ON (book_info_list.bookid = wish_list.bookid) WHERE wishlistid = {}".format(wishlistid)
            cursor.execute(query)
            queryRes = cursor.fetchall()
        #print("QUERY RESULT: {}".format(queryRes))
        return queryRes

        print("QUERY RESULT: {}".format(queryRes))
        return queryRes

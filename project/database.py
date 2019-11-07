import os
import psycopg2 as dbapi2

class dbOp:
    def __init__(self):
        pass

    def createTables(self):
        with dbapi2.connect(self.config) as connection:
            cursor = connection.cursor()

            # user_list
            query = """DROP TABLE IF EXISTS user_list CASCADE """
            cursor.execute(query)
            query = """CREATE TABLE user_list (
                                                    userId SERIAL PRIMARY KEY,
                                                    username VARCHAR(15) NOT NULL UNIQUE,
                                                    password VARCHAR(16) NOT NULL,
                                                    name VARCHAR(40) NOT NULL,
                                                    surname VARCHAR(40) NOT NULL,
                                                    email VARCHAR(100) UNIQUE NOT NULL,
                                                    schoolName VARCHAR(100) NOT NULL,
                                                    campusName VARCHAR(100),
                                                    wishlistId INTERGER,

                                                    FOREIGN KEY wishlistId REFERENCES wish_list(wishlistId) ON DELETE RESTRICT ON UPDATE CASCADE
                                                )"""
            cursor.execute(query)


            # interchange_event_list
            query = """DROP TABLE IF EXISTS interchange_event_list CASCADE """
            cursor.execute(query)
            query = """CREATE TABLE interchange_event_list (
                                                                interchangeId SERIAL PRIMARY KEY,
                                                                lenderId INTEGER NOT NULL UNIQUE,
                                                                borrowerId INTEGER NOT NULL UNIQUE,
                                                                time TIMESTAMP,
                                                                bookId INTEGER NOT NULL UNIQUE,


                                                                FOREIGN KEY bookId REFERENCES book_info_list(bookId) ON DELETE RESTRICT ON UPDATE CASCADE

                                                            )"""
                                                            # lenderID = userId
                                                            # borrowerId = userId

            cursor.execute(query)



            # book_info_list
            query = """DROP TABLE IF EXISTS book_info_list CASCADE """
            cursor.execute(query)
            query = """CREATE TABLE book_info_list(
                                                        bookId SERIAL PRIMARY KEY,
                                                        bookName VARCHAR(40) NOT NULL,
                                                        bookAuthor VARCHAR(40) NOT NULL,
                                                        totalPages INTEGER NOT NULL,

                                                    )"""
            cursor.execute(query)
            # @TODO Yazar tablosu eklendiginde authorId ile baska tabloya bagla




            # wish_list
            query = """DROP TABLE IF EXISTS wish_list CASCADE """
            cursor.execute(query)
            query = """CREATE TABLE wish_list (             wishlistID INTEGER NOT NULL,
                                                            bookId INTEGER NOT NULL,

                                                            PRIMARY KEY (wishlistID,bookId),
                                                            FOREIGN KEY bookId REFERENCES book_info_list(bookId) ON DELETE RESTRICT ON UPDATE CASCADE
                                            )"""
            cursor.execute(query)



        def db_init(self):
            pass

db = dbOp()

import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = {
    """
CREATE TABLE IF NOT EXISTS "book_info_list" (
    "bookid" SERIAL   NOT NULL,
    "bookname" VARCHAR(40)   NOT NULL,
    "bookauthor" VARCHAR(40)   NOT NULL,
    "totalpages" INTEGER   NOT NULL,
    CONSTRAINT "pk_book_info_list" PRIMARY KEY (
        "bookname", "bookauthor"
     )
);

CREATE TABLE IF NOT EXISTS "wish_list" (
    "wishlistid" INTEGER NOT NULL,
    "bookid" INTEGER NOT NULL,
    CONSTRAINT "pk_wish_list" PRIMARY KEY (
        "wishlistid","bookid"
     )
);

CREATE TABLE IF NOT EXISTS "user_list" (
    "userid" serial   NOT NULL,
    "username" VARCHAR(15)  NOT NULL,
    "password" VARCHAR(50)  NOT NULL,
    "firstname" VARCHAR(40)   NOT NULL,
    "lastname" VARCHAR(40)   NOT NULL,
    "email" VARCHAR(100)   NOT NULL,
    "schoolname" VARCHAR(100)   NOT NULL,
    "campusname" VARCHAR(100)   NOT NULL,
    "wishlistid" SERIAL NOT NULL,
    CONSTRAINT "pk_user_list" PRIMARY KEY (
        "userid"
     )
);

CREATE TABLE IF NOT EXISTS "interchange_event_list" (
    "interchangeid" SERIAL   NOT NULL,
    "lenderid" INTEGER   NOT NULL,
    "borrowerid" INTEGER   NOT NULL,
    "time" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    "bookid" INTEGER   NOT NULL,
    CONSTRAINT "pk_interchange_event_list" PRIMARY KEY (
        "interchangeid"
     )
);

INSERT INTO book_info_list(bookname,bookauthor, totalpages)VALUES ('1984','George Orwell',237);
INSERT INTO book_info_list(bookname,bookauthor, totalpages)VALUES ('The Count of Monte Cristo','Alexandre Dumas',276);
INSERT INTO book_info_list(bookname,bookauthor, totalpages)VALUES ('Animal Farm','George Orwell',141);
INSERT INTO book_info_list(bookname,bookauthor, totalpages)VALUES ('The Brothers Karamazov','Fyodor Dostoyevsky',10);
INSERT INTO book_info_list(bookname,bookauthor, totalpages)VALUES ('The Little Prince','Antoine de Saint-Exupery',10);
INSERT INTO book_info_list(bookname,bookauthor, totalpages)VALUES ('Romeo and Juliet','William Shakespeare',10);
INSERT INTO book_info_list(bookname,bookauthor, totalpages)VALUES ('War and Peace','Leo Tolstoy ',10);
INSERT INTO book_info_list(bookname,bookauthor, totalpages)VALUES ('Robinson Crusoe','Daniel Defoe',10);
INSERT INTO book_info_list(bookname,bookauthor, totalpages)VALUES ('David Copperfield','Charles Dickens',10);
INSERT INTO book_info_list(bookname,bookauthor, totalpages)VALUES ('Anna Karenina','George Eliot',10);
INSERT INTO book_info_list(bookname,bookauthor, totalpages)VALUES ('The Call of the Wild','Jack London',10);

INSERT INTO user_list (username,password,firstname,lastname, email,schoolname,campusname,wishlistid)
VALUES ('admin','12345','admin','admin','admin@interbooks.com', 'Istanbul Technical University','Ayazaga',1);

INSERT INTO user_list (username,password,firstname,lastname, email,schoolname,campusname,wishlistid)
VALUES ('cefatihozturk','0','M. Fatih','Öztürk','fatih@interbooks.com', 'Istanbul Technical University','Ayazaga',2);

INSERT INTO user_list (username,password,firstname,lastname, email,schoolname,campusname,wishlistid)
VALUES ('reyhanlioglu','1','Emre','Reyhanlıoğlu','emre@interbooks.com', 'Istanbul Technical University','Ayazaga',3);

INSERT INTO wish_list(bookid, wishlistid) VALUES (1, 1);
INSERT INTO wish_list(bookid, wishlistid) VALUES (4, 1);
INSERT INTO wish_list(bookid, wishlistid) VALUES (5, 1);


INSERT INTO interchange_event_list(lenderid, borrowerid, bookid) VALUES (1, 2,8);
INSERT INTO interchange_event_list(lenderid, borrowerid, bookid) VALUES (1, 3,5);




    """
}

def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)

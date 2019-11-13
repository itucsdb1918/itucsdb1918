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
        "bookid"
     )
);

CREATE TABLE IF NOT EXISTS "wish_list" (
    "wishlistid" SERIAL   NOT NULL,
    "bookid" INTEGER   NOT NULL,
    CONSTRAINT "pk_wish_list" PRIMARY KEY (
        "wishlistid","bookid"
     )
);

CREATE TABLE IF NOT EXISTS "user_list" (
    "userid" serial   NOT NULL,
    "username" VARCHAR(15)  NOT NULL,
    "firstname" VARCHAR(40)   NOT NULL,
    "lastname" VARCHAR(40)   NOT NULL,
    "email" VARCHAR(100)   NOT NULL,
    "schoolname" VARCHAR(100)   NOT NULL,
    "campusname" VARCHAR(100)   NOT NULL,
    "wishlistid" INTEGER   NOT NULL,
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
INSERT INTO book_info_list(bookname,bookauthor, totalpages)
VALUES ('cinali tatilde','erdem celik',10);
INSERT INTO wish_list(bookid)
VALUES (1);
INSERT INTO user_list (username,firstname,lastname, email,schoolname,campusname,wishlistid)
VALUES ('admin','admin','admin','admin@gmail.com', 'itu','maslak',1);

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

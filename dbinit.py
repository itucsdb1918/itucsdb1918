import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = {
    """
    CREATE TABLE IF NOT EXISTS "user_list" (
    "userId" serial   NOT NULL,
    "userName" VARCHAR(15)  NOT NULL,
    "firstName" VARCHAR(40)   NOT NULL,
    "lastName" VARCHAR(40)   NOT NULL,
    "email" VARCHAR(100)   NOT NULL,
    "schoolName" VARCHAR(100)   NOT NULL,
    "campusName" VARCHAR(100)   NOT NULL,
    "wishlistId" INTEGER   NOT NULL,
    CONSTRAINT "pk_user_list" PRIMARY KEY (
        "userId"
     )
);

CREATE TABLE IF NOT EXISTS "interchange_event_list" (
    "interchangeId" SERIAL   NOT NULL,
    "lenderId" INTEGER   NOT NULL,
    "borrowerId" INTEGER   NOT NULL,
    "time" TIMESTAMP   WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    "bookId" INTEGER   NOT NULL,
    CONSTRAINT "pk_interchange_event_list" PRIMARY KEY (
        "interchangeId"
     )
);


CREATE TABLE IF NOT EXISTS "book_info_list" (
    "bookId" SERIAL   NOT NULL,
    "bookName" VARCHAR(40)   NOT NULL,
    "bookAuthor" VARCHAR(40)   NOT NULL,
    "totalPages" INTEGER   NOT NULL,
    CONSTRAINT "pk_book_info_list" PRIMARY KEY (
        "bookId"
     )
);
CREATE TABLE IF NOT EXISTS "wish_list" (
    "wishlistID" SERIAL   NOT NULL,
    "bookId" INTEGER   NOT NULL,
    CONSTRAINT "pk_wish_list" PRIMARY KEY (
        "wishlistID","bookId"
     )
);

INSERT INTO user_list (userName,firstName,lastName, email,schoolName,campusName)
VALUES ('admin','admin','admin','admin@gmail.com', 'itu','maslak');
INSERT INTO interchange_event_list(lenderId,borrowerId, bookId)
VALUES (1,2,1);
INSERT INTO book_info_list(bookName,bookAuthor, totalPages)
VALUES ('cinali tatilde','erdem celik',10');

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

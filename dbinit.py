import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = {
    """
    CREATE TABLE IF NOT EXISTS "user_list" (
    "userId" serial   NOT NULL,
    "username" VARCHAR(15) IF NOT EXISTS  NOT NULL,
    "name" VARCHAR(40)   NOT NULL,
    "surname" VARCHAR(40)   NOT NULL,
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
    "time" TIMESTAMP   NOT NULL,
    "bookId" INTEGER   NOT NULL,
    CONSTRAINT "pk_interchange_event_list" PRIMARY KEY (
        "interchangeId"
     )
);

CREATE TABLE IF NOT EXISTS "book_info_list" (
    "bookId" SERIAL   NOT NULL,
    "bookName" VARCHAR(40)   NOT NULL,
    "bookAuthor" VARCHAR(40)   NOT NULL,
    "TotalPages" INTEGER   NOT NULL,
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


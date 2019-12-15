import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = {
    """

CREATE TABLE IF NOT EXISTS "user_list" (
    "userid" serial   NOT NULL,
    "username" VARCHAR(15)   NOT NULL,
    "password" VARCHAR(50)   NOT NULL,
    "firstname" VARCHAR(40)   NOT NULL,
    "lastname" VARCHAR(40)   NOT NULL,
    "email" VARCHAR(100)   NOT NULL,
    "schoolid" INTEGER   NOT NULL,
    "campusname" VARCHAR(100)   NOT NULL,
    "wishlistid" serial   NOT NULL,
    CONSTRAINT "pk_user_list" PRIMARY KEY (
        "userid"
     )
);

CREATE TABLE IF NOT EXISTS "interchange_event_list" (
    "interchangeid" SERIAL   NOT NULL,
    "lenderid" INTEGER   NOT NULL,
    "borrowerid" INTEGER   NOT NULL,
    "time" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    "bookname" VARCHAR(40)   NOT NULL,
    "bookauthor" VARCHAR(40)   NOT NULL,
    "totalpages" INTEGER   NOT NULL,
    "publisher" VARCHAR(40)   NOT NULL,
    CONSTRAINT "pk_interchange_event_list" PRIMARY KEY (
        "interchangeid"
     )
);

CREATE TABLE IF NOT EXISTS "school_list" (
    "schoolid" SERIAL   NOT NULL,
    "schoolname" VARCHAR(50)   NOT NULL,
    "schooltype" VARCHAR(40)   NOT NULL,
    "schoolcountry" VARCHAR(40)   NOT NULL,
    "schoolcity" VARCHAR(40)   NOT NULL,
    "schoolphonenumber" VARCHAR(40)   NOT NULL,
    CONSTRAINT "pk_school_list" PRIMARY KEY (
        "schoolid"
     )
);


ALTER TABLE "user_list" ADD CONSTRAINT "fk_user_list_schoolid" FOREIGN KEY("schoolid")
REFERENCES "school_list" ("schoolid");

ALTER TABLE "interchange_event_list" ADD CONSTRAINT "fk_interchange_event_list_lenderid" FOREIGN KEY("lenderid")
REFERENCES "user_list" ("userid");

ALTER TABLE "interchange_event_list" ADD CONSTRAINT "fk_interchange_event_list_borrowerid" FOREIGN KEY("borrowerid")
REFERENCES "user_list" ("userid");

    """
}


"""

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

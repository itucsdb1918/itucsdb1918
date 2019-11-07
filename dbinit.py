import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = {
    """
    CREATE TABLE user_list( 
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
                    );

    CREATE TABLE interchange_event_list( 
        interchangeId SERIAL PRIMARY KEY,
        lenderId INTEGER NOT NULL UNIQUE,
        borrowerId INTEGER NOT NULL UNIQUE,
        time TIMESTAMP,
        bookId INTEGER NOT NULL UNIQUE,
		FOREIGN KEY lenderId REFERENCES user_list(userId) ON DELETE RESTRICT ON UPDATE CASCADE
	    FOREIGN KEY borrowerId REFERENCES user_list(userId) ON DELETE RESTRICT ON UPDATE CASCADE
        FOREIGN KEY bookId REFERENCES book_info_list(bookId) ON DELETE RESTRICT ON UPDATE CASCADE
        );


    CREATE TABLE book_info_list( 
        bookId SERIAL PRIMARY KEY,
        bookName VARCHAR(40) NOT NULL,
        bookAuthor VARCHAR(40) NOT NULL,
        totalPages INTEGER NOT NULL              
                     );  

    CREATE TABLE wish_list( 
        wishlistID INTEGER NOT NULL,
        bookId INTEGER NOT NULL,
        PRIMARY KEY (wishlistID,bookId),
        FOREIGN KEY bookId REFERENCES book_info_list(bookId) ON DELETE RESTRICT ON UPDATE CASCADE
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


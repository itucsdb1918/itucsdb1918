import os
import psycopg2 as dbapi2

class dbOp:
    def __init__(self):
        pass
    
    def createTables(self):
        with dbapi2.connect(self.config) as connection:
            cursor = connection.cursor()

            # ADMIN USER INFO TABLOSU
            query = """DROP TABLE IF EXISTS adminUserInfo CASCADE """
            cursor.execute(query)
            query = """CREATE TABLE adminUserInfo (
                                                            ID SERIAL PRIMARY KEY,
                                                            Username VARCHAR(15) NOT NULL UNIQUE,
                                                            Name VARCHAR(40) NOT NULL,
                                                            Surname VARCHAR(40) NOT NULL,
                                                            Mail VARCHAR(100) UNIQUE NOT NULL,
                                                            SchoolName VARCHAR(100) NOT NULL,
                                                            CampusName VARCHAR(100),
                                                            WishlistID SERIAL PRIMARY KEY
                                                            FOREIGN KEY ID REFERENCES adminInterchangeOps(LenderID) 
                                                            ON DELETE RESTRICT ON UPDATE CASCADE,
                                                            FOREIGN KEY ID REFERENCES adminInterchangeOps(BorrowerID) 
                                                            ON DELETE RESTRICT ON UPDATE CASCADE
                                                                            )"""
            cursor.execute(query)
            
            
            
            
        def db_init(self):
            pass
        
db = dbOp()            

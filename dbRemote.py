import psycopg2
import psycopg2.extras


class Database:
    def __init__(self, dbname="daj9gh29vue350", user="crcwonmkxgjemv",
                    password="c6326c163f00c313adc58d3edc0e8a15db6fb938b9eb6e4468f1d1c6a13b15e7",
                    host="ec2-46-137-159-254.eu-west-1.compute.amazonaws.com"):
        self.con = psycopg2.connect(database=dbname, user=user, password=password, host=host)
        self.cur = self.con.cursor()

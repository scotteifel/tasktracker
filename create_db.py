import sqlite3, os

def db_startup():

    try:
        test = open("main.db")
    except:
        create_database()
        print("not there")


def create_database():
        path = os.path.abspath("tasktrack")
        path = path[:-9]
        conn = sqlite3.connect(path+"main.db")
        conn.commit()
        conn.close()

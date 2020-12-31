import sqlite3, os




def db_startup():

    try:
        with open('main.db') as file:
            print("yes it exists")
        return True

    except IOError:
        print("File does not exist")
        create_database()
        return False

def create_database():
        path = os.path.abspath("tasktrack")
        path = path[:-9]
        conn = sqlite3.connect(path+"main.db")
        conn.commit()
        conn.close()

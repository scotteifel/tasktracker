import sqlite3, os




def db_startup():

    #Check to see if the projectname table was created or not
    try:
        with open('main.db') as file:
            conn = sqlite3.connect('main.db')
            cur = conn.cursor()
            cur.execute('''SELECT * FROM project_name''')
            cur.close()
            conn.close()
        return True

    except:
        create_database()
        return False

def create_database():
        path = os.path.abspath("tasktrack")
        path = path[:-9]
        conn = sqlite3.connect(path+"main.db")
        conn.commit()
        conn.close()

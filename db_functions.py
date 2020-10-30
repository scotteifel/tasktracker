import sqlite3


def new_task_info(name,blurb,count):

    conn = sqlite3.connect('main.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS tasks (title TEXT,
                description TEXT, time INTEGER)''')
    conn.commit()

    cur.execute('''INSERT INTO tasks (title, description, time)
                    VALUES(?,?,?)''', (name,blurb,count))
    conn.commit()

    cur.close()
    conn.close()

def retrieve_tasks():
    conn = sqlite3.connect('main.db')
    cur = conn.cursor()
    info = None
    try:
        qry = cur.execute('''SELECT * FROM tasks''')
        info = qry.fetchall()
        print(info)
    except:
        pass

    cur.close()
    conn.close()
    return info

import sqlite3


def new_task_info(name,blurb):

    conn = sqlite3.connect('main.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS tasks (title TEXT,
                description TEXT)''')
    conn.commit()

    cur.execute('''INSERT INTO tasks (title, description) VALUES(?,?)''',
                                         (name,blurb))
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
    except:
        pass

    cur.close()
    conn.close()
    return info

import sqlite3


def new_task_info(name,blurb,count):

    count = int(count)
    conn = sqlite3.connect('main.db')
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS tasks (title TEXT,
    description TEXT, time INTEGER)''')
    conn.commit()
    try:
        qry = cur.execute('''SELECT * FROM tasks WHERE title = (?)''', (name,))
        info = qry.fetchone()[0]
        cur.execute('''UPDATE tasks SET title = (?), description=(?),
                    time=(?) WHERE title = (?)''', (name,blurb,count,info))
        conn.commit()
        cur.close()
        conn.close()
        print("here")
        return True
    except:
        cur.execute('''INSERT INTO tasks (title, description, time)
                        VALUES(?,?,?)''', (name,blurb,count))
        conn.commit()
        cur.close()
        conn.close()
        print("returned true")
        return False
    # try:
    #     qry = cur.execute('''SELECT * FROM tasks WHERE title = (?)''', (name,))
    #     info = qry.fetchone()
    #     cur.execute('''UPDATE tasks SET title = (?), description = (?),
    #                 time=(?) WHERE title = name)''', (name,blurb,count))
    #     conn.commit()
    #     print("Hey here")
    #
    # except:
    #     cur.execute('''INSERT INTO tasks (title, description, time)
    #                     VALUES(?,?,?)''', (name,blurb,count))
    #     conn.commit()
    #     print('Excepted')



def add_completed_task(title, description, time, on_time):

    conn = sqlite3.connect("main.db")
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS completed (title TEXT,
                description TEXT, time INTEGER, on_time BOOL)''')

    qry = cur.execute('''INSERT INTO completed (title, description,time,
           on_time) VALUES (?,?,?,?)''',(title,description,time,on_time))
    conn.commit()

    qry1 = cur.execute('''SELECT * FROM completed''')
    for item in qry1:
        print(item)

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

def retrieve_task_info(task):
    conn = sqlite3.connect('main.db')
    cur = conn.cursor()
    qry = cur.execute('''SELECT * FROM tasks WHERE title = (?)''', (task,))
    info = qry.fetchone()
    cur.close()
    conn.close()
    return info


def retrieve_description(title):
    conn = sqlite3.connect('main.db')
    cur = conn.cursor()
    info = None
    try:
        qry = cur.execute('''SELECT * FROM tasks WHERE title = (?)''',(title,))
        info = qry.fetchone()
    except:
        pass

    cur.close()
    conn.close()
    return info


def update_timer(new_time, task):

    conn = sqlite3.connect('main.db')
    cur = conn.cursor()

    qry = cur.execute('''UPDATE tasks SET time = (?) WHERE title = (?)''',
    (new_time, task))
    conn.commit()

    cur.close()
    conn.close()


def delete_task(task):
    conn = sqlite3.connect('main.db')
    cur = conn.cursor()

    qry = cur.execute('''DELETE FROM tasks WHERE title = (?)''',
    (task,))
    conn.commit()

    qry = cur.execute('''SELECT * FROM tasks''')

    cur.close()
    conn.close()

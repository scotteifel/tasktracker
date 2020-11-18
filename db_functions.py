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
        return True
    except:
        cur.execute('''INSERT INTO tasks (title, description, time)
                        VALUES(?,?,?)''', (name,blurb,count))
        conn.commit()
        cur.close()
        conn.close()
        return False


def retrieve_completions():
    conn = sqlite3.connect('main.db')
    cur = conn.cursor()

    qry = cur.execute('''SELECT * FROM completions''')
    info = qry.fetchall()

    cur.close()
    conn.close()
    return info


def add_completed_task(title, description, time, on_time):
    conn = sqlite3.connect("main.db")
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS completions (title TEXT,
                description TEXT, time INTEGER, on_time INTEGER)''')

    qry = cur.execute('''INSERT INTO completions (title, description, time,
            on_time) VALUES (?,?,?,?)''',(title,description,time,on_time))
    conn.commit()

    qry1 = cur.execute('''SELECT * FROM completions''')

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

import sqlite3, os



def save_project_name(name):
    conn = sqlite3.connect('main.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS project_name (name TEXT)''')
    conn.commit()
    cur.execute('''INSERT INTO project_name (name) VALUES(?)''', (name,))
    conn.commit()
    cur.close()
    conn.close()

def get_project_name():
    conn = sqlite3.connect('main.db')
    cur = conn.cursor()
    qry = cur.execute('''SELECT name FROM project_name''')
    item = qry.fetchone()[0]
    cur.close()
    conn.close()

    return item

def new_task_info(name,blurb,count):

    count = int(count)
    conn = sqlite3.connect('main.db')
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS tasks (title TEXT,
    description TEXT, time INTEGER, project_name TEXT)''')

    #If a user is modifying an existing task this try statement will be used
    try:
        qry =cur.execute('''SELECT * FROM tasks WHERE title = (?)''',(name,))
        info = qry.fetchone()[0]
        cur.execute('''UPDATE tasks SET title = (?), description=(?),
                    time=(?) WHERE title = (?)''', (name,blurb,count,info))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except:
        cur.execute('''INSERT INTO tasks (title, description, time)
                       VALUES(?,?,?)''',(name,blurb,count))
        conn.commit()
        cur.close()
        conn.close()
        return False


def start_new_project():

    os.remove('main.db')
    print("database removed")

def check_completed_names(text):
    conn = sqlite3.connect('main.db')
    cur = conn.cursor()

    try:
        qry = cur.execute('''SELECT * FROM completions WHERE title = (?)''',
                            (text,))
        _ = qry.fetchone()

        if _ == None:
            result = False
        else:
            result = True
    except:
        result = False
    cur.close()
    conn.close()

    return result


def add_completed_task(title, description, time, notes):
    conn = sqlite3.connect("main.db")
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS completions (title TEXT,
        description TEXT, time INTEGER, notes TEXT)''')

    qry = cur.execute('''INSERT INTO completions (title, description,
        time, notes) VALUES (?,?,?,?)''',
        (title, description, time, notes))

    conn.commit()
    cur.close()
    conn.close()
    return


def run_project_timer():
    conn = sqlite3.connect('main.db')
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS project_time
                   (time INTEGER)''')
    conn.commit()

    info = cur.execute('''SELECT * FROM project_time''')
    qry = cur.fetchone()

    #if statement used to catch the first time this func is run from program
    if not qry:
            cur.execute('''INSERT INTO project_time (time) VALUES (?)''',
                        (1,))
            conn.commit()
            cur.close()
            conn.close()
            return 1

    new_time = qry[0] + 1
    cur.execute('''UPDATE project_time SET time = (?)''', (new_time,))

    conn.commit()
    cur.close()
    conn.close()
    return new_time


def update_timer(new_time, task):

    conn = sqlite3.connect('main.db')
    cur = conn.cursor()

    qry = cur.execute('''UPDATE tasks SET time = (?) WHERE title = (?)''',
    (new_time, task))
    conn.commit()

    cur.close()
    conn.close()


def retrieve_project_time():
    conn = sqlite3.connect('main.db')
    cur = conn.cursor()

    try:
        qry = cur.execute('''SELECT * FROM project_time''')
        info = qry.fetchone()[0]
    except:
        info = 0
    cur.close()
    conn.close()
    return info


def retrieve_tasks():
    conn = sqlite3.connect('main.db')
    cur = conn.cursor()
    info = None
    try:
        qry = cur.execute('''SELECT title, time FROM tasks''')
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
        qry=cur.execute('''SELECT description FROM tasks WHERE title = (?)''',
                        (title,))
        info = qry.fetchone()
    except:
        pass


    cur.close()
    conn.close()
    return info


def retrieve_initial_time(title):
    conn = sqlite3.connect('main.db')
    cur = conn.cursor()
    qry=cur.execute('''SELECT time FROM tasks WHERE title = (?)''',
                    (title,))
    info = qry.fetchone()

    cur.close()
    conn.close()
    return info


def retrieve_notes(title):
    conn = sqlite3.connect('main.db')
    cur = conn.cursor()
    info = None
    try:
        qry=cur.execute('''SELECT notes FROM completions WHERE title = (?)''',
                        (title,))
        info = qry.fetchone()
    except:
        pass

    cur.close()
    conn.close()
    return info


def retrieve_completions():
    conn = sqlite3.connect('main.db')
    cur = conn.cursor()

    try:
        qry = cur.execute('''SELECT * FROM completions''')
        info = qry.fetchall()
    except:
        info = False
        pass

    cur.close()
    conn.close()
    return info


def delete_task(task):
    conn = sqlite3.connect('main.db')
    cur = conn.cursor()

    qry = cur.execute('''DELETE FROM tasks WHERE title = (?)''',
    (task,))
    conn.commit()

    qry = cur.execute('''SELECT * FROM tasks''')

    cur.close()
    conn.close()

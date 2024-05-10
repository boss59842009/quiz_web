import sqlite3

db_name = 'quiz.db'
conn = None
cursor = None


def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()


def close():
    cursor.close()
    conn.close()


def do(query):
    cursor.execute(query)
    conn.commit()


def create():
    open()
    do('''CREATE TABLE quiz(
            id INTEGER PRIMARY KEY,
            name VARCHAR)''')

    do('''CREATE TABLE questions(
                id INTEGER PRIMARY KEY,
                question VARCHAR,
                answer VARCHAR,
                wrong1 VARCHAR,
                wrong2 VARCHAR,
                wrong3 VARCHAR)''')

    close()


def clear_db():
    ''' видаляє всі таблиці '''
    open()
    query = '''DROP TABLE IF EXISTS questions'''
    do(query)
    query = '''DROP TABLE IF EXISTS quiz'''
    do(query)
    close()


def add_quizes():
    open()
    quizes = [
        ("Моя гра",),
        ('Хто хоче стати мільйонером?',),
        ('Найрозумніший',),
        ("Математика",)
    ]
    cursor.executemany('''INSERT INTO quiz (name) VALUES (?)''', quizes)
    conn.commit()
    close()



def main():
    # clear_db()
    # create()
    add_quizes()
    pass


main()



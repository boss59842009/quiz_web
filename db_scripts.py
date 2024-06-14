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


def clear_db():
    ''' видаляє всі таблиці '''
    open()
    query = '''DROP TABLE IF EXISTS quiz_content'''
    do(query)
    query = '''DROP TABLE IF EXISTS questions'''
    do(query)
    query = '''DROP TABLE IF EXISTS quiz'''
    do(query)
    close()

    
def create():
    '''Створення таблиць в БД'''
    open()
    do('''CREATE TABLE IF NOT EXISTS quiz(
        id INTEGER PRIMARY KEY,
        name VARCHAR)''')

    do('''CREATE TABLE IF NOT EXISTS questions(
            id INTEGER PRIMARY KEY,
            question VARCHAR,
            answer VARCHAR, 
            wrong1 VARCHAR,
            wrong2 VARCHAR,
            wrong3 VARCHAR)''')

    do('''CREATE TABLE IF NOT EXISTS quiz_content(
            id INTEGER PRIMARY KEY,
            quiz_id INTEGER,
            question_id INTEGER,
            FOREIGN KEY (quiz_id) REFERENCES quiz (id),
            FOREIGN KEY (question_id) REFERENCES questions (id))''')

    close()


def add_questions():
    '''Додавання запитань в таблицю БД'''
    questions = [
        ('Скільки місяців на рік мають 28 днів?', 'Всі', 'Один', 'Жодного', 'Два'),
        ('Яким стане зелена скеля, якщо впаде в Червоне море?', 'Мокрим', 'Червоним', 'Не зміниться', 'Фіолетовим'),
        ('Якою рукою краще розмішувати чай?', 'Ложкою', 'Правою', 'Лівою', 'Любою'),
        ('Що не має довжини, глибини, ширини, висоти, а можна виміряти?', 'Час', 'Дурність', 'Море', 'Повітря'),
        ('Коли сіткою можна витягнути воду?', 'Коли вода замерзла', 'Коли немає риби', 'Коли спливла золота рибка',
         'Коли сітка порвалася'),
        ('Що більше слона і нічого не важить?', 'Тінь слона', 'Повітряна куля', 'Парашут', 'Хмара')
    ]
    open()
    cursor.executemany('''INSERT INTO questions (question, answer, wrong1, wrong2, wrong3) VALUES (?,?,?,?,?)''', questions)
    conn.commit()
    close()

def add_quiz():
    '''Додавання вікторин в таблицю БД'''
    quizes = [
        ('Своя гра',),
        ('Хто хоче стати мільйонером?',),
        ('Найрозумніший',),
        ("Математика",)
    ]
    open()
    cursor.executemany('''INSERT INTO quiz (name) VALUES (?)''', quizes)
    conn.commit()
    close()


def add_links():
    '''Додавання звʼязків між вікторинами і питаннями в таблицю БД'''
    open()
    cursor.execute('PRAGMA foreign_keys=on')
    answer = input("Додати звʼязок?(y/n) ")
    while answer != 'n':
        quiz_id = int(input("Номер вікторини: "))
        question_id = int(input("Номер запитання: "))
        cursor.execute('INSERT INTO quiz_content (quiz_id, question_id) VALUES (?,?)', [quiz_id, question_id])
        conn.commit()
        answer = input("Додати звʼязок?(y/n) ")
    close()


def show(table):
    query = 'SELECT * FROM ' + table
    open()
    cursor.execute(query)
    print(cursor.fetchall())
    close()


def get_question_after(question_id=0, quiz_id=1):
    '''Повертає дані про наступне питання привʼязане до вікторини'''
    open()
    cursor.execute('''SELECT quiz_content.id, questions.question, questions.answer,
     questions.wrong1, questions.wrong2, questions.wrong3
     FROM quiz_content, questions
     WHERE quiz_content.question_id == questions.id
     AND quiz_content.id > ? AND quiz_content.quiz_id == ?
     ORDER BY quiz_content.id''', [question_id, quiz_id])
    result = cursor.fetchone()
    close()
    return result


def quiz_count():
    '''Повертає кількість вікторин в таблиці'''
    open()
    cursor.execute('SELECT MAX(quiz_id) FROM quiz_content')
    result = cursor.fetchone()
    close()
    return result


def get_quizes():
    '''Повертає назви вікторин'''
    open()
    cursor.execute('SELECT * FROM quiz ORDER BY id')
    result = cursor.fetchall()
    close()
    return result


def insert_quiz(quiz):
    '''Запис вікторин в талицю БД'''
    open()
    cursor.execute("INSERT INTO quiz (name) VALUES(?)", [quiz])
    conn.commit()
    close()


def insert_question(question):
    '''Запис запитань в таблицю БД'''
    open()
    cursor.execute("INSERT INTO questions (question, answer, wrong1, wrong2, wrong3) VALUES (?,?,?,?,?)", question)
    conn.commit()
    close()


def add_link(quiz_name):
    '''Додавання звʼязку вікторини з запитанням'''
    open()
    cursor.execute('SELECT id FROM quiz WHERE name == ?', [quiz_name])
    quiz_id = cursor.fetchone()
    cursor.execute('SELECT max(id) FROM questions')
    question_id = cursor.fetchone()
    cursor.execute('INSERT INTO quiz_content (quiz_id, question_id) VALUES (?, ?)', [quiz_id[0], question_id[0]])
    conn.commit()
    close()


def show_tables():
    show('questions')
    show('quiz')
    show('quiz_content')


def check_answer(quiz_cont_id, answer):
    '''Перевіряє чи правильна відповідь на питання'''
    open()
    cursor.execute('''
        SELECT questions.answer
        FROM quiz_content, questions
        WHERE quiz_content.id == ?
        AND quiz_content.question_id == questions.id''', [quiz_cont_id])
    right_ans = cursor.fetchone()
    conn.commit()
    close()
    if right_ans is None:
        return False
    elif answer == right_ans[0]:
        return True
    else:
        return False


def main():
    # clear_db()
    # create()
    # add_questions()
    # add_quiz()
    # add_links()
    # show_tables()
    # print(get_question_after(2, 1))
    pass


if __name__ == "__main__":
    main()

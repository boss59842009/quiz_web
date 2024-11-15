import sqlite3

db_name = 'quiz.db'
conn = None
cursor = None


def open():
    '''Відкриття БД'''
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

    do('''CREATE TABLE quiz_content(
                    id INTEGER PRIMARY KEY,
                    quiz_id INTEGER,
                    question_id INTEGER,
                    FOREIGN KEY (quiz_id) REFERENCES quiz (id),
                    FOREIGN KEY (question_id) REFERENCES questions (id))''')
    close()


def clear_db():
    ''' видаляє всі таблиці '''
    open()
    query = '''DROP TABLE IF EXISTS questions'''
    do(query)
    query = '''DROP TABLE IF EXISTS quiz'''
    do(query)
    query = '''DROP TABLE IF EXISTS quiz_content'''
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


def add_questions():
    questions = [
        ('Скільки місяців на рік мають 28 днів?', 'Всі', 'Один', 'Жодного', 'Два'),
        ('Яким стане зелена скеля, якщо впаде в Червоне море?', 'Мокрим', 'Червоним', 'Не зміниться', 'Фіолетовим'),
        ('Якою рукою краще розмішувати чай?', 'Ложкою', 'Правою', 'Лівою', 'Любою'),
        ('Що не має довжини, глибини, ширини, висоти, а можна виміряти?', 'Час', 'Дурність', 'Море', 'Повітря'),
        ('Коли сіткою можна витягнути воду?', 'Коли вода замерзла', 'Коли немає риби', 'Коли спливла золота рибка', 'Коли сітка порвалася'),
        ('Що більше слона і нічого не важить?', 'Тінь слона', 'Повітряна куля', 'Парашут', 'Хмара'),
    ]
    open()
    cursor.executemany('INSERT INTO questions (question, answer, wrong1, wrong2, wrong3) VALUES (?, ?, ?, ?, ?)', questions)
    conn.commit()
    close()


def add_links():
    '''Додає звʼязки вікторини і запитання'''
    open()
    cursor.execute("PRAGMA foreign_keys=on")
    answer = input("Додати звʼязок? (y/n)")
    while answer != 'n':
        quiz_id = int(input("Введіть номер вікторини"))
        question_id = int(input("Введіть номер запитання"))
        cursor.execute('INSERT INTO quiz_content (quiz_id, question_id) VALUES (?, ?)', [quiz_id, question_id])
        conn.commit()
        answer = input("Додати звʼязок? (y/n)")
    close()


def get_question_after(question_id=0, quiz_id=1):# 3, 4
    '''Повертає наступне запитання до вибраної вікторини'''
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

def get_quizes():
    '''Отримуємо всі вікторини'''
    open()
    cursor.execute('SELECT * FROM quiz ORDER BY id')
    quizes = cursor.fetchall()
    print(quizes)
    close()
    return quizes


def check_ans(answer, quest_id):
    """Перевіряє чи правильно ми відповіли на питання"""
    open()
    cursor.execute('''
        SELECT questions.answer 
        FROM quiz_content, questions
        WHERE quiz_content.id == ?
        AND quiz_content.question_id == questions.id''', [quest_id])
    result = cursor.fetchone()  # ('ложкою', )
    conn.commit()
    close()
    if answer == result[0]:
        return True
    elif answer is None:
        return False
    else:
        return False


def insert_quiz(quiz):
    """Записує вікторину в БД"""
    open()
    cursor.execute('INSERT INTO quiz (name) VALUES (?)', [quiz])
    conn.commit()
    close()


def insert_question(question_list):
    """Записує дані запитання в БД"""
    open()
    cursor.execute('INSERT INTO questions (question, answer, wrong1, wrong2, wrong3) VALUES (?, ?, ?, ?, ?)', question_list)
    conn.commit()
    close()


def add_link(quiz_name):
    """Записує звʼязок між вікториною і запитанням в БД"""
    open()
    cursor.execute('SELECT id FROM quiz WHERE name == ?', [quiz_name])
    quiz_id = cursor.fetchone()
    cursor.execute('SELECT max(id) FROM questions')
    question_id = cursor.fetchone()
    cursor.execute("INSERT INTO quiz_content (quiz_id, question_id) VALUES (?, ?)", [quiz_id[0], question_id[0]])
    conn.commit()
    close()


def main():
    # clear_db()
    # create()
    # add_quizes()
    # add_questions()
    # add_links()
    # get_question_after(11, 4)
    get_quizes()


main()



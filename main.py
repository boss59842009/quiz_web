from flask import Flask, request, url_for, render_template, redirect, session
import db_scripts
from random import shuffle


def start_session(quiz_id=0):
    '''Створення сессій для розділення користувачів'''
    session['quiz'] = quiz_id
    session['last_question'] = 0
    session['right_ans'] = 0
    session['wrong_ans'] = 0
    session['total'] = 0


app = Flask(__name__)


# шлях до головної сторінки
@app.route('/', methods=['GET', 'POST'])
@app.route('/index')
def index():
    """Фукнція відображення головної сторінки"""
    if request.method == 'GET':
        start_session(-1)
        quizes_list = db_scripts.get_quizes()
        return render_template('index.html', quizes=quizes_list)
    else:
        quiz_id = request.form.get('quiz')
        start_session(quiz_id)
        return redirect(url_for('test'))


def question_form(question): #(4, "Якесь питання", "Правильна відповідь", "Неправ1", "Неправ2", "Неправ3")
    answers_list = [
        question[2],
        question[3],
        question[4],
        question[5]
    ]
    shuffle(answers_list)
    return render_template('test.html', question_id=question[0], quest=question[1], ans_list=answers_list)


def check_answer():
    """Функція яка перевіряє чи правильно ми відповіли на питання"""
    answer = request.form.get('ans_name')
    quest_id = request.form.get('q_id')
    session['last_question'] = quest_id
    session['total'] += 1
    if db_scripts.check_ans(answer, quest_id):
        session['right_ans'] += 1
    else:
        session['wrong_ans'] += 1


# шлях до сторінки з тестуванням
@app.route('/test', methods=['GET', 'POST'])
def test():
    """Фукнція відображення сторінки з тестуванням"""
    if not ('quiz' in session) or int(session['quiz']) < 0:
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            check_answer()
        new_question = db_scripts.get_question_after(session['last_question'], session['quiz'])
        if new_question is None or len(new_question) == 0:
            return redirect(url_for('result'))
        else:
            return question_form(new_question)

# шлях до сторінки з результатами
@app.route('/result')
def result():
    """Функція відображення сторінки з результатами тестування"""
    res = render_template('result.html', total=session['total'], right=session['right_ans'], wrong=session['wrong_ans'])
    session.clear()
    return res
    
def save_quiz():
    """Фунція яка зберігає віткорину та запитання і додає звʼязок"""
    quiz = request.form.get('quiz')
    question = request.form.getlist('question[]')
    db_scripts.insert_question(question)
    quizes = db_scripts.get_quizes() 
    for id, name in quizes:
        if name.lower() == quiz.lower():
            db_scripts.add_link(quiz)
            break
    else:
        db_scripts.insert_quiz(quiz)
        db_scripts.add_link(quiz)


# шлях до сторінки з додаванням вікторини
@app.route('/add_quiz', methods=['GET', 'POST'])
def add_quiz():
    """Функція відображення сторінки з додаванням вікторини"""
    if request.method == 'GET':
        return render_template('add_quiz.html')
    else:
        save_quiz()
        return redirect(url_for('index'))


app.config['SECRET_KEY'] = '12345678'
if __name__ == '__main__':
    app.run(port=5000)

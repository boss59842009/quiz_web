from flask import Flask, url_for, render_template, request, redirect, session
import sqlite3
from db_scripts import *
from random import randint, shuffle

app = Flask(__name__)


def start_quiz(quiz_id=0):
    session['quiz'] = quiz_id
    session['last_question'] = 0
    session['answer'] = 0
    session['total'] = 0


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        start_quiz(-1)
        # return '<a href="/test">Перейти до тесту</a>'
        quizes = get_quizes()
        return render_template('start.html', quiz_list=quizes)
    else:
        quiz_id = request.form.get('quiz')
        start_quiz(quiz_id)
        return redirect(url_for('test'))


def question_form(question):
    answers_list = [
        question[2], question[3], question[4], question[5]
    ]
    shuffle(answers_list)
    return render_template('test.html', question=question[1], quest_id=question[0], answers_list=answers_list)


def save_answers():
    answer = request.form.get('ans_text')
    quiz_content_id = request.form.get('q_id')
    session['last_question'] = quiz_content_id
    session['total'] += 1
    if check_answer(quiz_content_id, answer):
        session['answer'] += 1


@app.route('/test', methods=['POST', 'GET'])
def test():
    result = get_question_after(session['last_question'], session['quiz'])
    if not ('quiz' in session) or int(session['quiz']) < 0:
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            save_answers()
        next_question = get_question_after(session['last_question'], session['quiz'])
        if next_question is None or len(next_question) == 0:
            return redirect(url_for('result'))
        else:
            return question_form(next_question)


@app.route('/result')
def result():
    res = render_template('result.html', right=session['answer'], total=session['total'])
    session.clear()
    return res


def save_quiz():
    quiz_name = request.form.get('quiz_name')
    question_info = request.form.getlist('question_info[]')
    insert_question(question_info)
    for id, quiz in get_quizes():
        if quiz_name == quiz:
            add_link(quiz_name)
            break
    else:
        insert_quiz(quiz_name)
        add_link(quiz_name)


@app.route('/add_quiz', methods=['POST', 'GET'])
def add_quiz():
    if request.method == 'POST':
        save_quiz()
        return '<h1>Запис пройшов успішно</h1>'
    else:
        return render_template('add_quiz.html')


app.config['SECRET_KEY'] = '12345678'
if __name__ == '__main__':
    app.run(port=3000)



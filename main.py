from flask import Flask, request, url_for, render_template, redirect, session
import db_scripts
from random import shuffle


def start_session(quiz_id=0):
    session['quiz'] = quiz_id
    session['last_question'] = 0
    session['right_ans'] = 0
    session['wrong_ans'] = 0
    session['total'] = 0


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index')
def index():
    if request.method == 'GET':
        start_session(-1)
        quizes_list = db_scripts.get_quizes()
        return render_template('index.html', quizes=quizes_list)
    else:
        quiz_id = request.form.get('quiz')
        start_session(quiz_id)
        return redirect(url_for('test'))


def question_form(question):
    print(question)
    answers_list = [
        question[2],
        question[3],
        question[4],
        question[5]
    ]
    shuffle(answers_list)
    return render_template('test.html', question_id=question[0], quest=question[1], ans_list=answers_list)


@app.route('/test', methods=['GET', 'POST'])
def test():
    new_question = db_scripts.get_question_after(session['last_question'], session['quiz'])
    if not ('quiz' in session) or int(session['quiz']) < 0:
        return redirect(url_for('index'))
    else:
        if request.method == 'GET':
            return question_form(new_question)
        else:
            answer = request.form.get('ans_name')
            print(answer)
            return redirect(url_for('index'))


@app.route('/result')
def result():
    return '<h1>Result page</h1>'


@app.route('/add_quiz')
def add_quiz():
    return '<h1>Add quiz page</h1>'


app.config['SECRET_KEY'] = '12345678'
if __name__ == '__main__':
    app.run(port=3000)

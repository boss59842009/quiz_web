from flask import Flask, url_for, render_template, redirect, session
import db_scripts

def start_session(quiz_id=0):
    session['quiz'] = quiz_id
    session['last_question'] = 0
    session['right_ans'] = 0
    session['wrong_ans'] = 0
    session['total'] = 0

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    start_session(1)
    print(session)
    return '<h1>Start page</h1>'


@app.route('/test')
def test():
    session['quiz'] += 1
    print(session)
    return '<h1>Test page</h1>'


@app.route('/result')
def result():
    return '<h1>Result page</h1>'


@app.route('/add_quiz')
def add_quiz():
    return '<h1>Add quiz page</h1>'


app.config['SECRET_KEY'] = '12345678'
if __name__ == '__main__':
    app.run(port=9000)

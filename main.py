from flask import Flask, url_for, render_template, redirect
import db_scripts

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return '<h1>Start page</h1>'


@app.route('/test')
def test():
    return '<h1>Test page</h1>'


@app.route('/result')
def result():
    return '<h1>Result page</h1>'


@app.route('/add_quiz')
def add_quiz():
    return '<h1>Add quiz page</h1>'


if __name__ == '__main__':
    app.run(port=9000)

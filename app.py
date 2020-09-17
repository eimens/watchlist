from flask import Flask
from flask import url_for

app = Flask(__name__)

@app.route('/')
@app.route('/index')
@app.route('/home')
def hello():
    return '<h1>Hello toroto</h1> <img src="http://helloflask.com/totoro.gif">'

@app.route('/user/<name>')
def user_page(name):
    appear = 'user is :' + name
    return appear

@app.route('/test')
def test_url_for():
    print(url_for('hello'))
    print(url_for('user_page', name='yihk'))
    print(url_for('user_page', name='peter'))
    print(url_for('test_url_for', num=2))
    return 'Test page' 
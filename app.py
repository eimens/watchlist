from flask import Flask, render_template
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
import sys
import os
import click

app = Flask(__name__)

prefix = 'sqlite:////'
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)

class Cuser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))

@app.cli.command()
def forge():
    db.create_all()
    
    user = Cuser(name=name)
    db.session.add(user)

    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)
    
    db.session.commit()
    click.echo('Done..')

@app.context_processor
def inject_user():
    user = Cuser.query.first()
    return dict(user=user)

@app.route('/')
@app.route('/index')
def index():
    user = Cuser.query.first()
    movie = Movie.query.all()
    return render_template('index.html', movies=movie)

    
@app.route('/hello') 
def hello():
    return 'hello eveyboday!'

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

@app.errorhandler(404)
def page_not_found(e):
    user = Cuser.query.first()
    return render_template('404.html') 

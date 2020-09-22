from flask import Flask, render_template, request, redirect, flash
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, login_required
from flask_login import logout_user, LoginManager, current_user
import sys
import os
import click

app = Flask(__name__)

prefix = 'sqlite:////'
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['SECRET_KEY'] = 'dev'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' 

class Cuser(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    user_name = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))

@app.cli.command()
def forge():
    db.create_all()
    
    name = 'Grey Li'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

    user = Cuser(name=name)
    db.session.add(user)

    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)
    
    db.session.commit()
    click.echo('Done..')

@app.cli.command()
@click.option('--username', prompt=True, help="The username used to login")
@click.option('--password', prompt=True, hide_input=True, 
              confirmation_prompt=True, help="The password user to login")
def admin(username, password):
    """create user"""
    db.create_all()

    user = Cuser.query.first()
    if user is not None:
        click.echo('Update user')
        user.user_name = username
        user.set_password(password)
    else:
        click.echo('Create user')
        user = User(user_name = username, name='Admin')
        user.set_password(password)
        db.session.add(user)
    
    db.session.commit()
    click.echo("Done")

@app.context_processor
def inject_user():
    user = Cuser.query.first()
    return dict(user=user)

@login_manager.user_loader
def load_user(user_id):
    user = Cuser.query.get(int(user_id))
    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Invalid input')
            return redirect(url_for('login'))
        
        user = Cuser.query.first()
        if username == user.user_name and user.validate_password(password):
            login_user(user)
            flash("Login success.")
            return redirect(url_for('index'))

        flash('Inavlid username or password.')
        return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Good bye.')
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('index'))

        title = request.form.get('title')
        year = request.form.get('year')

        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('index'))

        movie = Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        flash('Item create.')
        return redirect(url_for('index'))

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

@app.route('/movie/edit/<int:movie_id>', methods=['POST','GET'])
@login_required
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':
        title = request.form.get('title')
        year = request.form.get('Year')


        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input')
            return redirect(url_for('edit', movie_id=movie_id))

        movie.title = title
        movie.year = year
        db.session.commit()
        flash('Item update')
        return redirect(url_for('index'))    
    return render_template('edit.html', movie=movie) 

@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
@login_required
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted')
    return redirect(url_for('index'))

@app.route('/settings', methods=['POST', 'GET'])
@login_required
def setting():
    if request.method == 'POST':
        name = request.form.get('name')

        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('setting'))

        current_user.name = name
        db.session.commit()
        flash("Setting update.")
        return redirect(url_for('index'))
    
    return render_template('settings.html')


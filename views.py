from watchlist.app import app, db
from watchlist.models import Cuser, Movie 
from flask_login import logout_user, current_user, login_required, login_user
from flask import render_template, request, redirect, flash
from flask import url_for


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
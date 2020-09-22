from watchlist import app, db
from watchlist.models import Cuser, Movie
import click

@app.cli.command()
def forge():
    db.drop_all()
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

from watchlist.models import Cuser
from flask import render_template
from watchlist import app

@app.errorhandler(404)
def page_not_found(e):
    user = Cuser.query.first()
    return render_template('404.html') 
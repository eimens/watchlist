import sys
import os
from flask_login import LoginManager
from watchlist.models import Cuser
from watchlist.app import app, db



login_manager = LoginManager(app)

@app.context_processor
def inject_user():
    user = Cuser.query.first()
    return dict(user=user)

@login_manager.user_loader
def load_user(user_id):
    user = Cuser.query.get(int(user_id))
    return user

login_manager.login_view = 'login' 

from watchlist import views, errors, commands 
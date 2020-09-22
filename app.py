from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

prefix = 'sqlite:////'
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['SECRET_KEY'] = 'dev'

db = SQLAlchemy(app)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from os.path import join, dirname, realpath

app = Flask(__name__)
app.secret_key = 'some_secret'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['LOCAL'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
if app.config['LOCAL']:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'testDB.db')
    key_file = open(join(dirname(realpath(__file__))[0:-12], "keyfile.txt"))
    key_lib = []
    for line in key_file.readlines():
        key_lib.append(line.split("="))
    app.config['KEY_ID'] = key_lib[0][1][0:-1]
    app.config['KEY_ACCESS'] = key_lib[1][1]
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    app.config['KEY_ID'] = os.environ['AWS_ACCESS_KEY_ID']
    app.config['KEY_ACCESS'] = os.environ['AWS_SECRET_ACCESS_KEY']
db = SQLAlchemy(app)

from app import views

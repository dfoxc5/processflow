from flask import Flask

app = Flask(__name__)
app.secret_key = 'some_secret'

from app import views

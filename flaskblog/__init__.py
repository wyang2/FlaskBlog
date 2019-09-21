from flask_sqlalchemy import SQLAlchemy
from flask import Flask



app = Flask(__name__)

secret_key = 'a835e1d85a7157bd0e3cf3722fd7acfa'
app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

from flaskblog import route

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os



app = Flask(__name__)

secret_key = 'a835e1d85a7157bd0e3cf3722fd7acfa'
app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
db.create_all()
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' #redirect to login page
app.config['MAIL_SERVER']='smtp.googlemail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_TLS']=True
# app.config['MAIL_USERNAME'] = 'w.yangcanada@gmail.com'
# app.config['MAIL_PASSWORD'] = 'yangwenhan@321'
app.config['MAIL_USERNAME']=os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD']=os.environ.get('EMAIL_PASSWORD')
mail = Mail(app)

from flaskblog import route

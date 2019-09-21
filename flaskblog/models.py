from flaskblog import db #import db in __init__.py
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique = True, nullable = False)
    username = db.Column(db.String(20), unique = True, nullable = False)
    image = db.Column(db.String(20), default = 'default.jpg', nullable = False)
    password = db.Column(db.String(60), nullable = False)
    posts = db.relationship('Post',backref = 'author', lazy = True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.username}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable = False)
    date = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
            return f"Post('{self.title}','{self.date}')"
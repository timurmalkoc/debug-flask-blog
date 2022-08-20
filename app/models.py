from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(150), nullable = False, unique = True)
    email = db.Column(db.String(150), nullable = False, unique = True)
    password = db.Column(db.String(256), nullable = False)
    post = db.relationship('Post', backref = 'author', lazy = 'dynamic')

    def __init__(self,username,email,password):
        self.username = username
        self.email = email
        self.password = self.set_password(password)
        db.session.add(self)
        db.session.commit()

    def set_password(self,password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password,password)

    def __repr__(self):
        return f'{self.username} has been created with {self.email}'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200))
    content = db.Column(db.String(300))
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    def __init__(self,title,content,user_id):
        self.title = title
        self.content = content
        self.user_id = user_id
        db.session.add(self)
        db.session.commit()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key in {'title','content','user_id'}:
                setattr(self,key,value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'The title of the post is {self.title} \n and the content is {self.content}.'
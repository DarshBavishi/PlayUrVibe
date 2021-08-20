from music_player import db,login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    # Create a table in the db
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    mood = db.Column(db.String(10),nullable = False, default = 'happy')
    def __init__(self, email, username, password):
        self.email = email
        self.username = username

        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"UserName: {self.username}"


class Feedback(db.Model):
    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), index=True)
    name = db.Column(db.String(64), index=True)
    subject = db.Column(db.String(64), index=True)

    def __init__(self, email, name, subject):
        self.email = email
        self.name = name
        self.subject = subject


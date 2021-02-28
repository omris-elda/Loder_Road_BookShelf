from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    password_hash = db.Column(db.String(128))

    about_me = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default = datetime.utcnow)

    books = db.relationship("Book", backref = "owner", lazy = "dynamic")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User {}>".format(self.username)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return "https://www.gravatar.com/avatar/{}?d=identicon&s={}".format(digest, size)
        # this adds avatars based on your email address
    
    def get_id(self):
        return(self.user_id)
        # This is required because I'm using user_id instead of just id, and so
        # the login form isn't so happy.

class Book(db.Model):
    book_id = db.Column(db.Integer, primary_key = True)
    book_title = db.Column(db.String(64), index = True, unique = True)
    book_author = db.Column(db.String(64), index = True)
    book_owner = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    book_genre = db.Column(db.Integer, db.ForeignKey("genre.genre_id"))
    book_description = db.Column(db.String(140))
 # availability
    def __repr__(self):
        return "<Title: {}\n\r".format(self.book_title)

class Genre(db.Model):
    genre_id = db.Column(db.Integer, primary_key = True)
    genre_name = db.Column(db.String(64), unique = True, index = True)

    book_genre = db.relationship("Book", backref = "genre", lazy = "dynamic")

    def __repr__(self):
        return "<Genre: {}\n\r".format(self.genre_name)
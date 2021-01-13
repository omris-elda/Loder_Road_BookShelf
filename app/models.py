from datetime import datetime
from app import db
from flask_login import UserMixin
from app import login
from werkzeug.security import generate_password_hash, check_password_hash

@login.user_loader
def load_user(id):
    return User.Query.get(int(id))

"""
This is the user table model, which defines the table within the database.
Some of the fields have restraints on them, such as the unique, which means
that every entry has to be unique and cannot be duplicated within the database,
as well as the index restraint which allows them to be searched a bit more easily.
While that's not very important for such a small application, for bigger apps 
it can speed up search functions significantly.
"""
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(60), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return "<User {}>".format(self.username)

"""
This is the genre model to create the genre table in the database.
It has a relationship with the book table, allowing for easy cross-referencing.
"""
class Genre(db.Model):
    genre_id = db.Column(db.Integer, primary_key = True)
    genre_name = db.Column(db.String(100), index = True, unique = True)

    book = db.relationship("Book", backref="genre", lazy = "dynamic")

    def __repr__(self):
        return "<Genre: {}>\n\r".format(self.genre_name)

"""
This is the books model used to create the book table in the database.
This is quite simple, utilizing a foreign key from the Genre table to allow for easy
searching and cross-referencing
"""
class Book(db.Model):
    book_id = db.Column(db.Integer, primary_key = True)
    book_title = db.Column(db.String(50), index = True, unique = True)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.genre_id"))
    book_description = db.Column(db.String(500))
    book_availability = 
from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError, Length
from app.models import User, Genre, Book

"""
USER FORMS
"""
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email Address", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user is not None:
            raise ValidationError("This username is already in use, please select another.")
        # makes sure there's no duplicate usernames

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("This email is already in use, please use another.")
        # makes sure there's no duplicate emails

class EditProfileForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    about_me = TextAreaField("About Me", validators=[Length(min=0, max = 128)])
    submit = SubmitField("Submit")

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError("This username is already in use, please use another.")
    # These two functions both are so that the user can keep their original usernames when they
    # edit their profiles without it causing an error

"""
GENRE FORMS
"""

class AddGenreForm(FlaskForm):
    genre_name = StringField("Genre", validators=[DataRequired()])
    submit = SubmitField("Add Genre")

    def validate_genre(self, genre_name):
        genre = Genre.query.filter_by(genre_name = genre_name.data).first()
        if genre is not None:
            raise ValidationError("This genre is already in use, please select another.")
        # makes sure there's no duplicate usernames

class EditGenreForm(FlaskForm):
    genre_name = StringField("Genre", validators=[DataRequired()])
    submit = SubmitField("Submit")

"""
BOOK FORMS
"""
class AddBookForm(FlaskForm):
    book_title = StringField("Title", validators=[DataRequired()])
    book_author = StringField("Author", validators=[DataRequired()])
    # book_owner
    book_genre = SelectField("Genre", choices=[])
    book_description = TextAreaField("Description", validators=[Length(min=0, max=140)])
    submit = SubmitField("Submit")

class EditBookForm(FlaskForm):
    book_title = StringField("Title", validators=[DataRequired()])
    book_author = StringField("Author", validators=[DataRequired()])
    # book_owner
    book_genre = SelectField("Genre", choices=[])
    book_description = TextAreaField("Description", validators=[Length(min=0, max=140)])
    submit = SubmitField("Submit")

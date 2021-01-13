from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User, Books
from flask_login import current_user

"""
This is the design for the login form.
Not a lot of validation is needed here, as it's not adding anything to the database
"""
class LoginForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired()])
    password = PasswordField("Password", validators = [DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")

"""
This is the registration form, which will not really be used hopefully!
Even so, I've added a little validation to avoid duplications just in case this ever gets used
in the future.
"""
class RegisterForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired()])
    email = StringField("Email Address", validators = [DataRequired()])
    password = PasswordField("Password", validators = [DataRequired()])
    password2 = PasswordField("Repeat Password", validators = [DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.Query.filter_by(username = username.data).first()
        if user is not None:
            raise ValidationError("Username already in use.")
        # This just makes sure that there can't be duplciated usernames
    
    def validate_email(self, email):
        user = user.query.filter_by(email = email.data).first()
        if user is not None:
            raise ValidationError("Email is already in use.")
        # This just makes sure that the same email cannot be used to make multiple accounts

"""
This is the edit profile form, it's very basic as I don't think it's really going to be used
very much, but it's here just in case we wish to expand upon it in later times.
"""
class EditProfileForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired()])
    email = StringField("Email", validators = [DataRequired()])
    submit = SubmitField("Edit Account")
    
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()
            if user is not None:
                raise ValidationError("Email is already in use.")
            # This makes sure that you can't change your email to an email that's
            # already in use

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()
            if user is not None:
                raise ValidationError("Username is already in use.")
            # This makes sure that you can't change your username to
            # a username that's already in use

"""
This is the form to add a genre, allowing a relational refference to the
genre when adding books, and saving repeated data entry/deviance from the norm
"""
class AddGenre(FlaskForm):
    genre = StringField("Genre", validators = [DataRequired()])
    submit = SubmitField("Add Genre")

    def validate_genre(self, genre):
        genre = Genre.query.filter_by(genre = genre.data).first()
        if genre is not None:
            raise ValidationError("This genre already exists in the database")

"""
This is the form to edit a genre, in the event of a misspelling or similar
"""
class EditGenre(FlaskForm):
    genre = StringField("Genre", validators = [DataRequired()])
    submit = SubmitField("Edit Genre")

    def validate_genre(self, genre):
        genre = Genre.query.filter_by(genre = genre.data).first()
        if genre != self.genre:
            if genre:
                raise ValidationError("The genre already exists.")

"""
This is the form to add a new book to the database. There is some validation to ensure there are
no duplications.
"""
class AddBook(FlaskForm):
    book_title = StringField("Title", validators = [DataRequired()])
    book_author = StringField("Author", validators = [DataRequired()])
    book_genre1 = StringField("Genre 1", validators = [DataRequired()])
    book_genre2 = StringField("Genre 2")
    book_genre3 = StringField("Genre 3")
    book_genre4 = StringField("Genre 4")
    book_owner = StringField("Book Owner", validators = [DataRequired()])
    currently_available = BooleanField("Currently Available")
    submit = SubmitField(Add Book)

    def validate_book_title(self, book_title):
        book_title = Books.query.filter_by(book_title = book_title.data).first()
        if book_title is not None:
            raise ValidationError("A book with this title already exists.")
        # Making sure that there's no book with this title already in the database
    
    def validate_genre1(self, book_genre1):
        book_genre1 = Genre.query.filter_by(book_genre1 = book_genre1.data).first()
        if book_genre1 is None:
            raise ValidationError("Genre 1 doesn't exist or hasn't been added to the database.")
        # Making sure the genre entered exists/is spelt correctly
    
    def validate_genre2(self, book_genre2):
        book_genre2 = Genre.query.filter_by(book_genre2 = book_genre2.data).first()
        if book_genre2 is None:
            raise ValidationError("This genre doesn't exist or hasn't been added to the database.")
        # Making sure the genre entered exists/is spelt correctly

    def validate_genre3(self, book_genre3):
        book_genre3 = Genre.query.filter_by(book_genre3 = book_genre3.data).first()
        if book_genre3 is None:
            raise ValidationError("This genre doesn't exist or hasn't been added to the database.")
        # Making sure the genre entered exists/is spelt correctly
    
    def validate_genre4(self, book_genre4):
        book_genre4 = Genre.query.filter_by(book_genre4 = book_genre4.data).first()
        if book_genre4 is None:
            raise ValidationError("This genre doesn't exist or hasn't been added to the database.")
        # Making sure the genre entered exists/is spelt correctly

"""
This is to edit a book entry
"""
class EditBooks(FlaskForm):
    book_title = StringField("Title", validators = [DataRequired()])
    book_author = StringField("Author", validators = [DataRequired()])
    book_genre1 = StringField("Genre 1", validators = [DataRequired()])
    book_genre2 = StringField("Genre 2")
    book_genre3 = StringField("Genre 3")
    book_genre4 = StringField("Genre 4")
    book_owner = StringField("Book Owner", validators = [DataRequired()])
    currently_available = BooleanField("Currently Available")
    submit = SubmitField(Add Book)

    def validate_book_title(self, book_title):
        book_title = Books.query.filter_by(book_title = book_title.data).first()
        if book_title != self.book_title:
            if book_title is not None:
                raise ValidationError("A book with this title already exists.")
            # Making sure that there's no book with this title already in the database
    
    def validate_genre1(self, book_genre1):
        book_genre1 = Genre.query.filter_by(book_genre1 = book_genre1.data).first()
        if book_genre1 != self.book_genre1:
            if book_genre1 is None:
                raise ValidationError("Genre 1 doesn't exist or hasn't been added to the database.")
            # Making sure the genre entered exists/is spelt correctly
        
    def validate_genre2(self, book_genre2):
        book_genre2 = Genre.query.filter_by(book_genre2 = book_genre2.data).first()
        if book_genre2 != self.book_genre2:
            if book_genre2 is None:
                raise ValidationError("This genre doesn't exist or hasn't been added to the database.")
            # Making sure the genre entered exists/is spelt correctly

    def validate_genre3(self, book_genre3):
        book_genre3 = Genre.query.filter_by(book_genre3 = book_genre3.data).first()
        if book_genre3 != self.book_genre3:
            if book_genre3 is None:
                raise ValidationError("This genre doesn't exist or hasn't been added to the database.")
            # Making sure the genre entered exists/is spelt correctly
        
    def validate_genre4(self, book_genre4):
        book_genre4 = Genre.query.filter_by(book_genre4 = book_genre4.data).first()
        if book_genre4 != self.book_genre4:
            if book_genre4 is None:
                raise ValidationError("This genre doesn't exist or hasn't been added to the database.")
            # Making sure the genre entered exists/is spelt correctly

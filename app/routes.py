from flask_login.utils import login_required
from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import AddBookForm, LoginForm, RegistrationForm, EditProfileForm, AddGenreForm, EditBookForm, EditGenreForm
# This line imports the forms from the forms.py file
from flask_login import current_user, login_user, logout_user
from app.models import User, Book, Genre
# This line imports the database models from the models.py file
from werkzeug.urls import url_parse
from datetime import datetime

# Home page
@app.route("/")
@app.route("/index")
def index():
    books = Book.query.all()
    return render_template("index.html", title = "Home", books = books)

"""
USER ROUTES
"""

# Login page
@app.route("/login", methods = ["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
        # This makes sure that an already logged in user cannot log in again
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
        # the above four lines of code make it so that you will go back to the
        # page that you were redirected from if possible, or if not you'll 
        # be redirected to the index page.
    return render_template("users/login.html", title = "Sign In", form = form)

# Logout function
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

# Registration page
@app.route("/register", methods = ["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you're now a registered user!")
        return redirect(url_for("login"))
    return render_template("users/register.html", title = "Register", form = form)

# Users profile page
@app.route("/user/<username>")
def user(username):
    user = User.query.filter_by(username = username).first_or_404()
    books = Book.query.filter_by(book_owner = user.user_id).all()
    return render_template("users/user.html", user = user, books = books)

# This will allow the app to keep track of when the user was last logged in
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

# Edit users profile page
@app.route("/edit_profile", methods = ["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for("edit_profile"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template("users/edit_profile.html", title = "Edit Profile", form = form)

# Deleting your account and associated books
@app.route("/edit_account/delete_account/<user_id>", methods=["GET", "POST"])
@login_required
def delete_profile(user_id):
    user_id = user_id
    if current_user.is_authenticated:# and current_user.user_id == user_id:
        account = User.query.filter_by(user_id=current_user.user_id).first()
        books = Book.query.filter_by(book_owner=current_user.user_id).all()
        for book in books:
            db.session.delete(book)
        logout_user()
        db.session.delete(account)
        db.session.commit()
        flash("Your account and all associated books have been deleted")
        return redirect(url_for("register"))
    else:
        flash("You're not authorised to delete this account.")
        return redirect(url_for("index"))

"""
GENRE ROUTES
"""

# View all genres
@app.route("/view_all_genres")
def view_all_genres():
    genres = Genre.query.all()
    return render_template("genres/view_all_genres.html", genres = genres)

# View a specific genre
@app.route("/view_genre/<genre_id>")
def view_genre(genre_id):
    genre = Genre.query.filter_by(genre_id = genre_id).first()
    books = Book.query.filter_by(book_genre = genre_id).all()
    return render_template("genres/view_genre.html", title = "View Genre", genre = genre, books = books)

# Adding a new genre
@app.route("/add_genre", methods = ["GET", "POST"])
@login_required
def add_genre():
    form = AddGenreForm()
    if form.validate_on_submit():
        genre = Genre(genre_name = form.genre_name.data)
        db.session.add(genre)
        db.session.commit()
        flash("Genre added successfully")
        return redirect(url_for("view_all_genres"))
    return render_template("/genres/add_genre.html", title = "Add Genre", form = form)

# Deleting a specific genre
@app.route("/edit_genre/delete_genre/<genre_id>", methods=["GET", "POST"])
@login_required
def delete_genre(genre_id):
    genre_id = genre_id
    genre = Genre.query.filter_by(genre_id=genre_id).first()
#    books = Book.query.filter_by(genre_id=genre_id).all()
    if current_user.is_authenticated:
#        for book in books:
#            db.session.delete(book)
        db.session.delete(genre)
        db.session.commit()
        flash("Genre has been deleted")
        return redirect(url_for("add_genre"))
    else:
        return redirect(url_for("index"))

"""
BOOK ROUTES
"""

@app.route("/add_book", methods = ["GET", "POST"])
@login_required
def add_book():
    form = AddBookForm()
    form.book_genre.choices = [(genre.genre_id, genre.genre_name) for genre in Genre.query.all()]
    if form.validate_on_submit():
        book = Book(
            book_title = form.book_title.data,
            book_genre = form.book_genre.data,
            book_author = form.book_author.data,
            book_description = form.book_description.data,
            book_owner = current_user.user_id
        )
        db.session.add(book)
        db.session.commit()
        flash("Book successfully added")
        return redirect(url_for("index"))
    return render_template("books/add_book.html", title = "Add Book", form = form)

# Edit book page
@app.route("/edit_book/<book_id>", methods = ["GET", "POST"])
@login_required
def edit_book(book_id):
    form = EditBookForm(book_id)
    book = Book.query.filter_by(book_id = book_id).first()
    form.book_genre.choices = [(genre.genre_id, genre.genre_name) for genre in Genre.query.all()]
    if current_user.is_authenticated and current_user.user_id == book.owner.user_id:
        if form.validate_on_submit():
            book.book_title = form.book_title.data
            book.book_author = form.book_author.data
            book.book_description = form.book_description.data
            book.book_genre = form.book_genre.data
            db.session.commit()
            flash("Your changes have been saved.")
            return redirect(url_for("edit_book"))
        elif request.method == "GET":
            form.book_title.data = book.book_title
            form.book_author.data = book.book_author
            form.book_description.data = book.book_description
            form.book_genre.data = book.book_genre
        return render_template("books/edit_book.html", title = "Edit Book", form = form)
    else:
        flash("You cannot edit a book you do not own.")
        return redirect(url_for("index"))

# Deleting a specific book
@app.route("/edit_book/delete_book/<book_id>", methods=["GET", "POST"])
@login_required
def delete_book(book_id):
    book_id = book_id
    book = Book.query.filter_by(book_id=book_id).first()
    if current_user.is_authenticated:# and book.book_owner == current_user.user_id:
        db.session.delete(book)
        db.session.commit()
        flash("Book has been deleted")
        return redirect(url_for("add_book"))
    else:
        return redirect(url_for("index"))

@app.route("/view_book/<book_id>")
def view_book(book_id):
    book_id = book_id
    books = Book.query.filter_by(book_id=book_id).all()
    return render_template("/books/view_book.html", title = "Books", books = books)

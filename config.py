import os
from werkzeug.utils import secure_filename

basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER") or "/bookcovers"
    ALLOWED_EXTENSIONS = {"pdf"}

    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev" 
    # This provides an extra layer of security against CSRF attacks, and should be
    # gotten from an environmental variable, dev should NOT be used and is just a placeholder.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
        # This sets the database url to either an environmental variable,
        # or to a local database contained within the apps directory
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # This means that the application will not be signalled every time
    # a change is about to be made to the database.

    # Below is a lot of email stuff to make sure I get the app to email
    # me if anything goes wrong. More is done in the __init__.py file

    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 25)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS") is not None
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    ADMINS = ["edmundtheeel@gmail.com"]

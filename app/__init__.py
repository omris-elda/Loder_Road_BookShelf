from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

app = Flask(__name__)
app.config.from_object(Config) # this line gets the configurations from the Config object in the config file
db = SQLAlchemy(app) # this represents the database
migrate = Migrate(app, db) # this represents the migration engine
login = LoginManager(app)
login.login_view = "login"
# This tells the app where to go in the event that a user tries to go to a page they
# need to be logged in for without being logged in. I.E. the login page.

if not app.debug:
    if app.config["MAIL_SERVER"]:
        auth = None
        if app.config["MAIL_USERNAME"] or app.config ["MAIL_PASSWORD"]:
            auth = (app.config["MAIL_USERNAME"], app.config["MAIL_PASSWORD"])
        secure = None
        if app.config["MAIL_USE_TLS"]:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config["MAIL_SERVER"], app.config["MAIL_PORT"]),
            fromaddr="no-reply@" + app.config["MAIL_SERVER"],
            toaddrs=app.config["ADMINS"], subject="Loder Road Bookshelf Failure",
            credentials = auth, secure=secure
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
    # All this means that email logging will be enabled when debugging is off, and there
    # is an email server in the configuration
    if not os.path.exists("logs"):
        os.mkdir("logs")
    file_handler = RotatingFileHandler("logs/loder_road_bookshelf.log", maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("Loder Road Bookshelf Startup")
    # This makes and writes logs, which may contain errors that aren't important enough to
    # include in emails to the dev (me).
    # The file size is limited to 10kbs, and only the last 10 are being kept
    # so that not too much space is being taken up



from app import routes, models, errors
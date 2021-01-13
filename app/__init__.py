from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from os import getenv
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)

app.config.from_object(Config) # imports the config options from the config.py file
db = SQLAlchemy(app) # sets the database variable
migrate = Migrate(app, db) # this is for updating the database if we change the layout etc
bycrypt = Bcrypt(app)
login_manager = LoginManager(app) # shockingly, this manages logins
login_manager.login_view = "login"

from application import routes, models, errors
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

client = Flask(__name__)
client.config['SECRET_KEY'] = 'aeg5ncphjx6KZX4xgb'
client.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

database = SQLAlchemy(client)
bcrypt = Bcrypt(client)
login_manager = LoginManager(client)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from sitedosguri import routes
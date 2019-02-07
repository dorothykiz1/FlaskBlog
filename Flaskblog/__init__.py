from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = '79d64c304c964d793be61e7fc7696a9b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# sqlite /// specify the relative path 
# secret key for this app
# config values in our application app.config
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
# login function name for our route login
login_manager.login_message_category ='info'
#shows alert with info color
from Flaskblog import routes

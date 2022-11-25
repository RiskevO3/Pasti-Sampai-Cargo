from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__) # initiatition app for flask
bcrypt = Bcrypt(app) # initiation encrypt with bcrypt to app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pastisampai.db' # database configuration for app
app.config['SECRET_KEY'] = '749a680b784380e5dbffae5c' #configuration secret key for flask can run
db = SQLAlchemy(app) #initiation database to ap
login_manager = LoginManager(app) #initiation login manager feature from flask to app
login_manager.login_message = 'Harap login untuk melihat direktori ini!'
login_manager.login_view = "login_page" #redirect login if there is someone want access login required page
login_manager.login_message_category = "info" #flash popup category for login required directory

from pastisampai import routes #import routes for initiation to this application

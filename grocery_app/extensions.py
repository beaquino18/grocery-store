from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from grocery_app.config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

###########################
# Authentication
###########################

# Creates a login manager and initializde our app
# tells manager where to find login route which is inside the 
# auth bluepring and is called login
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from .models import User

# Tell manager how to load a user with a particular id
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# initialize Bcrypt
bcrypt = Bcrypt(app)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager



app = Flask(__name__)

app.secret_key="5fe64a01cf90509302de5ca4b0faa805"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///saggezza.db'

# database instantiation
db = SQLAlchemy(app)

# encryption instantiation
bcrypt = Bcrypt(app)

# login manager instantiation
login_manager = LoginManager(app)

# instantiation the manager for login view
# it's return on the log in page when someone try 
# to access account page from the url manually 
login_manager.login_view = 'login'

# raise the message with boostrap style
login_manager.login_message_category = 'info'

from Laconics import route, models 
from Laconics.models import User, Expense
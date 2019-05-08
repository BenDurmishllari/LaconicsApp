##########################################################################
# Project: Saggezza Expense App                                          #
# Full Stack Development: Arben Durmishllari                             #
# Second Year Student (Computer Science)                                 #
# Year: 2018-2019                                                        #
# Email: ben.durmishllari@gmail.com                                      #
# Github: BenDurmishllari                                                #
# LinkedIn: Ben Durmishllari                                             #
##########################################################################

# imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail



app = Flask(__name__)

# unique app key it's maiden only once
# will never produced the same key
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

# configs for the mails for reset passwords & send expenses 
# the 'MAIL_USERNAME' will be the mail that it will shows
# on the user always as sender for both functinalities.
# For the workablity of this function you need just to
# add an email and the correct password of this google mail,
# if for any reason this password change don't forget to
# change it and here as well.
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = True
mail = Mail(app)

from Laconics import route, models 
from Laconics.models import User, Expense
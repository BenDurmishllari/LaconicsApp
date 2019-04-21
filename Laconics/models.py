from Laconics import db, app, route, login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from flask_login import UserMixin



# Flask-Login provides user session management for Flask. 
# It handles the common tasks of logging in, logging out, 
# and remembering your users’ sessions over extended periods of time.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    employee_number = db.Column(db.String(20), unique = True, nullable = False)
    name = db.Column(db.String(120), nullable = False)
    surname = db.Column(db.String(120), nullable = False)
    email = db.Column(db.String(120), unique=True, nullable = False)
    password = db.Column(db.String(60), nullable = False)
    profile_image = db.Column(db.String(20), nullable = False, default = 'default.jpg')
    role = db.Column(db.String(20), nullable = False)
    expenses = db.relationship('Expense', backref = 'author', lazy = True)


    def get_reset_token(self, expires_sec = 600):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    

    #printed method ToString()
    def __repr__(self):
        return f"Users('{self.id}','{self.name}', '{self.surname}','{self.profile_image},'{self.expenses}'')"


class Expense(db.Model):
    expense_id = db.Column(db.Integer, primary_key = True)
    client_name = db.Column(db.String(120), nullable = False)
    client_project = db.Column(db.String(120), nullable = False)
    client_or_saggezza = db.Column(db.String(120), nullable = False)
    post_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    expenses_date = db.Column(db.DateTime, nullable=False)
    billable_to = db.Column(db.String(120), nullable = False)
    payment = db.Column(db.String(120), nullable = False)
    receipt = db.Column(db.String(120), nullable = False)
    expense_category = db.Column(db.Text, nullable = False)
    verify_or_decline = db.Column(db.String(20), nullable = True)
    GBP = db.Column(db.String(20), nullable = False)
    EUR = db.Column(db.String(20), nullable = True)
    USD = db.Column(db.String(20), nullable = True)
    receipt_image = db.Column(db.LargeBinary)
    description = db.Column(db.Text, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

     #printed method ToString()
    def __repr__(self):
        return f"Users('{self.expense_id}','{self.client_name}', '{self.client_project}', '{self.post_date},'{self.user_id}'')"

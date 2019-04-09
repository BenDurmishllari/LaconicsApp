from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.fields.html5 import DateField
from Laconics.models import User
from flask_login import current_user



class RegistrationForm(FlaskForm):
    
    employee_number = StringField('Employee Number', validators=[DataRequired(), Length(min=2, max=20)])
    
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    
    surname = StringField('Surname', validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('Email', validators=[DataRequired(), Email()])
    
    password = PasswordField('Password', validators = [DataRequired()])
    
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])

    role = SelectField ('Role', choices = [('Admin', 'Admin'), ('Manager', 'Manager'), ('User', 'User')])
    
    submit = SubmitField('Sign Up')

    # validation method to check in the database if exist the employee number 
    # to don't allow to create an account with an exist employee number
    def validate_employee_number(self, employee_number):

        user = User.query.filter_by(employee_number = employee_number.data).first()

        if user:
            raise ValidationError('This employee number belongs to another employee')
    
    # validation method to check in the database if exist the email
    # to dont allow to create a account with an exist email
    def validate_email(self, email):

        user = User.query.filter_by(email = email.data).first()

        if user:
            raise ValidationError('This email address belongs to another employee')

class LoginForm(FlaskForm):
    
    employee_number = StringField('Employee Number', validators=[DataRequired(), Length(min=2, max=20)])
    
    password = PasswordField('Password', validators = [DataRequired()])
    
    submit = SubmitField('Sign Up')


class UpdateProfileForm(FlaskForm):
     
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('Email', validators=[DataRequired(), Email()])

    picture = FileField('Update Profile Picture' , validators = [FileAllowed(['jpg','png','tiff','pdf'])])
    
    submit = SubmitField('Update')

    
    # validation method to check in the database if exist the email
    # to dont allow to update a account with an exist email
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError('This email address belongs to another employee')


class CreateExpenseForm(FlaskForm):
    
    client_name = StringField('Client Name', validators=[DataRequired()])
    
    client_project = StringField('Client Project', validators=[DataRequired()])
    
    client_or_saggezza = SelectField('Client or Saggezza:', choices = [('Saggezza UK', 'Saggezza UK'), 
                                                                       ('Saggezza US', 'Saggezza US'), 
                                                                       ('Client', 'Client')])
    
    expenses_date = DateField('Choose date of the appointment:', format='%Y-%m-%d', validators=[DataRequired()])
    
    billable_to = SelectField('Billable to client ?', choices = [('Yes', 'Yes'), ('No', 'No')])
    
    payment = SelectField('Payment Method', choices = [('Own Payment', 'Own Payment'), 
                                                       ('Corporate Card', 'Corporate Card')])
    
    receipt = SelectField('Receipt', choices = [('Yes-Soft Copy', 'Yes-Soft Copy'), 
                                                ('Yes-Hard Copy', 'Yes-Hard Copy'), 
                                                ('No-Receipt', 'No-Receipt')])
    
    description = TextAreaField('Description', validators=[DataRequired()])
    
    expense_category = SelectField('Category', choices = [('Employee Rewards', 'Employee Rewards'), 
                                                          ('Consumables', 'Consumables'), 
                                                          ('Other', 'Other')])
    
    GBP = StringField('Cost in GBP:  Required *', validators=[DataRequired()])
    EUR = StringField('Cost in EUR: (optional)')
    USD = StringField('Cost in USD: (optional)')
    
    verify_or_decline = StringField('verify or decline value')
    
    submit = SubmitField('Add Expense')
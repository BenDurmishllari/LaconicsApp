##########################################################################
# Project: Saggezza Expense App                                          #
# Full Stack Development: Arben Durmishllari                             #
# Second Year Student (Computer Science)                                 #
# Year: 2018-2019                                                        #
# Email: ben.durmishllari@gmail.com                                      #
# Github: BenDurmishllari                                                #
# LinkedIn: Ben Durmishllari                                             #
##########################################################################

# import of the wtf form, this forms
# are specif from the framework and it's give
# the flexibility to create classes for each form
# that you want to use on the system. 
# As I mention in many methods on the route.py these
# forms are connected by passing into a variable and from the html with the ({{ form.hidden_tag() }})
# so always the routes via variables knows about the form from the tag and the amount of data from the forms.py
from flask_wtf import FlaskForm

# imports type of files
from flask_wtf.file import FileField, FileAllowed

# import the form field types
from wtforms import (StringField, 
                     PasswordField, 
                     SubmitField, 
                     SelectField, 
                     TextAreaField, 
                     IntegerField, 
                     validators, 
                     FloatField)

# import validations
from wtforms.validators import (DataRequired, 
                                Length, 
                                Email, 
                                EqualTo, 
                                ValidationError)
from wtforms.fields.html5 import DateField
from Laconics.models import User, Expense

# import current_user, with this specific
# library we give the flexibility on the system
# to auto-recognize tha user that it's logged in
# and to give many oppurtunity to app on the way 
# that it's working
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
    
    submit = SubmitField('Sign In')


class UpdateProfileForm(FlaskForm):
     
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('Email', validators=[DataRequired(), Email()])

    picture = FileField('Update Profile Picture' , validators = [FileAllowed(['jpg','png','tiff','pdf'])])

    password = PasswordField('Password', validators = [DataRequired()])
    
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])
    
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
                                                          ('General Office Expenses', 'General Office Expenses'),
                                                          ('General Travel: Accommodation','General Travel: Accommodation'),
                                                          ('General Travel: Travel', 'General Travel: Travel'),
                                                          ('General Travel: Subsistence', 'General Travel: Subsistence'),
                                                          ('Sales Entertaining','Sales Entertaining'),
                                                          ('Staff Entertaining','Staff Entertaining'),
                                                          ('Recruitment fees','Recruitment fees'),
                                                          ('Visa & Immigration','Visa & Immigration'),
                                                          ('Software & IT','Software & IT'),
                                                          ('Staff Training','Staff Training'),
                                                          ('Stationery & Office Supplies','Stationery & Office Supplies'),
                                                          ('Telephone & Conference','Telephone & Conference'),
                                                          ('Other', 'Other')])
    
    GBP = FloatField('Cost in GBP:  Required *', validators=[validators.NumberRange(min=0)])
    EUR = FloatField('Cost in EUR: (optional)', validators=[validators.NumberRange(min=0)])
    USD = FloatField('Cost in USD: (optional)', validators=[validators.NumberRange(min=0)])
    
    picture_expense = FileField('Upload Receipt Image' , validators = [FileAllowed(['jpg','png','tiff'])])
    
    submit = SubmitField('Add Expense')


class Edit_expenseForm(FlaskForm):
    
    receipt = SelectField('Receipt', choices = [('Yes-Soft Copy', 'Yes-Soft Copy'), 
                                                ('Yes-Hard Copy', 'Yes-Hard Copy'), 
                                                ('No-Receipt', 'No-Receipt')])
    
    expense_category = SelectField('Category', choices = [('Employee Rewards', 'Employee Rewards'), 
                                                          ('Consumables', 'Consumables'), 
                                                          ('General Office Expenses', 'General Office Expenses'),
                                                          ('General Travel: Accommodation','General Travel: Accommodation'),
                                                          ('General Travel: Travel', 'General Travel: Travel'),
                                                          ('General Travel: Subsistence', 'General Travel: Subsistence'),
                                                          ('Sales Entertaining','Sales Entertaining'),
                                                          ('Staff Entertaining','Staff Entertaining'),
                                                          ('Recruitment fees','Recruitment fees'),
                                                          ('Visa & Immigration','Visa & Immigration'),
                                                          ('Software & IT','Software & IT'),
                                                          ('Staff Training','Staff Training'),
                                                          ('Stationery & Office Supplies','Stationery & Office Supplies'),
                                                          ('Telephone & Conference','Telephone & Conference'),
                                                          ('Other', 'Other')])
    
    client_project = StringField('Client Project', validators = [DataRequired()])
    
    client_or_saggezza = SelectField('Client or Saggezza:', choices = [('Saggezza UK', 'Saggezza UK'), 
                                                                       ('Saggezza US', 'Saggezza US'), 
                                                                       ('Client', 'Client')])
    billable_to = SelectField('Billable to client ?', choices = [('Yes', 'Yes'), ('No', 'No')])

    payment = SelectField('Payment Method', choices = [('Own Payment', 'Own Payment'), 
                                                       ('Corporate Card', 'Corporate Card')])

    submit = SubmitField('Update Expense')

class PasswordRequest(FlaskForm):
    
    mail = StringField('Email', validators = [DataRequired(), Email()])
    
    submit = SubmitField('Password Reset')

class PasswordReset(FlaskForm):
    
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm password', validators = [DataRequired(), EqualTo('password')])

    submit = SubmitField('Submit')

class SendPayroll(FlaskForm):
    
    mail = StringField('Email', validators = [DataRequired(), Email()])
    
    submit = SubmitField('Send Expense')

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
import os 
# import io
import sys
import secrets
import base64
#from io import BytesIO

# import for the image
# this library manage the
# workability of the users 
# profile image
from PIL import Image

# imports from the module
from Laconics import app, db, bcrypt, mail

# specific flask libraries
# for different workabilities
from flask import (render_template, 
                   redirect, 
                   url_for, 
                   request, 
                   flash, 
                   request, 
                   abort)

# importing all the forms 
# from the forms.py
from Laconics.forms import (RegistrationForm, 
                            UpdateProfileForm, 
                            LoginForm, 
                            CreateExpenseForm, 
                            Edit_expenseForm,
                            PasswordRequest,
                            PasswordReset,
                            SendPayroll)

# importing all the db models 
# from the models.py
from Laconics.models import User, Expense

# specific flask libraries 
# to validate and manage different
# situations on the app
from flask_login import (login_user, 
                         logout_user, 
                         login_required, 
                         current_user)

# specific flask libary for the email
# that it's helping the workability of
# the reset password, you'll find the 
# configurations on the __init__.py 
from flask_mail import Mail, Message


"""
 login route, 
 methods redirect the app
 to this route always when you access 
 the app for the first time
"""
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    
    
    # check the user if it's already log in to don't allow
    # to to go on login page
    if current_user.is_authenticated:
        return redirect(url_for('guideline'))
    
    # saving on variable the log in form
    # they communicate with form from the "form tag"
    # that you can find in all the forms on the app
    # you'll find this command in all the routes that
    # they manage forms from the app
    form = LoginForm()

    if form.validate_on_submit():
        
        user = User.query.filter_by(employee_number = form.employee_number.data).first()
        
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
                        
                        
                        # this line of code give the access for 'remember me' option in log in page
                        # I didn't add it for security reason in case if the device get lost
                        # ( remember = form.remember.data)
            
            
            # this functionality it direct you always
            # on guideline page after of the log in.
            # it's an important step for the system to know
            # which is the direction after of the log in
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('guideline'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
   
    return render_template('login.html', 
                            title='Login', 
                            form=form)



# you'll find the 'login_required' in all the routes of the system, 
# it doesn't allowed to access any page without log in
@app.route('/guideline')
@login_required 
def guideline():
    return render_template('guideline.html', 
                            title='guideline')

# route to view the list of the user,
# this functionality it's available only for the admin account 
@app.route('/users', methods=['GET', 'POST'])
@login_required
def users():

    users = User.query.all()

    return render_template('users.html', 
                            title='Users', 
                            users=users)
                            

# this route it's show the users profiles,
# it's receive the full details from the db by id
# this functionality it's available only for the admin account 
@app.route('/userprofile/<int:id>')
def userprofile(id):
    
    user = User.query.get_or_404(id)

    profile_image = url_for('static', filename = 'profile_pic/' + user.profile_image)
    

    return render_template('users_profile.html', 
                            user=user, 
                            profile_image=profile_image)
                            


# This method will work only when the account that you want
# to delete it doesn't have any exist expense on this author
@app.route('/userprofile/<int:id>/delete', methods=['POST'])
def delete_user(id):
    
    # try-except to dont allowed to delete a user 
    # profile when its still exist expense for this author
    try:

        user = User.query.get_or_404(id)

        if current_user.role != 'Admin':
            abort(403)
        db.session.delete(user)
        db.session.commit()
        flash('Employee account has been deleted', 'success')
        return redirect(url_for('users'))
    
    except:
        flash('You can"t delete this account expenses still exist for this author', 'danger')
        return redirect(url_for('users'))



@app.route('/register', methods=['GET', 'POST'])
# @login_required
def register():
    
    
    # saving on variable the register form
    # you'll find this form on forms.py
    form = RegistrationForm()
    
    if form.validate_on_submit():

        # hash password, functinality
        # from the flask libraries you'll find it
        # on __init__.py
        hased_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        # creating the user object
        user = User(employee_number = form.employee_number.data, 
                    name = form.name.data,
                    surname = form.surname.data, 
                    email = form.email.data, 
                    password = hased_password, 
                    role = form.role.data)
        
        
        db.session.add(user)
        db.session.commit()
        
        flash('Employee account has been created', 'success')
        return redirect(url_for('guideline'))
    
    # if statment to check the role of current user
    # if the role is univen of admin
    # it doesn't allowe you to access it.
    # if current_user.role != 'Admin':
    #     abort(403)
    return render_template('register.html', 
                            title='Register', 
                            form=form)  


# logout route, it's redirect you
# on log in page
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))



"""
 This function it's save the pictures and it's rename and giving secret characters to the images
 that this characters are unique for each user. Also, it's resize the pictures
 that the user's upload on their profile in 256 pixel to save space and quality.
"""
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, file_extension = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + file_extension
    picture_path = os.path.join(app.root_path, 'static/profile_pic', picture_filename)

    picture_outputSize = (256, 256)
    image = Image.open(form_picture)
    image.thumbnail(picture_outputSize)
    image.save(picture_path)

    return picture_filename


# route for the personal profile page 
# on this page they have access only the current user
# that its log in 
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    

    # saving on variable the upldate profile form
    # you'll find this form on forms.py
    form = UpdateProfileForm()
    


    # on this functionality users have the access
    # to update details of their info like name/email/password also, 
    # to upload profile picture this method it's connect with the method 
    # above I have more descriptions above the profile picture functionality above
    if form.validate_on_submit():
        
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.profile_image = picture_file
        current_user.name = form.name.data
        current_user.email = form.email.data
        hased_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        current_user.password = hased_password
        db.session.commit()
        flash('Your profile info has been updated', 'success')
    
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
    profile_image = url_for('static', filename = 'profile_pic/' + current_user.profile_image)
    
    return render_template('profile.html', 
                            title='Account', 
                            profile_image = profile_image, 
                            form = form)
                            



# route for the expenses, this fuctionality it's show 
# all the expenses that they own on current user
# all the user can view their own expenses on the 
# expenses option on the navigation bar
@app.route('/expenses', methods=['GET', 'POST'])
@login_required
def expenses():

    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    
    return render_template('expenses.html', 
                            title='Expenses', 
                            expenses=expenses)


# route for the reports, this fuctionality it's show
# all the expenses of the users only manager and admin accounts
# have access for this. If the current user role is 'Manager' or 'Admin'
# you can see the report option on the navigation bar otherwise this option is hiding.
@app.route('/reports', methods=['GET', 'POST'])
@login_required
def reports():

    expenses = Expense.query.all()
    
    # if statment to be sure that if the 
    # normal user try to access it the system will not
    # allowed them
    if current_user.role == 'User':
        abort(403)
    
    return render_template('reports.html', 
                            title='Reports', 
                            expenses=expenses)
    
# route for the creation of the expenses
@app.route('/create_expense/new', methods=['GET', 'POST'])
@login_required
def new_expense():

    # saving on variable the upldate create expense form
    # you'll find this form on forms.py
    form = CreateExpenseForm()

    if form.validate_on_submit():

        # try for the creating of the expenses object
        # I use this way because I set it to add on the database
        # the receipt image as BLOB so the 'file' variable that you'll
        # see after whatever it's reading it's send it on the database
        # and it's creating the object including the receipt image.
        # I use this way to manage this case of the 
        # receipt image cause I wanted the full quality of the picture to be readable 
        # and after when they delete the expense to remove it with the expense as part of it,
        # to save space and to don't fill the db space with past files.

        # except case is when the users create an expense without receipt image 
        # to allow the system to create the object without this attribute.
        try:
            
            
            file = request.files['picture_expense']      
            
            expense = Expense(client_name = form.client_name.data, 
                              client_project = form.client_project.data,
                              client_or_saggezza = form.client_or_saggezza.data, 
                              expenses_date = form.expenses_date.data, 
                              billable_to = form.billable_to.data, 
                              payment = form.payment.data, 
                              receipt = form.receipt.data, 
                              expense_category = form.expense_category.data,  
                              GBP = form.GBP.data, 
                              EUR = form.EUR.data, 
                              USD = form.USD.data, 
                              receipt_image = file.read(),
                              description = form.description.data,
                              author = current_user)
            expense.verify_or_decline = 'Pending'
            db.session.add(expense)
            db.session.commit()
        
        except:
            expense = Expense(client_name = form.client_name.data, 
                              client_project = form.client_project.data,
                              client_or_saggezza = form.client_or_saggezza.data, 
                              expenses_date = form.expenses_date.data, 
                              billable_to = form.billable_to.data, 
                              payment = form.payment.data, 
                              receipt = form.receipt.data, 
                              expense_category = form.expense_category.data,  
                              GBP = form.GBP.data, 
                              EUR = form.EUR.data, 
                              USD = form.USD.data,
                              description = form.description.data,
                              author = current_user)
            expense.verify_or_decline = 'Pending'
            db.session.add(expense)
            db.session.commit()

        flash('Your expense has been created', 'success')
        return redirect(url_for('expenses'))
    return render_template('create_expense.html', 
                            title='New Expense', 
                            form=form)


# route for the expenses profile
# this route it's taking the expense id 
# and it's display the expense with full details.
@app.route('/expensesprofile/<int:expense_id>')
def expensesprofile(expense_id):
    
    try:

        expense = Expense.query.get_or_404(expense_id)
        
        # as I mention above the receipt images are saving 
        # on the database as BLOB type, this variable it's decoding
        # the images by using base64. I decode it and pass this variable into html with
        # jinja to display the picture. I use this way to manage this case of the 
        # receipt image cause I wanted the full quality of the picture to be readable 
        # and after when they delete the expense to remove it with the expense as part of it
        # to save space and to don't fill the db space with past files.
        image = base64.b64encode(expense.receipt_image)

        return render_template('expensesprofile.html', 
                                expense=expense, 
                                client_name=expense.client_name, 
                                image=image.decode('utf-8')) 
    
    except:
        
        expense = Expense.query.get_or_404(expense_id)
        
        return render_template('expensesprofile.html', 
                                expense=expense, 
                                client_name=expense.client_name)

# route for the expense status, this route
# change the status of pending to verify also, it's accessable
# only from the manager account as is the only role that 
# the jinja on html display this buttons.
@app.route('/expensesprofile/<int:expense_id>/verify', methods=['GET', 'POST'])
def verify(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    expense.verify_or_decline = 'Verify'
    db.session.commit()
    flash('Expense has been verified', 'success')
    return redirect(url_for('reports'))
    if current_user.role != 'Manager':
        abort(403)
    return render_template('expenses.html', 
                            title='Expenses', 
                            expense=expense)


# route for the expense status, this route
# change the status of pending to decline also, it's accessable
# only from the manager account as is the only role that 
# the jinja on html display this buttons.
@app.route('/expensesprofile/<int:expense_id>/decline', methods=['GET', 'POST'])
def decline(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    expense.verify_or_decline = 'Decline'
    db.session.commit()
    flash('Expense has been declined', 'success')
    return redirect(url_for('reports'))
    if current_user.role != 'Manager':
        abort(403)
    return render_template('expenses.html', 
                            title='Expenses', 
                            expense=expense)

# route for the edit expense, this functionality is availabe
# only for the admin account and when an expense is on pending status
@app.route('/expensesprofile/<int:expense_id>/edit', methods=['GET', 'POST'])
def edit_expense(expense_id):
    
    expense = Expense.query.get_or_404(expense_id)
    form = Edit_expenseForm()

    # adding the changes on the db
    if form.validate_on_submit():
        expense.receipt = form.receipt.data
        expense.expense_category = form.expense_category.data
        expense.client_project = form.client_project.data
        expense.client_or_saggezza = form.client_or_saggezza.data
        expense.billable_to = form.billable_to.data
        expense.payment = form.payment.data
        db.session.commit()
        flash('Expense has been updated', 'success')
        return redirect(url_for('expensesprofile', expense_id=expense.expense_id))
    
    # keeping the details that are same
    elif request.method == 'GET':
        form.receipt.data = expense.receipt
        form.expense_category.data = expense.expense_category
        form.client_project.data = expense.client_project
        form.client_or_saggezza.data = expense.client_or_saggezza
        form.billable_to.data = expense.billable_to
        form.payment.data = expense.payment
    
    if current_user.role != 'Admin':
        abort(403)
    
    return render_template('edit_expense.html', 
                            title='Edit Expense', 
                            form=form, 
                            expense=expense)

# route for the delete expense, this fuctionality is available
# only for the admin account and it's deleting the whole expense
# from the db by taking the expense id
@app.route('/expensesprofile/<int:expense_id>/delete', methods=['POST'])
def delete_expense(expense_id):
    
    expense = Expense.query.get_or_404(expense_id)

    # again we check for security reason
    # if the account role is Admin to give 
    # access of this functionality
    if current_user.role != 'Admin':
        abort(403)
    db.session.delete(expense)
    db.session.commit()
    flash('Expense has been deleted', 'success')
    return redirect(url_for('reports'))


# method for the email that the users receive
# to reset their password via email, this method use 
# the secret token character are always unique for any 
# email that it will send it. Also, I set up the token to expire
# after of 15 minutes for security reason you'll find those method
# on the models.py into the user class etc. Finally on sender you need
# to pass the email of main email that you'll set on mail(username) config on __init__.py
def reset_email(user):
    token = user.get_reset_token()
    message = Message('Request to reset your password',
                       sender = 'ben.durmishllari@gmail.com', 
                       recipients = [user.email])
    
    # into the mail body users will receive a link that it's start with
    # the direction of 'reset_password.html' that it's the page with the form
    # that it will allowed the user to set the new pass, after it's the token 
    # characters as I mention above. All that are creating a link that it's
    # give to user a safty way to change his password via email.
    message.body = f''' Please click on link bellow to reset your password:
{url_for('change_password', token=token, _external=True)}

    This is an email to reset your password if you didn't make this request ignore this email and contact the administrator
    '''

    mail.send(message)

# route for reset password via email that it's pass the user on a form
# to input email. This functionality it's checking into database if this 
# email exist on register user and if it's true it's sending the above mail 
# to reset the passowrd.
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():

    if current_user.is_authenticated:
        return redirect(url_for('guideline'))
    
    form = PasswordRequest()
    if form.validate_on_submit():
        
        user = User.query.filter_by(email=form.mail.data).first()
        
        try:
            reset_email(user)
            flash('Email for reset password has been sended', 'info')
        except:
            flash('This email does not exist to register user!!', 'info')
            return redirect(url_for('login'))
    
    return render_template('reset_request.html', 
                            title='Reset Password', 
                            form=form)

# route for the change password, this route it's render
# when the user click on the link that receive on the email
# and it's giving the access to set the new password, this data
# are replace into dabatase by giving the access to log in with
# the new password.
@app.route('/change_password/<token>', methods=['GET', 'POST'])
def change_password(token):
    if current_user.is_authenticated:
        return redirect('guideline')
    user = User.verify_reset_token(token)

    # if the link its expires the system
    # it doesn't recognize the token so it's understand that this
    # user might not exist or the mail is expired.
    if user is None:
        flash('This user might not exist or this email has been expired', 'danger')
        return redirect(url_for('reset_password'))
    
    form = PasswordReset()
    if form.validate_on_submit():
        hased_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hased_password
        db.session.commit()
        flash('Your password has been reseted', 'success')
        return redirect(url_for('login'))
    return render_template('reset_password.html', 
                            title = 'Change Password', 
                            form=form)



# method of the expense that it's sending via email
# when the expense it has verify status. This method is connected with
# send_expense() by passing the expense id to know wich expense has to send.
# This method have one requirement to work, admin needs to create a virtual
# account and to set as email the email of the payment department of the company
# and after to pass on the 'user' variable the possition that this account has on the
# database. With this way we pass on the recepient the email of the company payment department,
# users needs only to know the email of the payment department and to fill when it will render 
# the form that it's asking for the email of the payment department. Finally on sender you need
# to pass the email of main email that you'll set on mail(username) config on __init__.py
def expensemail(expense_id):
    user = User.query.get(2)
    expense = Expense.query.get_or_404(expense_id)
    message = Message('Expense Request',
                       sender = 'ben.durmishllari@gmail.com',
                       recipients = [user.email])
    message.body = ('Expense ID: ' + str(expense.expense_id) + '\n' + '\n'
                 + 'Expense Status: ' + expense.verify_or_decline + '\n' + '\n'
                 + 'Expense Author Employee Number: '  + expense.author.employee_number + '\n' + '\n'
                 + 'Expense Author Full Name: ' + expense.author.name + '\t' +  expense.author.surname + '\n' + '\n'
                 + 'Expense Author Email: ' + expense.author.email + '\n' + '\n'
                 + '\n'
                 + '\n'
                 + '------------------------------- Expense Info -------------------------------' + '\n'
                 + '\n' 
                 + '\n'
                 + 'Client Name: ' + expense.client_name + '\n' + '\n'
                 + 'Client: ' + expense.client_or_saggezza + '\n' + '\n'
                 + 'Category: ' + expense.expense_category + '\n' + '\n'
                 + 'Payment: ' + expense.payment + '\n' + '\n'
                 + 'Expense Date: ' + str(expense.expenses_date.strftime('%d-%m-%Y')) + '\n' + '\n'
                 + 'Receipt: ' + expense.receipt + '\n' + '\n'
                 + 'Client Project: ' + expense.client_project  +'\n' + '\n'
                 + 'Billable to client: ' + expense.billable_to +'\n' + '\n'
                 + 'Amount GBP: ' + str(expense.GBP) + ' £ ' + '\n' + '\n'
                 + 'Amount EUR: ' + str(expense.EUR) + ' € '+ '\n' + '\n'
                 + 'Amount USD: ' + str(expense.USD) + ' $ '+ '\n' + '\n'
                 + 'Expense Description: ' + expense.description)

    mail.send(message)


# route for send expense via email, this method will direct users
# on a form to fill the email of the company payment department. The only 
# requirement for this fuctionality is that the users need to know the email of the
# payment department because as I mention above the app will check into database if this
# email exist.
@app.route('/send_expense/<int:expense_id>/sendexpense', methods=['GET', 'POST'])
@login_required
def send_expense(expense_id):
    
    expense = Expense.query.get_or_404(expense_id)

    form = SendPayroll()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.mail.data).first()
        expensemail(expense_id)
        flash('Your expense has been sent', 'info')
        return redirect(url_for('expenses'))
    
    return render_template('send_expense.html', 
                            title='Send Expense', 
                            form=form)


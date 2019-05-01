##########################################################################
# Project: Saggezza Expense App                                          #
# Full Stack Development: Arben Durmishllari, University of Sunderland   #
# Second Year Student (Computer Science)                                 #
# Year: 2018-2019                                                        #
# Email: ben.durmishllari@gmail.com                                      #
# Linkedin: Ben Durmishllari                                             #
# Github: BenDurmishllari                                                #
##########################################################################



"""
 libraries
"""
import os 
import io
import sys
import secrets
import base64
#from io import BytesIO
from PIL import Image
from Laconics import app, db, bcrypt, mail
from flask import (render_template, 
                   redirect, 
                   url_for, 
                   request, 
                   flash, 
                   request, 
                   abort)
from Laconics.forms import (RegistrationForm, 
                            UpdateProfileForm, 
                            LoginForm, 
                            CreateExpenseForm, 
                            Edit_expenseForm,
                            PasswordRequest,
                            PasswordReset)
from Laconics.models import User, Expense
from flask_login import (login_user, 
                         logout_user, 
                         login_required, 
                         current_user)
from flask_mail import Mail, Message


"""
 login route, methods helping to
 redirect the app when its running on the log in always
"""
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    
    # check the user if it's already log in to don't allow
    # to to go on login page
    """
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    """

    form=LoginForm()

    if form.validate_on_submit():
        
        user = User.query.filter_by(employee_number = form.employee_number.data).first()
        
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
                        # this line of code give the access for 'remember me' option in log in page
                        # I didn't add it for security reason ( remember = form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
   
    return render_template('login.html', 
                            title='Login', 
                            form=form)




@app.route('/home')
def home():
    return render_template('home.html', 
                            title='Home')


@app.route('/users', methods=['GET', 'POST'])
def users():

    users = User.query.all()

    return render_template('users.html', 
                            title='Users', 
                            users=users)
                            


@app.route('/userprofile/<int:id>')
def userprofile(id):
    
    user = User.query.get_or_404(id)
    
    profile_image = url_for('static', filename = 'profile_pic/' + user.profile_image)


    return render_template('users_profile.html', 
                            user=user, 
                            name=user.name, 
                            surname=user.surname, 
                            profile_image=profile_image)
                            


"""
 This method will work only when the account that you want
 to delete it doesn't have any exist expense
"""
@app.route('/userprofile/<int:id>/delete', methods=['POST'])
def delete_user(id):
    
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
def register():
    
    # check the user if it's already log in to don't allow
    # to to go on register page
    """
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    """

    form = RegistrationForm()
    
    if form.validate_on_submit():
        hased_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        user = User(employee_number = form.employee_number.data, 
                    name = form.name.data,
                    surname = form.surname.data, 
                    email = form.email.data, 
                    password = hased_password, 
                    role = form.role.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Employee account has been created', 'success')
        return redirect(url_for('home'))
    # if current_user.role != 'Admin':
    #     abort(403)
    return render_template('register.html', 
                            title='Register', 
                            form=form)  



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))



"""
 This function it's save the pictures and it's giving secret characters to the images
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


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    
    form = UpdateProfileForm()
    
    if form.validate_on_submit():
        

        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.profile_image = picture_file
        current_user.name = form.name.data
        current_user.email = form.email.data
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
                            




@app.route('/expenses', methods=['GET', 'POST'])
@login_required
def expenses():

    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    
    return render_template('expenses.html', 
                            title='Expenses', 
                            expenses=expenses)



@app.route('/reports', methods=['GET', 'POST'])
def reports():
    expenses = Expense.query.all()
    if current_user.role == 'User':
        abort(403)
    return render_template('reports.html', 
                            title='Reports', 
                            expenses=expenses)
    

@app.route('/create_expense/new', methods=['GET', 'POST'])
@login_required
def new_expense():

    form = CreateExpenseForm()

    if form.validate_on_submit():

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
                              receipt_image=file.read(),
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


@app.route('/expensesprofile/<int:expense_id>')
def expensesprofile(expense_id):
    
    try:

        expense = Expense.query.get_or_404(expense_id)
        
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


@app.route('/expensesprofile/<int:expense_id>/edit', methods=['GET', 'POST'])
def edit_expense(expense_id):
    
    expense = Expense.query.get_or_404(expense_id)
    form = Edit_expenseForm()

   
    if form.validate_on_submit():
        expense.client_project = form.client_project.data
        expense.client_or_saggezza = form.client_or_saggezza.data
        db.session.commit()
        flash('Expense has been updated', 'success')
        return redirect(url_for('expensesprofile', expense_id=expense.expense_id))
    elif request.method == 'GET':
        form.client_project.data = expense.client_project
        form.client_or_saggezza.data = expense.client_or_saggezza
    if current_user.role != 'Admin':
        abort(403)
    return render_template('edit_expense.html', 
                            title='Edit Expense', 
                            form=form, 
                            expense=expense)


@app.route('/expensesprofile/<int:expense_id>/delete', methods=['POST'])
def delete_expense(expense_id):
    
    expense = Expense.query.get_or_404(expense_id)

    if current_user.role != 'Admin':
        abort(403)
    db.session.delete(expense)
    db.session.commit()
    flash('Expense has been deleted', 'success')
    return redirect(url_for('reports'))


def reset_email(user):
    token = user.get_reset_token()
    message = Message('Request to reset your password',
                       sender = 'ben.durmishllari@gmail.com',
                       recipients = [user.email])
    message.body = f''' Please click on link bellow to reset your password:
{url_for('change_password', token=token, _external=True)}

    This is an email to reset your password if you don't make this request void this email and contact with the administrator
    '''

    mail.send(message)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():

    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = PasswordRequest()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.mail.data).first()
        reset_email(user)
        flash('Email for reset password has been sended', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', 
                            title='Reset Password', 
                            form=form)


@app.route('/change_password/<token>', methods=['GET', 'POST'])
def change_password(token):
    if current_user.is_authenticated:
        return redirect('home')
    user = User.verify_reset_token(token)

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





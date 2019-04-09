import os 
import secrets
from PIL import Image
from Laconics import app, db, bcrypt
from flask import render_template, redirect, url_for, request, flash, request
from Laconics.forms import RegistrationForm, UpdateProfileForm, LoginForm, CreateExpenseForm
from Laconics.models import User, Expense
from flask_login import login_user, logout_user, login_required, current_user


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
   
    return render_template('login.html', title='Login', form=form)




@app.route('/home')
def home():
    return render_template('home.html', title='Home')

@app.route('/reports')
def reports():
    expenses = Expense.query.all()
    return render_template('reports.html', title='Reports', expenses=expenses)



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
    return render_template('register.html', title='Register', form=form)  

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))



"""
 This function it's save the pictures and it's giving secret characters to the images
 that this characters are unique for each user. Also, it's rezile the pictures
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
    expenses = Expense.query.all()
    return render_template('expenses.html', title='Expenses', expenses=expenses)
    

@app.route('/create_expense/new', methods=['GET', 'POST'])
@login_required
def new_expense():

    form = CreateExpenseForm()

    if form.validate_on_submit():
        expense = Expense(client_name = form.client_name.data, 
                          client_project = form.client_project.data,
                          client_or_saggezza = form.client_or_saggezza.data, 
                          expenses_date = form.expenses_date.data, 
                          billable_to = form.billable_to.data, 
                          payment = form.payment.data, 
                          receipt = form.receipt.data, 
                          expense_category = form.expense_category.data, 
                          verify_or_decline = form.verify_or_decline.data, 
                          GBP = form.GBP.data, 
                          EUR = form.EUR.data, 
                          USD = form.USD.data, 
                          description = form.description.data,
                          author = current_user)
        
        db.session.add(expense)
        db.session.commit()
        flash('Your expense has been created', 'success')
        return redirect(url_for('home'))
    return render_template('create_expense.html', title='New Expense', form=form)



# Third Party Imports
from flask import Flask, request, render_template, flash, redirect, url_for, session
from passlib.hash import pbkdf2_sha256
import datetime
from functools import wraps
import pymysql
from secrets import token_urlsafe
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# Local Imports
from app import app, db
from app.forms import *

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['login']
        if user == 'student':
            return redirect('/studentLogin')
        elif user == 'faculty':
            return redirect('/facultyLogin')
    elif request.method == 'GET':
        return render_template('login.html')


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first to access this page.")
            return redirect('/login')
    return wrap

def require_role(role):
    def decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            if 'role' in session:
                if session['role'] == role:
                    return func(*args, **kwargs)
                elif session['role'] == 'admin':
                    return func(*args, **kwargs)
                else:
                    msg = ''
                    url = ''
                    if session['role'] == 'student':
                        msg = 'You need to be logged in as admin to access this page.'
                        url = '/studentDashboard'
                    elif session['role'] == 'faculty':
                        msg = 'You need to be logged in as admin to access this page.'
                        url = '/facultyDashboard'
                    flash(msg)
                    return redirect(url)
            else:
                flash('You need to be logged in to access this page.')
                return redirect('/login')
        return wrapped_function
    return decorator



@app.route('/courseCategoryInsertion', methods=['GET', 'POST'])
@login_required
@require_role(role='admin')
def courseCategoryInsertion():
    form = CourseCategoryInsertionForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            print('noooooooooo')
            return render_template('course/courseCategoryInsertion.html', form = form)
        else:
            category_name = form.category_name.data
            print(category_name)
            cursor = db.cursor()
            sql = "SELECT category_name FROM course_category WHERE category_name = '{}';".format(category_name)
            cursor.execute(sql)
            db_category = cursor.fetchone()
            if db_category:
                flash('The Category already exists.')
                return render_template('course/courseCategoryInsertion.html', form = form)
            else:
                try:
                    cursor.execute("INSERT INTO course_category (category_name) VALUES ('{}')".format(category_name))
                    db.commit()
                    flash("New Category {} successfully Inserted!".format(category_name))
                except:
                    flash('Error in Inserting new Category.')
                    return render_template('course/courseCategoryInsertion.html', form = form)
            return redirect('/adminDashboard')
    
    elif request.method == 'GET':
        return render_template('course/courseCategoryInsertion.html', form = form)



def insertCourse(form, course_name, duration, credits, platform, category_id):
    try:
        cursor = db.cursor()
        sql = \
        '''INSERT INTO Course (course_name,credits,duration,platform,category_id) 
        VALUES ('{}', {}, '{}', '{}', {});'''.format(course_name, credits, duration, platform, category_id)
        cursor.execute(sql)
        db.commit()
        flash("Course Inserted successfully.")
    except:
        flash('Error in Inserting new Course.')
        return render_template('course/courseInsertion.html', form = form)


@app.route('/courseInsertion', methods=['GET', 'POST'])
@login_required
@require_role(role='admin')
def courseInsertion():
    form = CourseInsertForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            print('noooooooooo')
            return render_template('course/courseInsertion.html', form = form)
        else:
            course_name = form.course_name.data
            print(course_name)
            duration = form.duration.data
            duration = "%d:00:00" % (duration)
            print(duration)
            credits = form.credits.data
            platform = form.platform.data
            category = int(form.category.data)
            insertCourse(form, course_name, duration, credits, platform, category)
            return redirect('/adminDashboard')
    
    elif request.method == 'GET':
        return render_template('course/courseInsertion.html', form = form)


@app.route('/add-department', methods=['GET', 'POST'])
@login_required
@require_role(role='admin')
def add_department():
    form = AddDepartmentForm()
    if request.method == 'POST':
        dept_name = str(form.dept_name.data)
        cursor = db.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT dept_name FROM Department WHERE dept_name = '{}';".format(dept_name)
        cursor.execute(sql)
        db_deptname = cursor.fetchall()
        if db_deptname:
            flash('The Department Already Exists!')
            return render_template('admin/add_department.html', form=form)
        else:
            sql = "INSERT INTO DEPARTMENT (dept_name) VALUES ('{}') ;".format(dept_name)
            cursor.execute(sql)
            db.commit()
            flash('Successfully Inserted new Department name {}'.format(dept_name))
            return redirect('adminDashboard')
    elif request.method == 'GET':
        return render_template('admin/add_department.html', form=form)

@app.route('/add-branch', methods=['GET', 'POST'])
@login_required
@require_role(role='admin')
def add_branch():
    form = AddBranchForm()
    if request.method == 'POST':
        branch_name = str(form.branch_name.data)
        cursor = db.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT branch_name FROM Branch WHERE branch_name = '{}';".format(branch_name)
        cursor.execute(sql)
        db_branchname = cursor.fetchall()
        if db_branchname:
            flash('The Branch Already Exists!')
            return render_template('admin/add_branch.html', form=form)
        else:
            sql = "INSERT INTO Branch (branch_name) VALUES ('{}') ;".format(branch_name)
            cursor.execute(sql)
            db.commit()
            flash('Successfully Inserted new Branch {}'.format(branch_name))
            return redirect('adminDashboard')
    elif request.method == 'GET':
        return render_template('admin/add_branch.html', form=form)

def change_password(form, account_type, account_id):
        table_name, id_column, url = '', '', ''
        if account_type == 'student':
            table_name = 'Student'
            id_column = 'Student.student_id'
            url = '/studentProfile'
        elif account_type == 'faculty':
            table_name = 'Faculty'
            id_column = 'Faculty.faculty_id'
            url = '/facultyProfile'
        elif account_type == 'admin':
            table_name = 'Admin'
            id_column = 'Admin.admin_id'
            url = '/adminProfile'
        else:
            flash('Invalid account type!')
            flash('Login Again with a valid account')
            return redirect('/logout')
        
        try:
            old_password = form.old_password.data
            new_password = form.new_password.data
            cursor = db.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT password FROM {} WHERE {} = {};".format(table_name, id_column, account_id))
            print('Pointt 2222')
            db_Oldpassword = cursor.fetchone()
            if db_Oldpassword:
                db_Oldpassword = db_Oldpassword['password']
            else:
                raise Exception('')
            print('poinyyy3')
            print(url)
            print(id_column)
            print(table_name)
            print('pointtt44444')
            try:
                print('kdwnealj')
                if pbkdf2_sha256.verify(old_password, db_Oldpassword):
                    print('pointtt555555')
                    new_password = str(pbkdf2_sha256.hash(new_password))
                    sql = "UPDATE {} SET password = '{}' WHERE {} = {};".format(table_name, new_password, id_column, account_id)
                    cursor.execute(sql)
                    db.commit()
                    flash('Successfully changed the password!')
                    return redirect(url)
                else:
                    flash('The Old Password is Incorrect.')
                    return redirect(url)
            except:
                flash('Error in Changing the password')
                return redirect(url)
        except:
            flash('Error in changing Password')
            return redirect(url)
        return redirect('/logout')

def send_mail(email_id, token):
    host = 'smtp.gmail.com'
    port = 587 
    username = 'akiffdev@gmail.com'
    password = 'akifhasanap'
    
    message = MIMEMultipart()
    message['From'] = username
    message['To'] = email_id
    message['Subject'] = 'Password Reset'
    html = \
    '''
    <html>
        <body>
            <p>Your Password reset token for Edunix is: &nbsp;<b>{}</b></p>
        </body>
    </html>
    '''.format(token)
    body = html
    message.attach(MIMEText(body, 'html'))
    server = smtplib.SMTP(host, port)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username, password)
    text = message.as_string()
    server.sendmail(username, email_id, text)
    server.quit()

@app.route('/forgot-password', methods=['GET','POST'])
def forgot_password():
    form = PasswordResetForm()
    if request.method == 'POST':
        email_id = str(form.email.data)
        acc_type = int(form.account_type.data)
        account = ""
        if(acc_type == 1):
            account = "Student"
        elif acc_type == 2:
            account = "Faculty"
        token = token_urlsafe(16)
        try:
            cursor = db.cursor(pymysql.cursors.DictCursor)
            sql = "SELECT email FROM {} WHERE email='{}';".format(account, email_id)
            cursor.execute(sql)
            data = cursor.fetchone()
            if data:
                send_mail(email_id, token)
                try:
                    sql = "INSERT INTO Password_Reset (token, email, acc_type) VALUES ('{}', '{}', {});".format(token, email_id, acc_type)
                    cursor.execute(sql)
                    db.commit()
                except:
                    flash("Error")
                    return render_template('forgot_password.html', form=form)
                print(acc_type, email_id)
                flash("Password Reset token sent successfully. Enter the token to change your password.")
                return redirect('/password-reset')
            else:
                flash("No account registered with the entered email id. Please enter a valid email id.")
                return render_template('forgot_password.html', form=form)
        except:
            flash("Error")
            return render_template('forgot_password.html', form=form)
    elif request.method == 'GET':
        return render_template('forgot_password.html', form=form)

@app.route('/password-reset', methods=['GET', 'POST'])
def password_reset():
    form = PasswordTokenForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            print('noooooooooo')
            return render_template('password_reset.html', form = form)
        else:
            email_id = str(form.email.data)
            acc_type = int(form.account_type.data)
            token = str(form.token.data)
            password =  str(pbkdf2_sha256.hash(form.new_password.data))
            try:
                cursor = db.cursor(pymysql.cursors.DictCursor)
                sql = "SELECT token FROM Password_Reset WHERE email = '{}' AND acc_type = {};".format(email_id, acc_type)
                cursor.execute(sql)
                db_token = cursor.fetchone()['token']
                print(db_token)
                if db_token:
                    if db_token == token:
                        try:
                            account = ""
                            if(acc_type == 1):
                                account = "Student"
                            elif acc_type == 2:
                                account = "Faculty"
                            sql = "UPDATE {} SET password = '{}' WHERE email = '{}';".format(account, password, email_id)
                            cursor.execute(sql)
                            sql = "DELETE FROM Password_Reset WHERE email = '{}' AND acc_type = {}".format(email_id, acc_type)
                            cursor.execute(sql)
                            db.commit()
                            flash('Successfully changed the password. Login to continue!')
                            return redirect('/login')
                        except:
                            flash("Error in changing the password. Please try again later!")
                            return render_template('password_reset.html', form=form)
                        flash("Success")
                        return render_template('password_reset.html', form=form)
                    else:
                        flash("Invalid Token. Please enter a valid one.")
                        return render_template('password_reset.html', form=form)
                else:
                    flash("No token found in the database for the given account.")
                    return render_template('password_reset.html', form=form)
            except:
                flash("Error")
                return render_template('password_reset.html', form=form)
    elif request.method == 'GET':
        return render_template('password_reset.html', form=form)
        
    pass

@app.route('/logout', methods= ['GET', 'POST'])
@login_required
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('role', None)
    flash('You have successfully logged out.')
    return redirect('/login')


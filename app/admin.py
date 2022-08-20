# Third Party Imports
from flask import Flask, request, render_template, flash, redirect, url_for, session
from passlib.hash import pbkdf2_sha256
import datetime
from functools import wraps
import pymysql.cursors


# Local Imports
from app import app, db
from app.forms import *
from app.controllers import login_required, require_role, change_password





@app.route('/adminDashboard', methods = ['GET', 'POST'])
@login_required
@require_role(role="admin")
def adminDashboard():
    if request.method == 'POST':
        return ''
    elif request.method == 'GET':
        return render_template('admin/admin_dashboard.html')



def get_admin_info(admin_id):
    cursor = db.cursor(pymysql.cursors.DictCursor)
    print('Pointt555')
    sql = \
    '''SELECT admin_name, username, email 
    FROM Admin WHERE Admin.admin_id = {};'''.format(admin_id)
    cursor.execute(sql)
    profile = cursor.fetchone()
    print(profile)
    return profile


@app.route('/adminProfile', methods=['GET', 'POST'])
@login_required
@require_role(role='admin')
def admin_profile():
    form = FacultyPasswordChangeForm()
    if request.method == 'POST':
        account_type = session['role']
        account_id = int(session['id'])
        profile = get_admin_info(session['id'])
        if form.validate() == False:
            flash('All fields are required.')
            print('dkwn') 
            return render_template('admin/admin_profile.html', form=form, profile=profile)
        else:
            change_password(form, account_type, account_id)
            return render_template('admin/admin_profile.html', profile=profile, form=form)
    elif request.method == 'GET':
        try:
            admin_id = session['id']
            profile = get_admin_info(admin_id)
            print(profile)
            return render_template('admin/admin_profile.html', profile=profile, form=form)
        except:
            flash('Error in retrieveing Profile Information')
            return render_template('admin/admin_profile.html', form=form)


@app.route('/adminLogin', methods= ['GET', 'POST'])
def adminLogin():
    form = AdminLoginForm()

    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            print('noooooooooo')
            return render_template('admin/adminLogin.html', form=form)
        else:
            username = form.username.data
            password = form.password.data
            sql = "SELECT admin_id, username, password FROM Admin WHERE username='{}'".format(username)
            cursor = db.cursor()
            cursor.execute(sql)
            data = cursor.fetchone()
            if data == None:
                flash('No such Username exists. Please login with a valid username.')
                print('Noneeeeeeeee')
                return render_template('admin/adminLogin.html', form=form)
                
            else:
                dbID, dbUsername, dbPassword = data[0], data[1], data[2]
                print(dbID)
                try:
                    if pbkdf2_sha256.verify(password, dbPassword):
                        session['logged_in'] = True
                        session['id'] = dbID
                        session['username'] = username
                        session['role'] = 'admin'
                        flash("You have logged in successfully as {}.".format(username))
                        return redirect('/adminDashboard')
                    else:
                        flash('Incorrect Password')
                        return render_template('admin/adminLogin.html', form=form)
                except:
                    flash('Incorrect Password.')
                    return render_template('admin/adminLogin.html', form=form)
                    
    elif request.method == 'GET':
        return render_template('admin/adminLogin.html', form=form)


@app.route('/delete-course/<int:course_id>,<course_name>', methods= ['GET', 'POST'])
@login_required
@require_role(role='admin')
def delete_course(course_id, course_name):
    try:
        cursor = db.cursor(pymysql.cursors.DictCursor)
        sql = "DELETE FROM Course WHERE course_id = {};".format(course_id)
        cursor.execute(sql)
        db.commit()
        flash('Successfully deleted the course {}.'.format(course_name))
        return redirect('/admin-courses')
    except:
        flash('Unable to delete the course {}'.format(course_name))
        return redirect('/admin-courses')

@app.route('/edit-course/<int:course_id>', methods=['GET', 'POST'])
@login_required
@require_role(role='admin')
def edit_course(course_id):
    form = CourseUpdationForm()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        course_name = str(form.course_name.data)
        credits = int(form.credits.data)
        platform = str(form.platform.data)
        category_id = int(form.category.data)
        sql = \
        '''UPDATE Course SET course_name = '{}', credits={}, platform='{}', category_id={} 
        WHERE course_id = {};'''.format(course_name, credits, platform, category_id, course_id)
        cursor.execute(sql)
        db.commit()
        flash('Successfully edited the course {}.'.format(course_name))
        return redirect('/admin-courses')
    elif request.method == 'GET':
        try:
            
            sql = \
            '''
            SELECT course_id, course_name, credits, duration, platform, Course_Category.category_name 
            FROM Course JOIN Course_Category ON Course.category_id = Course_Category.category_id 
            WHERE course_id = {};'''.format(course_id)
            cursor.execute(sql)
            course = cursor.fetchone()
            print(course)
            course_name, credits, duration, platform, category_name = course['course_name'], course['credits'], course['duration'], course['platform'], course['category_name']
            return render_template('course/edit_course.html', form=form, course=course, course_name=course_name, \
                credits=credits, duration=duration, platform=platform,course_id=course_id, category_name=category_name)
        except:
            flash('Unable to fetch the course details!')
            return redirect('/admin-courses')
        

@app.route('/view-faculties', methods=['GET', 'POST'])
@login_required
@require_role(role='admin')
def view_faculties():
    cursor = db.cursor(pymysql.cursors.DictCursor)
    if request.method == 'GET':
        sql = \
        '''SELECT faculty_id, faculty_name, username, university_id, email, phno, Department.dept_name  
        FROM Faculty JOIN Department ON Faculty.dept_id = Department.dept_id'''
        cursor.execute(sql)
        faculties = cursor.fetchall()
        print(faculties)
        return render_template('admin/view_faculties.html', faculties=faculties)


@app.route('/admin-courses', methods=['GET', 'POST'])
@login_required
@require_role(role='admin')
def courses():
    form = SelectCategory()
    if request.method == 'POST':
        category_id = int(form.category.data)
        print(category_id)
        cursor = db.cursor(pymysql.cursors.DictCursor)
        if category_id == 0:
            sql = \
            '''
            SELECT course_id, course_name, credits, duration, platform, category_name 
            FROM Course JOIN Course_Category ON Course.category_id = Course_Category.category_id;
            '''
            cursor.execute(sql)
        else:
            sql = \
            '''
            SELECT course_id, course_name, credits, duration, platform, category_name 
            FROM Course JOIN Course_Category ON Course.category_id = Course_Category.category_id WHERE Course.category_id = {}; 
            '''.format(category_id)
            cursor.execute(sql)
        courses = cursor.fetchall()
        return render_template('admin/courses.html', form=form, courses=courses)
    
    elif request.method == 'GET':
        cursor = db.cursor(pymysql.cursors.DictCursor)
        sql = \
        '''
        SELECT course_id, course_name, credits, duration, platform, category_name 
        FROM Course JOIN Course_Category ON Course.category_id = Course_Category.category_id;
        '''
        cursor.execute(sql)
        courses = cursor.fetchall()
        print(courses)
        return render_template('admin/courses.html', courses=courses, form=form)


def insertAdmin(form, name, username, password, email):
    try:
        cursor = db.cursor()
        sql = "INSERT INTO Admin (admin_name, username, password, email) VALUES ('{}', '{}', '{}', '{}');".format(name, username, password, email)
        cursor.execute(sql)
        db.commit()
        flash('Account created successfully! Login to continue.')
        
    except:
        flash('Error in creating the account. Please Try Again')
        return render_template('admin/adminRegistration.html', form = form)


@app.route('/adminRegistration', methods= ['GET', 'POST'])
@require_role(role='admin')
def adminRegistration():
    form = AdminRegistrationForm()

    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            print('nooooooooooooo')
            return render_template('admin/adminRegistration.html', form=form)
        else:
            username = form.username.data
            email = form.email.data
            cursor = db.cursor()
            cursor.execute("SELECT username FROM Admin WHERE username='{}';".format(username))
            dbUsername = cursor.fetchone()
            # print(dbUsername)
            cursor.execute("SELECT email FROM Admin WHERE email='{}';".format(email))
            dbEmail = cursor.fetchone()
            # print(dbEmail)
            if dbUsername:
                flash('The username {} already exists.Please try a different username.'.format(dbUsername))
                return render_template('admin/adminRegistration.html', form = form)
            elif dbEmail:
                flash('The email {} already exists.Please try a different email.'.format(dbEmail))
                return render_template('admin/adminRegistration.html', form = form)
            else:
                name = form.name.data
                password =  str(pbkdf2_sha256.hash(form.password.data))
                insertAdmin(form, name, username, password, email)
                return redirect('/login')

    elif request.method == 'GET':
        return render_template('admin/adminRegistration.html', form=form)
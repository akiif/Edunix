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



@app.route('/studentDashboard', methods= ['GET', 'POST'])
@require_role(role='student')
def studentDashboard():
    if request.method == 'POST':
        return ''
    elif request.method == 'GET':
        # return render_template('student/studentDashboard.html')
        return redirect('viewEnrolled')


def get_student_info(student_id):
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = \
    '''SELECT student_name, username, university_id, email, dob, phno, age_calc.Age, courses_enrolled, semester, Branch.branch_name  
    FROM Student JOIN Branch JOIN age_calc ON Student.branch_id = Branch.branch_id AND Student.student_id = age_calc.student_id
    WHERE Student.student_id = {};'''.format(student_id)
    cursor.execute(sql)
    profile = cursor.fetchone()
    return profile

@app.route('/studentProfile', methods=['GET', 'POST'])
@login_required
@require_role(role='student')
def student_profile():
    form = PasswordChangeForm()
    if request.method == 'POST':
        account_type = session['role']
        account_id = int(session['id'])
        profile = get_student_info(session['id'])
        if form.validate() == False:
            flash('All fields are required.')
            print('dkwn') 
            return render_template('student/student_profile.html', form=form, profile=profile)
        else:
            change_password(form, account_type, account_id)
            return render_template('student/student_profile.html', profile=profile, form=form)
    elif request.method == 'GET':
        try:
            student_id = session['id']
            profile = get_student_info(student_id)
            print(profile)
            return render_template('student/student_profile.html', profile=profile, form=form)
        except:
            flash('Error in retrieveing Profile Information')
            return render_template('student/student_profile.html', form=form)


@app.route('/viewEnrolled', methods = ['GET', 'POST'])
@login_required
@require_role(role='student')
def viewEnrolled():
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        try:
            student_id = session['id']
            cursor = db.cursor(pymysql.cursors.DictCursor)
            sql = \
            '''SELECT enrollment.course_id, course.course_name, course.credits, 
            course.duration, course_category.category_name category, Enrollment.enroll_date 
            FROM Enrollment
            JOIN Course JOIN course_category ON 
            Enrollment.course_id = Course.course_id 
            AND 
            Course.category_id = course_category.category_id WHERE Enrollment.student_id = {};'''.format(student_id)
            cursor.execute(sql)
            enrolls = cursor.fetchall()
            sql = "SELECT courses_enrolled FROM Student WHERE student_id = {};".format(student_id)
            cursor.execute(sql)
            total_enrolled = cursor.fetchone()['courses_enrolled']
            return render_template('student/view_enrolled.html', enrolls=enrolls, total_enrolled=total_enrolled)  
        except:
            flash("Error")
            return render_template('student/view_enrolled.html')    


@app.route('/unenroll/<int:course_id>', methods = ['GET', 'POST'])
@login_required
@require_role(role='student')
def unenroll(course_id):
    try:
        student_id = session['id']
        print(course_id)
        cursor = db.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT course_name FROM Course WHERE course_id = {}".format(course_id)
        cursor.execute(sql)
        course_name = cursor.fetchone()['course_name']
        print(course_id)
        sql = "DELETE FROM Enrollment WHERE student_id = {} AND course_id = {};".format(student_id, course_id)
        cursor.execute(sql)
        db.commit()
        flash('Successfully unenrolled from the course {}'.format(course_name))
        return redirect('/viewEnrolled')
    except:
        flash('Unable to unernroll.')
        return redirect('/viewEnrolled')


@app.route('/enrollCourses', methods= ['GET', 'POST'])
@require_role(role='student')
def enrollCourses():
    form = SelectCategory()
    if request.method == 'POST':
        category_id = int(form.category.data)
        print(category_id)
        cursor = db.cursor()
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
        return render_template('student/enroll_courses.html', form=form, courses=courses)

    elif request.method == 'GET':
        cursor = db.cursor()
        sql = \
        '''
        SELECT course_id, course_name, credits, duration, platform, category_name 
        FROM Course JOIN Course_Category ON Course.category_id = Course_Category.category_id;
        '''
        cursor.execute(sql)
        courses = cursor.fetchall()
        return render_template('student/enroll_courses.html', courses=courses, form=form)



@app.route('/enroll/<int:id>', methods=['GET', 'POST'])
@require_role(role='student')
def enroll(id):
    if session['role'] == 'student':
        student_id = session['id']
        sql = "SELECT student_id, course_id FROM Enrollment WHERE student_id = {} AND course_id = {}".format(student_id, id)
        cursor = db.cursor()
        cursor.execute(sql)
        enrollData = cursor.fetchone()
        cursor.execute('SELECT course_name FROM Course WHERE course_id = {}'.format(id))
        course_name = cursor.fetchone()[0]
        if enrollData:
            flash("You have already enrolled in the course ' {} '.".format(course_name))
            return redirect('/enrollCourses')
        else:
            try:
                sql = "INSERT INTO Enrollment (student_id, course_id) VALUES ({}, {});".format(student_id, id)
                cursor.execute(sql)
                db.commit()
                data = cursor.fetchone()
                flash('You have successfully enrolled in the course {}'.format(course_name))
                return redirect('/studentDashboard')
            except:
                flash('Unable to enroll in the course.')
                return redirect('/enrollCourses')
    else:
        flash('You need to be a student to enroll in a course!')
        return redirect('/')

@app.route('/studentLogin', methods= ['GET', 'POST'])
def studentLogin():
    form = StudentLoginForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            print('noooooooooo')
            return render_template('student/student_login.html', form=form)
        else:
            username = form.username.data
            password = form.password.data
            sql = "SELECT student_id, username, password FROM Student WHERE username='{}'".format(username)
            cursor = db.cursor()
            cursor.execute(sql)
            data = cursor.fetchone()
            if data == None:
                flash('No such Username exists. Please login with a valid username.')
                print('Noneeeeeeeee')
                return render_template('student/student_login.html', form=form)
                
            else:
                dbID, dbUsername, dbPassword = data[0], data[1], data[2]
                print(dbID)
                try:
                    if pbkdf2_sha256.verify(password, dbPassword):
                        session['logged_in'] = True
                        session['id'] = dbID
                        session['username'] = username
                        session['role'] = 'student'
                        flash("You have logged in successfully as {}.".format(username))
                        return redirect('/studentDashboard')
                    else:
                        flash('Incorrect Password')
                        return render_template('student/student_login.html', form=form)
                except:
                    flash('Incorrect Password.')
                    return render_template('student/student_login.html', form=form)

    elif request.method == 'GET':
        return render_template('student/student_login.html', form=form)


# Insert into the Student Table
def insertStudents(form, name, username, password, uni_id, email, phno, semester, dob, branch_id):
    try:
        print('point4444444')
        cursor = db.cursor()
        print('point555555')
        cursor.execute('''
        INSERT INTO student (student_name, university_id, username, password, email, phno, semester, dob, branch_id) 
        VALUES ('{}', '{}', '{}', '{}', '{}', '{}', {}, '{}', {});'''.format(name, uni_id, username, password, email, phno, semester, dob, branch_id))
        # print('point66666666')
        db.commit()
        # print('point777777777')
        flash('Account created successfully! Login to continue.')
    except:
        flash('Error in creating the account. Please Try Again')
        return render_template('student/studentRegistrationForm.html', form = form)

@app.route('/studentRegistration', methods = ['GET', 'POST'])
def studentRegistration():
    form = StudentRegistrationForm()
    
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            print('noooooooooo')
            return render_template('student/studentRegistrationForm.html', form = form)
        else:
            username = form.username.data
            email = form.email.data
            university_id = form.university_id.data
            cursor = db.cursor()
            cursor.execute("SELECT username FROM Student WHERE username='{}';".format(username))
            dbUsername = cursor.fetchone()
            # print(dbUsername)
            cursor.execute("SELECT email FROM Student WHERE email='{}';".format(email))
            dbEmail = cursor.fetchone()
            # print(dbEmail)
            cursor.execute("SELECT university_id FROM Student WHERE university_id='{}';".format(university_id))
            dbUniv_id = cursor.fetchone()
            # print(dbUniv_id)
            if dbUsername:
                flash('The username {} already exists.Please try a different username.'.format(dbUsername))
                return render_template('student/studentRegistrationForm.html', form = form)
            elif dbEmail:
                flash('The email {} already exists.Please try a different email.'.format(dbEmail))
                return render_template('student/studentRegistrationForm.html', form = form)
            elif dbUniv_id:
                flash("The University ID {} already exists. Please try a different University ID.".format(dbUniv_id))
                return render_template('student/studentRegistrationForm.html', form = form)
            else:
                name = form.name.data
                print('point11111')
                password =  str(pbkdf2_sha256.hash(form.password.data))
                branch_id = int(form.branch.data)
                semester = int(form.semester.data)
                phone = form.phone.data
                print('point22222222')
                dob = request.form['birthday']
                print('point3333333')
                # Insert the data from the form to the Student Table  
                insertStudents(form, name, username, password, university_id, email, phone, semester, dob, branch_id)
                return redirect('/login')
    elif request.method == 'GET':
        return render_template('student/studentRegistrationForm.html', form = form)




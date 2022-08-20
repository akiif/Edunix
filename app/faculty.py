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



@app.route('/facultyDashboard', methods= ['GET', 'POST'])
@login_required
@require_role(role='faculty')
def facultyDashboard():
    if request.method == 'POST':
        return ''
    elif request.method == 'GET':
        return redirect('/view-students')


def get_faculty_info(faculty_id):
    cursor = db.cursor(pymysql.cursors.DictCursor)
    print('Pointt555')
    sql = \
    '''SELECT faculty_name, username, university_id, email, phno, Department.dept_name  
    FROM Faculty JOIN Department ON Faculty.dept_id = Department.dept_id
    WHERE Faculty.faculty_id = {};'''.format(faculty_id)
    cursor.execute(sql)
    profile = cursor.fetchone()
    print(profile)
    return profile


@app.route('/faculty-profile', methods=['GET', 'POST'])
@login_required
@require_role(role='faculty')
def faculty_profile():
    form = FacultyPasswordChangeForm()
    if request.method == 'POST':
        account_type = session['role']
        account_id = int(session['id'])
        profile = get_faculty_info(session['id'])
        if form.validate() == False:
            flash('All fields are required.')
            print('dkwn') 
            return render_template('faculty/faculty_profile.html', form=form, profile=profile)
        else:
            change_password(form, account_type, account_id)
            return render_template('faculty/faculty_profile.html', profile=profile, form=form)
    elif request.method == 'GET':
        try:
            faculty_id = session['id']
            profile = get_faculty_info(faculty_id)
            print(profile)
            return render_template('faculty/faculty_profile.html', profile=profile, form=form)
        except:
            flash('Error in retrieveing Profile Information')
            return render_template('faculty/faculty_profile.html', form=form)


@app.route('/view-students', methods= ['GET', 'POST'])
@login_required
@require_role(role='faculty')
def viewStudents():
    form = SearchStudentForm()

    if request.method == 'POST':
        student_uni_id = form.uni_id.data
        students = []
        try:
            print(student_uni_id)
            cursor = db.cursor(pymysql.cursors.DictCursor)
            if student_uni_id == 'all':
                sql = \
                '''SELECT student_id, student_name, username, university_id, email, semester, Branch.branch_name
                FROM Student Join Branch ON Student.branch_id = Branch.branch_id;'''
                cursor.execute(sql)
            else:
                sql = \
                '''SELECT student_id, student_name, username, university_id, email, semester, Branch.branch_name
                    FROM Student Join Branch ON Student.branch_id = Branch.branch_id WHERE university_id LIKE "%{}%";'''.format(student_uni_id)
                cursor.execute(sql)
            students = cursor.fetchall()
            return render_template('faculty/view_students.html', form=form, students=students)
        except:
            flash('No such Student found with the University ID: {}'.format(student_uni_id))
            return render_template('faculty/view_students.html', form=form, students=students)
    elif request.method == 'GET':
        try:
            cursor = db.cursor(pymysql.cursors.DictCursor)
            sql = \
                '''SELECT student_id, student_name, username, university_id, email, semester, Branch.branch_name
                    FROM Student Join Branch ON Student.branch_id = Branch.branch_id;'''
            cursor.execute(sql)
            students = cursor.fetchall()
            # print(students)
            return render_template('faculty/view_students.html', form=form, students=students)
        except:
            flash('Error in fetching students.')
            return render_template('faculty/view_students.html', form=form)


@app.route('/view-student-enroll-info/<int:student_id>', methods=['GET', 'POST'])
@login_required
@require_role(role='faculty')
def view_student_enroll_info(student_id):
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        try:
            cursor = db.cursor(pymysql.cursors.DictCursor)
            print('dkjsacdmkl')
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
            # print(enrolls)
            sql = \
             '''SELECT student_name, username, university_id, email, dob, phno, courses_enrolled, semester, Branch.branch_name  
            FROM Student JOIN Branch WHERE Student.student_id = {};'''.format(student_id)
            cursor.execute(sql)
            profile = cursor.fetchone()
            # print(profile)
            return render_template('faculty/view_student_info.html', enrolls=enrolls, profile=profile) 
        except:
            flash("Error")
            return redirect('/facultyDashboard') 

@app.route('/facultyLogin', methods=['GET', 'POST'])
def facultyLogin():
    form = FacultyLoginForm()

    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            print('noooooooooo')
            return render_template('faculty/facultyLogin.html', form=form)
        else:
            username = form.username.data
            password = form.password.data
            sql = "SELECT faculty_id, username, password FROM Faculty WHERE username='{}'".format(username)
            cursor = db.cursor()
            cursor.execute(sql)
            data = cursor.fetchone()
            if data == None:
                flash('No such Username exists. Please login with a valid username.')
                print('Noneeeeeeeee')
                return render_template('faculty/facultyLogin.html', form=form)
                
            else:
                dbID, dbUsername, dbPassword = data[0], data[1], data[2]
                print(dbID)
                try:
                    if pbkdf2_sha256.verify(password, dbPassword):
                        session['logged_in'] = True
                        session['id'] = dbID
                        session['username'] = username
                        session['role'] = 'faculty'
                        flash("You have logged in successfully as {}.".format(username))
                        return redirect('/facultyDashboard')
                    else:
                        flash('Incorrect Password')
                        return render_template('faculty/facultyLogin.html', form=form)
                except:
                    flash('Incorrect Password.')
                    return render_template('faculty/facultyLogin.html', form=form)
                    
    elif request.method == 'GET':
        return render_template('faculty/facultyLogin.html', form=form)



def insertFaculty(form, name, username, password, uni_id, email, phone, dept_id):
    try:
        cursor = db.cursor()
        sql = \
        '''
        INSERT INTO FACULTY (faculty_name, username, password, email, university_id, phno, dept_id)
        VALUES ('{}', '{}', '{}', '{}', '{}', '{}', {});'''.format(name, username, password, email, uni_id, phone, dept_id)
        cursor.execute(sql)
        db.commit()
        print(cursor.fetchone())
        flash('Account with username {} created successfully. Login to continue.'.format(username))

    except:
        flash('Error creating a new faculty account. Please try again.')
        return render_template('faculty/facultyRegistrationForm.html', form = form)

@app.route('/facultyRegistration', methods= ['GET', 'POST'])
@require_role(role='faculty')
def facultyRegistration():
    form = FacultyRegistrationForm()

    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            print('nooooooooooooo')
            return render_template('faculty/facultyRegistration.html', form=form)
        else:
            username = form.username.data
            email = form.email.data
            university_id = form.university_id.data
            cursor = db.cursor()
            cursor.execute("SELECT username FROM Faculty WHERE username='{}';".format(username))
            dbUsername = cursor.fetchone()
            # print(dbUsername)
            cursor.execute("SELECT email FROM Faculty WHERE email='{}';".format(email))
            dbEmail = cursor.fetchone()
            # print(dbEmail)
            cursor.execute("SELECT university_id FROM Faculty WHERE university_id='{}';".format(university_id))
            dbUniv_id = cursor.fetchone()
            # print(dbUniv_id)
            if dbUsername:
                flash('The username {} already exists.Please try a different username.'.format(dbUsername))
                return render_template('faculty/facultyRegistration.html', form = form)
            elif dbEmail:
                flash('The email {} already exists.Please try a different email.'.format(dbEmail))
                return render_template('faculty/facultyRegistration.html', form = form)
            elif dbUniv_id:
                flash("The University ID {} already exists. Please try a different University ID.".format(dbUniv_id))
                return render_template('faculty/facultyRegistration.html', form = form)
            else:
                name = form.name.data
                password =  str(pbkdf2_sha256.hash(form.password.data))
                dept_id = int(form.department.data)
                phone = form.phone.data
                insertFaculty(form, name, username, password, university_id, email, phone, dept_id)
                return redirect('/adminDashboard')

    elif request.method == 'GET':
        return render_template('faculty/facultyRegistration.html', form=form)
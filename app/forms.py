# Third Party Imports
from flask import Flask, request, render_template, flash
from flask_wtf import Form
from wtforms import TextField, BooleanField, RadioField, StringField, PasswordField, validators, \
IntegerField, TextAreaField, SubmitField, SelectField, DateField, TimeField

# Local Imports
from app import app, db


def getBranches():
    cursor = db.cursor()
    cursor.execute('SELECT * FROM Branch;')
    branch = cursor.fetchall()
    branchList  = []
    for row in branch:
        branchList.append((row[0], row[1]))
    # print(branchList)
    return branchList


class StudentRegistrationForm(Form):
    name = StringField('Name:',[validators.DataRequired(message="Please enter your name.")])
    username = StringField('Username:', [validators.Length(min=4, max=10, message="Username must be atleast 3 and atmost 10 characters long.")])
    password = PasswordField('New Password:', [ validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match.')])
    confirm = PasswordField('Confirm Password:')
    university_id = StringField('University ID:', [validators.Length(max=10)])
    email = StringField('Email Address:', [validators.Length(min=6, max=35), validators.Email("Please enter a valid email address.")])
    phone = StringField('Phone Number:', [validators.DataRequired()])
    branch = SelectField('Branch:', choices=getBranches())
    semester = SelectField('Semester:', choices=[(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8)])
    submit = SubmitField("Register")

class StudentLoginForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=10), validators.DataRequired(message='Enter the password')])
    password = PasswordField('Password', [validators.DataRequired(message='Enter the password')])
    submit = SubmitField("Login")


def getDepartments():
    cursor = db.cursor()
    cursor.execute('SELECT * FROM Department;')
    dept = cursor.fetchall()
    deptList = []
    for row in dept:
        deptList.append((row[0], row[1]))
    return deptList

class FacultyRegistrationForm(Form):
    name = StringField('Name:', [validators.DataRequired(message="Please enter your name.")])
    username = StringField('Username:', [validators.Length(min=4, max=10, message="Username must be atleast 3 and atmost 10 characters long."), validators.Required()])
    password = PasswordField('New Password:', [ validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match.')])
    confirm = PasswordField('Confirm Password:')
    university_id = StringField('University ID:', [validators.Length(max=10)])
    email = StringField('Email Address:', [validators.Length(min=6, max=35), validators.Email("Please enter a valid email address.")])
    phone = StringField('Phone Number:', [validators.DataRequired()])
    department = SelectField('Department:', choices=getDepartments())
    submit = SubmitField("Register")
    

class FacultyLoginForm(Form):
    username = StringField('Username:', [validators.Length(min=3, max=10), validators.DataRequired('Please Enter the Username')])
    password = PasswordField('Password', [validators.DataRequired(message='Enter the password')])
    submit = SubmitField("Login")


class AdminRegistrationForm(Form):
    name = StringField('Name:', [validators.DataRequired('Please Enter your name.')])
    username = StringField('Username:', [validators.Length(min=4, max=10, message="Username must be atleast 3 and atmost 10 characters long."), validators.Required()])
    password = PasswordField('New Password:', [ validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match.')])
    confirm = PasswordField('Confirm Password:')
    email = StringField('Email Address:', [validators.Length(min=6, max=35), validators.Email('Please enter a valid email address.')])
    submit = SubmitField("Register")

class AdminLoginForm(Form):
    username = StringField('Username:', [validators.Length(min=3, max=10), validators.DataRequired('Please Enter the Username')])
    password = PasswordField('Password', [validators.DataRequired(message='Enter the password')])
    submit = SubmitField("Login")


class CourseCategoryInsertionForm(Form):
    category_name = StringField('Category:', [validators.DataRequired('Please enter the new category name.')])
    submit = SubmitField('Add Category')


def getCourseCategories():
    cursor = db.cursor()
    cursor.execute('SELECT * FROM Course_Category;')
    cat = cursor.fetchall()
    catList = []
    for row in cat:
        catList.append((row[0], row[1]))
    return catList

def allCategories():
    catList = getCourseCategories()
    catList.insert(0, (0, 'All'))
    return catList

class CourseInsertForm(Form):
    course_name = StringField('Course Name:', [validators.DataRequired('Please enter the Course Name.')])
    credits = IntegerField('Credits:', [validators.DataRequired('Please Enter the Course Credits.')])
    duration = IntegerField('Duration:')
    platform = StringField('Platform:', [validators.DataRequired('Please Enter the Course platform.')])
    category = SelectField('Category', choices=getCourseCategories())
    submit = SubmitField('Add Course')

class CourseUpdationForm(Form):
    course_name = StringField('Course Name:', [validators.DataRequired('Please enter the Course Name.')])
    credits = IntegerField('Credits:', [validators.DataRequired('Please Enter the Course Credits.')])
    duration = IntegerField('Duration:')
    platform = StringField('Platform:', [validators.DataRequired('Please Enter the Course platform.')])
    category = SelectField('Category', choices=getCourseCategories())
    submit = SubmitField('Update Course')

class AddBranchForm(Form):
    branch_name =  StringField('Branch Name:', [validators.DataRequired('Please enter the Branch Name.')])
    submit = SubmitField('Add New Branch')

class AddDepartmentForm(Form):
    dept_name = StringField('Department Name:', [validators.DataRequired('Please enter the Department Name.')])
    submit = SubmitField('Submit')

class PasswordChangeForm(Form):
    old_password = PasswordField('Old Password', [validators.DataRequired('Please Enter your Old Password:')])
    new_password = PasswordField('New Password', [validators.DataRequired('Please Enter your New Password.'), \
        validators.Length(min=4,message="The Password should be atleast 4 characters long."),\
        validators.EqualTo('confirm', message='Passwords must match.')])
    confirm = PasswordField('Confirm Password:')

class FacultyPasswordChangeForm(Form):
    old_password = PasswordField('Old Password', [validators.DataRequired('Please Enter your Old Password:')])
    new_password = PasswordField('New Password', [validators.DataRequired('Please Enter your New Password.'), \
        validators.Length(min=4,message="The Password should be atleast 4 characters long."),\
        validators.EqualTo('confirm', message='Passwords must match.')])
    confirm = PasswordField('Confirm Password:')

class SelectCategory(Form):
    category = SelectField('Category', choices=allCategories())

class SearchStudentForm(Form):
    uni_id = StringField('University ID: ', [validators.DataRequired('Please enter the university id.')])

class PasswordResetForm(Form):
    account_type = SelectField('Account Type: ', choices=[(1, 'Student'), (2, 'Faculty')])
    email = StringField('Email Address:', [validators.Length(min=6, max=35), validators.Email('Please enter a valid email address.')])
    submit = SubmitField("Submit")

class PasswordTokenForm(Form):
    account_type = SelectField('Account Type: ', choices=[(1, 'Student'), (2, 'Faculty')])
    email = StringField('Email Address:', [validators.Length(min=6, max=35), validators.Email('Please enter a valid email address.')])
    token = StringField('Token: ', [validators.DataRequired('Please enter the token.')])
    new_password = PasswordField('New Password', [validators.DataRequired('Please Enter your New Password.'), \
        validators.Length(min=4,message="The Password should be atleast 4 characters long."),\
        validators.EqualTo('confirm', message='Passwords must match.')])
    confirm = PasswordField('Confirm Password:')
    submit = SubmitField("Submit")
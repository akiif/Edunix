# Third Party Imports
from flask import Flask, request, render_template, flash, redirect
import pymysql
from functools import wraps


app = Flask(__name__)
app.secret_key = 'm6V7JXnI77LwUPuV13M4eIuIgQukIOaRm'

db = pymysql.connect(host='localhost', user='root', passwd='akif', db='edunix')

#Local Imports
from app.forms import *
from app.controllers import *
from app.student import *
from app.faculty import *
from app.admin import *

@app.errorhandler(404)
def not_found(error):
    return render_template('error_pages/404.html')


@app.errorhandler(500)
def internal_error(error):
    return render_template('error_pages/500.html')



@app.route('/')
def index():
    return redirect('/login')
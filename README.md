# Edunix

**Edunix** web app is a Course Management Database system built using the Flask micro web-framework.

## Installation

 - To run the program make sure you have a MySql (prefarrabily Xampp) server running in your system.
 - First open the database.py file and enter your host name, user and root in the  line 3 of the file:

```python
db = pymysql.connect(host='localhost', user='root', passwd='akif')
```
- Open a terminal where the edunix folder is present
```bash
$ cd edunix
```

 - Install virtualenv to make a python virtual environment using:

For Linux:
```bash
$ pip3 install virtualenv
```

For Windows:
```bash
$ pip install virtualenv
```
 - Now create a virtual environment in your project's root directory:
  
For Windows: 
```bash
PS D:\Programs\flask\edunix> py -m venv venv
``` 
 For Linux:
```bash
$ python3 -m venv venv
``` 

 - Now activate the python virtual environmet using:
 
For Windows: 
```bash
PS D:\Programs\flask\edunix> venv\scripts\activate
(venv) PS D:\Programs\flask\edunix>
``` 
> Make sure you can run scripts in your windows terminal. To be able to run the scripts you can 
> refer  [How to enable execution of PowerShell scripts?](https://superuser.com/questions/106360/how-to-enable-execution-of-powershell-scripts)
 
 For Linux:
```bash
$ . venv/bin/activate
(venv) akif@akif-VirtualBox:~/flask$ 
```
 - Now install all the python packages required to run the web app using :
```bash
(venv) PS D:\Programs\flask\edunix> pip install -r requirements.txt
```
> Use pip3 instead of pip for linux.

 - Run the python database.py to create a new database.

```bash
(venv) PS D:\Programs\flask\edunix> python database.py
(('admin',), ('age_calc',), ('branch',), ('course',), ('course_category',), ('course_teacher',), ('cteacher',), ('department',), ('enrollment',), ('faculty',), ('student',))

Database Created Successfully!
```
> Use python3 database.py for linux.
## Run
To run the program use the following command in the terminal:

```bash
(venv) $ python run.py
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 156-853-127
 * Running on http://127.0.0.1:5008/ (Press CTRL+C to quit)
```
 Now open the url [http://127.0.0.1:5008/](http://127.0.0.1:5008/) in your browser to use the web app.
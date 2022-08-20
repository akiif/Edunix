import pymysql

db = pymysql.connect(host='localhost', user='root', passwd='akif')

cursor = db.cursor()

def create_database():
    # Create a new Database 'test_3' if it dosen't already exists.
    sql = "CREATE DATABASE IF NOT EXISTS Edunix DEFAULT CHARACTER SET utf8;"
    cursor.execute(sql)

    sql = "USE Edunix;"
    cursor.execute(sql)

    # Creating Course_Category Table.
    sql = \
    '''
    CREATE TABLE IF NOT EXISTS Course_Category (
        category_id      INTEGER NOT NULL AUTO_INCREMENT,
        category_name    VARCHAR(50) NOT NULL,

        PRIMARY KEY (category_id)
        ) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;
    '''
    cursor.execute(sql)

    # Creating Course Table
    sql = \
    ''' 
    CREATE TABLE IF NOT EXISTS Course (
        course_id       INTEGER NOT NULL AUTO_INCREMENT,
        course_name     VARCHAR(80) NOT NULL,
        credits         INTEGER NOT NULL,
        duration        TIME NOT NULL,
        platform        VARCHAR(20),
        category_id     INTEGER NOT NULL,

        PRIMARY KEY (course_id),

        INDEX (course_name) USING BTREE,
        
        CONSTRAINT FOREIGN KEY (category_id) REFERENCES Course_Category (category_id)
            ON DELETE CASCADE ON UPDATE CASCADE
        
        ) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;
    '''

    cursor.execute(sql)

    # Creating CTeacher Table
    sql = \
    '''
    CREATE TABLE IF NOT EXISTS CTeacher(
        teacher_id      INTEGER NOT NULL AUTO_INCREMENT,
        teacher_name    VARCHAR(50) NOT NULL,
        phno            VARCHAR(15) NOT NULL,

        PRIMARY KEY (teacher_id)
        ) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;
    '''

    cursor.execute(sql)


    sql = \
    '''
    CREATE TABLE IF NOT EXISTS Course_Teacher (
        teacher_id      INTEGER NOT NULL,
        course_id       INTEGER NOT NULL,

        PRIMARY KEY(teacher_id, course_id),

        CONSTRAINT FOREIGN KEY (teacher_id) REFERENCES CTeacher (teacher_id)
            ON DELETE CASCADE ON UPDATE CASCADE,
        CONSTRAINT FOREIGN KEY (course_id) REFERENCES Course (course_id)
            ON DELETE CASCADE ON UPDATE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;
    '''

    cursor.execute(sql)


    sql = \
    '''
    CREATE TABLE IF NOT EXISTS Branch (
        branch_id   INTEGER NOT NULL AUTO_INCREMENT,
        branch_name VARCHAR(60) NOT NULL,

        PRIMARY KEY (branch_id)
        ) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;
    '''

    cursor.execute(sql)

    sql = \
    '''
    CREATE TABLE IF NOT EXISTS Student (
        student_id          INTEGER NOT NULL AUTO_INCREMENT,
        student_name        VARCHAR(50) NOT NULL,
        university_id       VARCHAR(10) NOT NULL,
        username            VARCHAR(10) UNIQUE NOT NULL,
        password            VARCHAR(255) NOT NULL,
        email               VARCHAR(40) NOT NULL,
        phno                VARCHAR(15) NOT NULL,
        courses_enrolled    INTEGER DEFAULT 0,
        semester            INTEGER NOT NULL,
        dob                 DATE NOT NULL,
        branch_id           INTEGER NOT NULL,

        INDEX (username),
        
        PRIMARY KEY (student_id),

        CONSTRAINT FOREIGN KEY (branch_id) REFERENCES Branch (branch_id)
            ON DELETE CASCADE ON UPDATE CASCADE

        ) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;
    '''

    cursor.execute(sql)


    sql = \
    '''
    CREATE TABLE IF NOT EXISTS Enrollment(
        student_id      INTEGER NOT NULL,
        course_id       INTEGER NOT NULL,
        enroll_date     DATE DEFAULT NOW(),

        PRIMARY KEY(student_id, course_id),

        CONSTRAINT FOREIGN KEY (student_id) REFERENCES Student (student_id)
            ON DELETE CASCADE ON UPDATE CASCADE, 
        CONSTRAINT FOREIGN KEY (course_id) REFERENCES Course (course_id)
            ON DELETE CASCADE ON UPDATE CASCADE

        ) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;
    '''

    cursor.execute(sql)

    sql = \
    '''
    CREATE TABLE IF NOT EXISTS Department (
        dept_id     INTEGER NOT NULL AUTO_INCREMENT,
        dept_name   VARCHAR(80) NOT NULL,

        PRIMARY KEY(dept_id)
        ) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;
    '''

    cursor.execute(sql)

    sql = \
    '''
    CREATE TABLE IF NOT EXISTS Faculty (
        faculty_id      INTEGER NOT NULL AUTO_INCREMENT,
        faculty_name    VARCHAR(40) NOT NULL,
        email           VARCHAR(35) NOT NULL,
        university_id   VARCHAR(15) NOT NULL,
        username        VARCHAR(10) UNIQUE NOT NULL,
        password        VARCHAR(255) NOT NULL,
        phno            VARCHAR(15) NOT NULL,
        dept_id         INTEGER NOT NULL,

        INDEX (faculty_name),

        PRIMARY KEY(faculty_id),

        CONSTRAINT FOREIGN KEY (dept_id) REFERENCES Department (dept_id)
            ON DELETE CASCADE ON UPDATE CASCADE

        ) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;
    '''

    cursor.execute(sql)

    sql = \
    '''
    CREATE TABLE IF NOT EXISTS Admin (
        admin_id    INTEGER NOT NULL AUTO_INCREMENT,
        admin_name  VARCHAR(20) NOT NULL,
        username    VARCHAR(10) UNIQUE NOT NULL,
        password    VARCHAR(255) NOT NULL,
        email       VARCHAR(35) NOT NULL,

        PRIMARY KEY (admin_id)

        ) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;
    '''

    cursor.execute(sql)

    # Table for storing password reset tokens
    sql = \
    '''
    CREATE TABLE Password_Reset (
		token VARCHAR(32),
        email VARCHAR(25),
        acc_type INT,
        PRIMARY KEY (token, email, acc_type)
        
        ) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;
    '''

    cursor.execute(sql)

    
    # -- Trigger For When a Student Enrolls in a Course
    sql = \
    '''
    CREATE OR REPLACE TRIGGER add_CourseCount
    AFTER INSERT ON Enrollment
    FOR EACH ROW
    UPDATE Student
    SET Student.courses_enrolled = Student.courses_enrolled + 1
    WHERE Student.student_id = NEW.student_id;
    '''

    cursor.execute(sql)

    # -- Trigger for when a student unenrolls from a Course
    sql = \
    '''
    CREATE OR REPLACE TRIGGER sub_CourseCount
    AFTER DELETE ON Enrollment
    FOR EACH ROW
    UPDATE Student
    SET Student.courses_enrolled = Student.courses_enrolled - 1
    WHERE Student.student_id = OLD.student_id;
    '''

    cursor.execute(sql)

    # -- View To Display Age
    sql = "CREATE VIEW age_calc AS SELECT student_id,	floor(DATEDIFF((now()),dob)/365) AS Age FROM Student;"

    cursor.execute(sql)

    sql = \
    '''
    SELECT student_name, username, university_id, email, courses_enrolled, semester, dob, age_calc.Age, Branch.branch_name
    FROM Student JOIN Branch JOIN age_calc ON Student.branch_id = Branch.branch_id AND Student.student_id = age_calc.student_id; 
    '''
    # cursor.execute(sql)


    script="SHOW TABLES;"
    cursor.execute(script)

    print(cursor.fetchall())
    print('\nDatabase Created Successfully')

if __name__ == '__main__':
    try:
        create_database()
    except:
        print('Error in creating the database.')
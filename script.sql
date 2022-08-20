CREATE TABLE IF NOT EXISTS Course_Category (
    category_id      INTEGER NOT NULL AUTO_INCREMENT,
    category_name    VARCHAR(50) NOT NULL,

    PRIMARY KEY (category_id)
    ) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;


CREATE TABLE IF NOT EXISTS Course (
    course_id       INTEGER NOT NULL AUTO_INCREMENT,
    course_name     VARCHAR(50) NOT NULL,
    credits         INTEGER NOT NULL,
    duration        TIME NOT NULL,
    platform        VARCHAR(20),
    category_id     INTEGER NOT NULL,

    PRIMARY KEY (course_id),

    INDEX (course_name) USING BTREE,
    
    CONSTRAINT FOREIGN KEY (category_id) REFERENCES Course_Category (category_id)
        ON DELETE CASCADE ON UPDATE CASCADE
    
    ) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;

CREATE TABLE IF NOT EXISTS CTeacher(
    teacher_id      INTEGER NOT NULL AUTO_INCREMENT,
    teacher_name    VARCHAR(50) NOT NULL,
    phno            VARCHAR(15) NOT NULL,

    PRIMARY KEY (teacher_id)
    ) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;


CREATE TABLE IF NOT EXISTS Course_Teacher (
    teacher_id      INTEGER NOT NULL,
    course_id       INTEGER NOT NULL,

    PRIMARY KEY(teacher_id, course_id),

    CONSTRAINT FOREIGN KEY (teacher_id) REFERENCES CTeacher (teacher_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT FOREIGN KEY (course_id) REFERENCES Course (course_id)
        ON DELETE CASCADE ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;

CREATE TABLE IF NOT EXISTS Branch (
    branch_id   INTEGER NOT NULL AUTO_INCREMENT,
    branch_name VARCHAR(50) NOT NULL,

    PRIMARY KEY (branch_id)
    ) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;

CREATE TABLE IF NOT EXISTS Student (
    student_id          INTEGER NOT NULL AUTO_INCREMENT,
    student_name        VARCHAR(40) NOT NULL,
    university_id       VARCHAR(10) NOT NULL,
    username            VARCHAR(10) UNIQUE NOT NULL,
    password            VARCHAR(255) NOT NULL,
    email               VARCHAR(35) NOT NULL,
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

CREATE TABLE IF NOT EXISTS Department (
    dept_id     INTEGER NOT NULL AUTO_INCREMENT,
    dept_name   VARCHAR(50) NOT NULL,

    PRIMARY KEY(dept_id)
    ) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;

CREATE TABLE IF NOT EXISTS Faculty (
    faculty_id      INTEGER NOT NULL AUTO_INCREMENT,
    faculty_name    VARCHAR(40) NOT NULL,
    email           VARCHAR(35) NOT NULL,
    university_id   VARCHAR(15) NOT NULL,
    username        VARCHAR(10) UNIQUE NOT NULL ,
    password        VARCHAR(255) NOT NULL,
    phno            VARCHAR(15) NOT NULL,
    dept_id         INTEGER NOT NULL,

    INDEX (faculty_name),
    INDEX (username),

    PRIMARY KEY(faculty_id),

    CONSTRAINT FOREIGN KEY (dept_id) REFERENCES Department (dept_id)
        ON DELETE CASCADE ON UPDATE CASCADE

    ) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;


CREATE TABLE IF NOT EXISTS Admin (
    admin_id    INTEGER NOT NULL AUTO_INCREMENT,
    admin_name  VARCHAR(20) NOT NULL,
    username    VARCHAR(10) UNIQUE NOT NULL,
    password    VARCHAR(255) NOT NULL,
    email       VARCHAR(35) NOT NULL,

    INDEX (username),

    PRIMARY KEY (admin_id)

    ) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;


-- Trigger For When a Student Enrolls in a Course
CREATE TRIGGER add_CourseCount
AFTER INSERT ON Enrollment
FOR EACH ROW
UPDATE Student
SET Student.courses_enrolled = Student.courses_enrolled + 1
WHERE Student.student_id = NEW.student_id;
 
-- Trigger for when a student unenrolls from a Course
CREATE TRIGGER sub_CourseCount
AFTER DELETE ON Enrollment
FOR EACH ROW
UPDATE Student
SET Student.courses_enrolled = Student.courses_enrolled - 1
WHERE Student.student_id = OLD.student_id;

-- View To Display Age
CREATE VIEW age_calc AS SELECT student_id,	floor(DATEDIFF((now()),dob)/365) AS Age FROM Student;

SELECT student_name, username, university_id, email, courses_enrolled, semester, dob, age_calc.Age, Branch.branch_name
FROM Student JOIN Branch JOIN age_calc ON Student.branch_id = Branch.branch_id AND Student.student_id = age_calc.student_id; 
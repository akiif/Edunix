-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 15, 2021 at 06:20 PM
-- Server version: 10.4.16-MariaDB
-- PHP Version: 7.4.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `edunix`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `Admin` (
  `admin_id` int(11) NOT NULL,
  `admin_name` varchar(20) NOT NULL,
  `username` varchar(10) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(35) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `admin`
--

INSERT INTO `Admin` (`admin_id`, `admin_name`, `username`, `password`, `email`) VALUES
(1, 'Akif Mohammed', 'akif', '$pbkdf2-sha256$29000$b21tDSEkJGQMAeC89z4npA$KvuKu6Y6KyrectVgNWgl5F/b6adPFy1O./Ap8Y40.DQ', 'akif.hmohd@gmail.com'),
(2, 'Sara', 'sara', '$pbkdf2-sha256$29000$VcoZQyjlvJcyBgCAkBKiNA$iSrbffSLur1znCBVqbrx0RhqwXsMQSzMOfiNsm7f7DM', 'sara.is18@sahyadri.edu.in');

-- --------------------------------------------------------


-- --------------------------------------------------------

--
-- Table structure for table `branch`
--

CREATE TABLE `Branch` (
  `branch_id` int(11) NOT NULL,
  `branch_name` varchar(60) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `branch`
--

INSERT INTO `Branch` (`branch_id`, `branch_name`) VALUES
(1, 'Information Science & Engineering'),
(2, 'Electronics & Communication Engineering'),
(3, 'Computer Science & Engineering'),
(4, 'Mechanical Engineering'),
(5, 'Civil Engineering'),
(6, 'MBA'),
(7, 'Data Science'),
(8, 'AI & Machine Learning');

-- --------------------------------------------------------

--
-- Table structure for table `course`
--

CREATE TABLE `Course` (
  `course_id` int(11) NOT NULL,
  `course_name` varchar(80) NOT NULL,
  `credits` int(11) NOT NULL,
  `duration` time NOT NULL,
  `platform` varchar(20) DEFAULT NULL,
  `category_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `course`
--

INSERT INTO `Course` (`course_id`, `course_name`, `credits`, `duration`, `platform`, `category_id`) VALUES
(1, 'Python for Everybody', 5, '10:00:00', 'Coursera', 1),
(2, 'Deep Learning', 4, '05:00:00', 'Coursera', 1),
(3, 'Applied Data Science with Python', 6, '12:00:00', 'Coursera', 1),
(4, 'Neural Networks and Deep ', 4, '08:00:00', 'Coursera', 1),
(5, 'Front-End JavaScript Frameworks', 2, '04:00:00', 'Coursera', 1),
(6, 'Introduction to HTML5', 2, '05:00:00', 'Coursera', 1),
(8, 'Virtual Reality', 2, '04:00:00', 'Coursera', 1),
(9, 'Kotlin for Java Developers', 6, '20:00:00', 'Coursera', 1),
(10, 'Data Structures and Algorithms', 8, '15:00:00', 'Coursera', 1),
(11, 'Cloud Architecture with Google', 2, '14:00:00', 'Coursera', 2),
(12, 'SRE and DevOps Engineer with Google Cloud', 5, '12:00:00', 'Coursera', 2),
(13, 'Technical Support Fundamentals', 3, '02:00:00', 'Coursera', 2),
(14, 'Cybersecurity and the X-Factor', 4, '13:00:00', 'Coursera', 2),
(15, 'Site Reliability Engineering', 2, '05:00:00', 'Coursera', 2),
(16, 'AWS Fundamentals', 1, '02:00:00', 'Coursera', 2),
(17, 'The Bits and Bytes of Computer Networking', 2, '14:00:00', 'Coursera', 2),
(18, 'IT Project Management', 2, '05:00:00', 'Coursera', 2),
(19, 'Google Cloud Security', 4, '10:00:00', 'Coursera', 2),
(20, 'Career Success', 2, '12:00:00', 'Coursera', 5),
(21, 'Financial Markets', 4, '06:00:00', 'Coursera', 5),
(22, 'Excel Skills for Buisness', 1, '05:00:00', 'Coursera', 5),
(23, 'Social Media Management', 5, '12:00:00', 'Coursera', 5),
(24, 'Digital Marketing', 2, '10:00:00', 'Coursera', 5),
(25, 'Agile Development', 3, '04:00:00', 'Coursera', 5),
(26, 'Mathematics for Machine Learning', 2, '13:00:00', 'Coursera', 7),
(27, 'Algorithmic Toolbox', 1, '04:00:00', 'Coursera', 7),
(28, 'Graphic Design', 4, '14:00:00', 'Coursera', 4),
(29, 'Creative Writing', 2, '04:00:00', 'Coursera', 4),
(30, 'UI / UX Design', 2, '16:00:00', 'Coursera', 4),
(31, 'Java Programming', 5, '20:00:00', 'Udemy', 1),
(32, 'Angular-The Complete Guide', 2, '12:00:00', 'Udemy', 1),
(33, 'React Bootcamp', 4, '13:00:00', 'Udemy', 1),
(34, 'C# Unity Game Developer', 6, '15:00:00', 'Udemy', 1),
(35, 'Learn Ethical Hacking From Scratch', 7, '16:00:00', 'Udemy', 2),
(36, 'Microsoft Excel - Data Analysis', 2, '15:00:00', 'Udemy', 8),
(37, 'The Art and Science of Drawing', 2, '06:00:00', 'Udemy', 9),
(38, 'Life Coaching Certification Course', 2, '04:00:00', 'Udemy', 11);

-- --------------------------------------------------------

--
-- Table structure for table `course_category`
--

CREATE TABLE `Course_Category` (
  `category_id` int(11) NOT NULL,
  `category_name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `course_category`
--

INSERT INTO `Course_Category` (`category_id`, `category_name`) VALUES
(1, 'Computer Science'),
(2, 'Information Technology'),
(3, 'Social Sciences'),
(4, 'Arts and Humanities'),
(5, 'Buisness'),
(6, 'Marketing'),
(7, 'Math and Logic'),
(8, 'Office Productivity'),
(9, 'Lifestyle'),
(10, 'Photography and Video'),
(11, 'Personal Development'),
(12, 'Physical Science and Engineering'),
(13, 'Language Learning'),
(14, 'Health');

-- --------------------------------------------------------

--
-- Table structure for table `department`
--

CREATE TABLE `Department` (
  `dept_id` int(11) NOT NULL,
  `dept_name` varchar(80) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `department`
--

INSERT INTO `Department` (`dept_id`, `dept_name`) VALUES
(1, 'Department Of Information Science & Engineering'),
(2, 'Department Of Computer Science & Engineering'),
(3, 'Department Of Mechanical Engineering'),
(4, 'Department Of Electronics & Communication Engineering'),
(5, 'Department Of Civil Engineering'),
(6, 'Finance Department'),
(7, 'Admission Department'),
(8, 'Sports Department');

-- --------------------------------------------------------

--
-- Table structure for table `enrollment`
--

CREATE TABLE `Enrollment` (
  `student_id` int(11) NOT NULL,
  `course_id` int(11) NOT NULL,
  `enroll_date` date DEFAULT (CURRENT_DATE)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `enrollment`
--

INSERT INTO `Enrollment` (`student_id`, `course_id`, `enroll_date`) VALUES
(1, 1, '2021-01-13'),
(1, 2, '2021-01-13'),
(1, 5, '2021-01-13'),
(1, 6, '2021-01-13'),
(1, 9, '2021-01-13'),
(1, 11, '2021-01-13'),
(1, 28, '2021-01-13'),
(2, 2, '2021-01-13'),
(2, 8, '2021-01-13'),
(2, 11, '2021-01-13'),
(2, 12, '2021-01-13'),
(3, 10, '2021-01-13'),
(3, 13, '2021-01-13'),
(3, 16, '2021-01-13'),
(4, 5, '2021-01-13'),
(4, 14, '2021-01-13'),
(4, 17, '2021-01-13'),
(5, 17, '2021-01-13'),
(5, 20, '2021-01-13'),
(6, 10, '2021-01-13'),
(6, 19, '2021-01-13'),
(6, 22, '2021-01-13'),
(7, 1, '2021-01-13'),
(7, 31, '2021-01-13'),
(8, 21, '2021-01-13'),
(8, 28, '2021-01-13'),
(9, 16, '2021-01-13'),
(9, 36, '2021-01-13'),
(9, 38, '2021-01-13'),
(10, 1, '2021-01-13'),
(10, 5, '2021-01-13'),
(11, 11, '2021-01-13'),
(11, 18, '2021-01-13'),
(11, 25, '2021-01-13'),
(12, 1, '2021-01-13'),
(13, 3, '2021-01-13'),
(13, 4, '2021-01-13'),
(14, 4, '2021-01-13'),
(14, 6, '2021-01-13'),
(14, 12, '2021-01-13');

--
-- Triggers `enrollment`
--
DELIMITER $$
CREATE TRIGGER `add_CourseCount` AFTER INSERT ON `Enrollment` FOR EACH ROW UPDATE Student
    SET Student.courses_enrolled = Student.courses_enrolled + 1
    WHERE Student.student_id = NEW.student_id
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `sub_CourseCount` AFTER DELETE ON `Enrollment` FOR EACH ROW UPDATE Student
    SET Student.courses_enrolled = Student.courses_enrolled - 1
    WHERE Student.student_id = OLD.student_id
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `faculty`
--

CREATE TABLE `Faculty` (
  `faculty_id` int(11) NOT NULL,
  `faculty_name` varchar(40) NOT NULL,
  `email` varchar(35) NOT NULL,
  `university_id` varchar(15) NOT NULL,
  `username` varchar(10) NOT NULL,
  `password` varchar(255) NOT NULL,
  `phno` varchar(15) NOT NULL,
  `dept_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `faculty`
--

INSERT INTO `Faculty` (`faculty_id`, `faculty_name`, `email`, `university_id`, `username`, `password`, `phno`, `dept_id`) VALUES
(1, 'Akif', 'akif.hmohd@gmail.com', '4FS125', 'akif', '$pbkdf2-sha256$29000$9t77X8t5DyHkvLcWQgghhA$vaUUwUbdeWsuWSWH7AzC1/5p4DBzypFx6MbhJeMlTGo', '9731311904', 1),
(2, 'Sara', 'sara.is18@sahyadri.edu.in', '4FS111', 'sara', '$pbkdf2-sha256$29000$3Ps/p7T2HuO8N.Z8z9n7fw$8RrBr6eh1vyT7vtHD9ziluBH.MOsgF8k.fCDTLNj20Q', '4846', 1),
(3, 'Michel', 'michel.is18@sahyadri.edu.in', '4FS145', 'michel', '$pbkdf2-sha256$29000$PedcSymllFIKgfAeo7TW.g$PyT4GtKUqkYQgyHeQ8zw2Wgt.75nY/ZE0S9dm.0VeGo', '462367', 2),
(4, 'Amaan', 'amaan@me.com', '4II125', 'amaan', '$pbkdf2-sha256$29000$oPReC.GcE0JobQ2h1PofYw$e7zNbT8EudMSs5CO0OA6SE82LXXtlC288LPJftQ6TZQ', '64646', 3),
(6, 'John', 'john@me.com', '4GG568', 'john', '$pbkdf2-sha256$29000$xDjnfI.RMuZcixHi/L.X8g$BTInQX1dnihc8.2bsBApASpQW.dByokJzrGqtUVQogU', '6342462', 6),
(7, 'Henriette', 'henrie@me.com', '4TY6426', 'henriette', '$pbkdf2-sha256$29000$L2UMgTDmfG9NyXnP2RsD4A$XaF8.tF7G1j1OMt9lQfOPbj4zd1LGrGNcQoDu25JwPY', '1653484', 7);

-- --------------------------------------------------------

--
-- Table structure for table `student`
--

CREATE TABLE `Student` (
  `student_id` int(11) NOT NULL,
  `student_name` varchar(50) NOT NULL,
  `university_id` varchar(10) NOT NULL,
  `username` varchar(10) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(40) NOT NULL,
  `phno` varchar(15) NOT NULL,
  `courses_enrolled` int(11) DEFAULT 0,
  `semester` int(11) NOT NULL,
  `dob` date NOT NULL,
  `branch_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `student`
--

INSERT INTO `Student` (`student_id`, `student_name`, `university_id`, `username`, `password`, `email`, `phno`, `courses_enrolled`, `semester`, `dob`, `branch_id`) VALUES
(1, 'Akif', '8IA215', 'akif', '$pbkdf2-sha256$29000$8d7be89ZS2kNYWxt7b33Pg$HOnPTspbOnU19mre44XYLkKI7D5Eq53szr9L.WIAtMA', 'akif.hmohd@gmail.com', '9731311904', 7, 5, '2000-01-26', 1),
(2, 'Sara', '8IA458', 'sara', '$pbkdf2-sha256$29000$dW5t7b13LiVkDAHg/J/zng$Ey1WRtM6sahZWnQdEU1sC4lccWQ4BtEfUL5euxpagN8', 'sara.is18@sahyadri.edu.in', '789696426', 5, 6, '2000-05-22', 2),
(3, 'Michel', '4II548', 'michel', '$pbkdf2-sha256$29000$K6VUKoVQyrl3bg0hpFTqHQ$Cbnp4fULqYZ.XVMZDbcb7uNrHBJK4CKznmYifwNTWf8', 'michel.is18@sahyadri.edu.in', '4682636', 3, 4, '2002-05-01', 3),
(4, 'Thousif', '4UI548', 'thousif', '$pbkdf2-sha256$29000$11rr/Z8T4vz/P6d0zlkL4Q$HiNOBACw4ZxFPk43OZ.8VAr3PSwgn1Ltlo1pA5XAHCI', 'thousi@me.com', '4266345', 3, 3, '1999-03-25', 4),
(5, 'Yuvraj', '4AA879', 'yuvraj', '$pbkdf2-sha256$29000$3BvD2BvjHIPQulcKYcwZow$Eg5fksObIW8eli6hsSN.VGas1/pGSzzjdiPh0M69mpw', 'yuvrajp.is18@sahyadri.edu.in', '7864446', 3, 2, '2000-12-12', 5),
(6, 'Ahmed', '4UU789', 'ahmed', '$pbkdf2-sha256$29000$YIyxVkpJae2d07o3Zuwd4w$NKvs4rAl9nm1C/7eJye9AeOZiG2xPNXpx6WFR8OcI40', 'ahmed@gmail.com', '84343132', 3, 3, '2002-05-01', 4),
(7, 'Elise', '4TT223', 'elise', '$pbkdf2-sha256$29000$cE7pPaf0Pmfs3ZuT0hqDcA$zTMi/g5SdTWfjr92uesdcJpA0tEClIZvkQZeswNtK58', 'elise@me.com', '8785435', 2, 2, '0000-00-00', 3),
(8, 'Suhas', '4UU457', 'suhas', '$pbkdf2-sha256$29000$xnhPiRFCCMHYO4dQas157w$s4d0iDSeizdg2mVrjQHJRaY/3F8C1cCqeRPiyXeeVhU', 'suhas@me.com', '782348', 2, 3, '2003-05-13', 5),
(9, 'Shibani', '4PP785', 'shibani', '$pbkdf2-sha256$29000$915Laa2VUirl3FuLsZYyxg$RQ03A9aUJmvP9Wj9rZTq1ae3jceltnikn4yWgRm6BSY', 'shibani@me.com', '78328648', 3, 7, '2000-06-12', 3),
(10, 'Ashwitha', '4OP755', 'ashwitha', '$pbkdf2-sha256$29000$QSilVMo5BwDAmNPau1fKWQ$66GfGMt962Pt3L58ObQ496.ApRZu0VgxPaJLAA/QOKc', 'ashwitha@me.com', '85565223', 3, 6, '2000-02-23', 3),
(11, 'Yashas', '4IP456', 'yashas', '$pbkdf2-sha256$29000$qlXKmXPO.T9HaO1da23tXQ$5PBLhwI3ANVhM.rhHrl6vNt7897kw69rZGCrBaEFqJw', 'yashas@me.com', '8386464', 3, 5, '2000-08-12', 1),
(12, 'Vishnu', '4IU555', 'vishnu', '$pbkdf2-sha256$29000$G.PcG.Oc03oPAcCYkzJGiA$QX9nKpRYQ4P17M8z/ChY/S5ZDumO3In7rAA7tLvZV8Q', 'vishnu@me.com', '7555222', 1, 7, '2000-01-01', 1),
(13, 'Mohan', '4WW125', 'mohan', '$pbkdf2-sha256$29000$CiHkvFeqlRJi7H1vba01Zg$xh/Yz7NN1OQfsS7dVhkJN/FnbWj4BN9Vh2RouqrFtKg', 'mohn@me.com', '8546435', 2, 5, '2000-10-02', 3),
(14, 'Rasheem', '4RT251', 'rasheem', '$pbkdf2-sha256$29000$G6NUqnUOYex9T4nx/h9jjA$za1yzVTGk9fSETL3Q4uLnabjbqhAPwVG9zILD1LMFYo', 'rasheem@me.com', '4387642', 3, 3, '2000-01-12', 4);

-- --------------------------------------------------------

--
-- Structure for view `age_calc`
--


--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `Admin`
  ADD PRIMARY KEY (`admin_id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `branch`
--
ALTER TABLE `Branch`
  ADD PRIMARY KEY (`branch_id`);

--
-- Indexes for table `course`
--
ALTER TABLE `Course`
  ADD PRIMARY KEY (`course_id`),
  ADD KEY `course_name` (`course_name`) USING BTREE,
  ADD KEY `category_id` (`category_id`);

--
-- Indexes for table `course_category`
--
ALTER TABLE `Course_Category`
  ADD PRIMARY KEY (`category_id`);

--
-- Indexes for table `department`
--
ALTER TABLE `Department`
  ADD PRIMARY KEY (`dept_id`);

--
-- Indexes for table `enrollment`
--
ALTER TABLE `Enrollment`
  ADD PRIMARY KEY (`student_id`,`course_id`),
  ADD KEY `course_id` (`course_id`);

--
-- Indexes for table `faculty`
--
ALTER TABLE `Faculty`
  ADD PRIMARY KEY (`faculty_id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD KEY `faculty_name` (`faculty_name`),
  ADD KEY `dept_id` (`dept_id`);

--
-- Indexes for table `student`
--
ALTER TABLE `Student`
  ADD PRIMARY KEY (`student_id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD KEY `username_2` (`username`),
  ADD KEY `branch_id` (`branch_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `Admin`
  MODIFY `admin_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `branch`
--
ALTER TABLE `Branch`
  MODIFY `branch_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `course`
--
ALTER TABLE `Course`
  MODIFY `course_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=39;

--
-- AUTO_INCREMENT for table `course_category`
--
ALTER TABLE `Course_Category`
  MODIFY `category_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `department`
--
ALTER TABLE `Department`
  MODIFY `dept_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `faculty`
--
ALTER TABLE `Faculty`
  MODIFY `faculty_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `student`
--
ALTER TABLE `Student`
  MODIFY `student_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `course`
--
ALTER TABLE `Course`
  ADD CONSTRAINT `course_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `Course_Category` (`category_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `enrollment`
--
ALTER TABLE `Enrollment`
  ADD CONSTRAINT `enrollment_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `Student` (`student_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `enrollment_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `Course` (`course_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `faculty`
--
ALTER TABLE `Faculty`
  ADD CONSTRAINT `faculty_ibfk_1` FOREIGN KEY (`dept_id`) REFERENCES `Department` (`dept_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `student`
--
ALTER TABLE `Student`
  ADD CONSTRAINT `student_ibfk_1` FOREIGN KEY (`branch_id`) REFERENCES `Branch` (`branch_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

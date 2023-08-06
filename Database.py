import sqlite3

class Course:
    def __init__(self, course_CRN, course_title, course_dept, course_startTime, course_endTime, course_days, course_semester, course_year, course_credits, course_instructor):
        self.course_CRN = course_CRN
        self.course_title = course_title
        self.course_dept = course_dept
        self.course_startTime = course_startTime
        self.course_endTime = course_endTime
        self.course_days = course_days
        self.course_semester = course_semester
        self.course_year = course_year
        self.course_credits = course_credits
        self.course_instructor = course_instructor

class Schedule:
    def __init__(self, db_connection):
        self.db_connection = db_connection


class User:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def authenticate(self, username, password):
        # This method is implemented by the subclasses
        raise NotImplementedError("Subclasses must implement the authenticate method.")


class Admin(User):
    def authenticate(self, username, password):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT ID, NAME, SURNAME FROM ADMIN WHERE USERNAME = ? AND PASSWORD = ?",
                       (username, password))
        admin_data = cursor.fetchone()
        if admin_data:
            admin_id = admin_data[0]
            admin_name = admin_data[1]
            self.user_type = "ADMIN"
            self.user_data = (admin_id, admin_name)
            return True
        return False

    def search_courses(self, params):
        cursor = self.db_connection.cursor()
        if(params == "ALL" or params == "all"):
            cursor.execute("SELECT CRN, TITLE, INSTRUCTOR FROM COURSES")
            results = cursor.fetchall()

        else:
            cursor.execute("SELECT CRN, TITLE, INSTRUCTOR "
                       "FROM COURSES "
                       "WHERE CRN LIKE ? OR TITLE LIKE ? OR DEPT LIKE ? " 
                       "OR STARTTIME = ? OR ENDTIME = ? OR DAYS LIKE ? "
                       "OR SEMESTER LIKE ? OR YEAR = ? OR CREDITS = ? "
                       "OR INSTRUCTOR LIKE ?",
                       (f"%{params}%", f"%{params}%", f"%{params}%", f"%{params}%", 
                        f"%{params}%", f"%{params}%", f"%{params}%", f"%{params}%",
                        f"%{params}%", f"%{params}%"))
            results = cursor.fetchall()
        return results
    
    def add_course(self, course):
        cursor = self.db_connection.cursor()
        cursor.execute("INSERT INTO COURSES (CRN, TITLE, DEPT, STARTTIME, ENDTIME, DAYS, SEMESTER, YEAR, CREDITS, INSTRUCTOR) "
                       "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (course.course_CRN, course.course_title, course.course_dept, course.course_startTime, course.course_endTime, course.course_days, course.course_semester, course.course_year, course.course_credits, course.course_instructor))
        self.db_connection.commit()
    
    def remove_course(self, course_CRN):
        cursor = self.db_connection.cursor()
        cursor.execute("DELETE FROM COURSES WHERE CRN = ?", (course_CRN,))
        self.db_connection.commit()

class Instructor(User):
    def authenticate(self, username, password):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT ID, NAME, SURNAME FROM INSTRUCTOR WHERE USERNAME = ? AND PASSWORD = ?",
                       (username, password))
        instructor_data = cursor.fetchone()
        if instructor_data:
            instructor_id = instructor_data[0]
            instructor_name = instructor_data[1]
            self.user_type = "INSTRUCTOR"
            self.user_data = (instructor_id, instructor_name)
            return True
        return False

    def search_courses(self, params):
        cursor = self.db_connection.cursor()
        if(params == "ALL" or params == "all"):
            cursor.execute("SELECT CRN, TITLE, INSTRUCTOR FROM COURSE_SCHEDULE")
            results = cursor.fetchall()

        else:
            cursor.execute("SELECT CRN, TITLE, INSTRUCTOR "
                       "FROM COURSE_SCHEDULE "
                       "WHERE CRN LIKE ? OR TITLE LIKE ? OR DEPT LIKE ? " 
                       "OR STARTTIME = ? OR ENDTIME = ? OR DAYS LIKE ? "
                       "OR SEMESTER LIKE ? OR YEAR = ? OR CREDITS = ? "
                       "OR INSTRUCTOR LIKE ?",
                       (f"%{params}%", f"%{params}%", f"%{params}%", f"%{params}%", 
                        f"%{params}%", f"%{params}%", f"%{params}%", f"%{params}%",
                        f"%{params}%", f"%{params}%"))
            results = cursor.fetchall()
        return results

    def print_roster(self, instructor_name):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT CRN, TITLE, INSTRUCTOR "
                       "FROM COURSE_SCHEDULE "
                       "WHERE INSTRUCTOR = ?",
                       (instructor_name,))
        roster = cursor.fetchall()
        for course in roster:
            print(f"Course CRN: {course[0]}")
            print(f"Course Title: {course[1]}")
            print(f"Instructor: {course[2]}")
            print()
        return course[0], course[1], course[2]

    def add_course(self, course):
        cursor = self.db_connection.cursor()
        cursor.execute("INSERT INTO COURSE_SCHEDULE (CRN, TITLE, DEPT, STARTTIME, ENDTIME, DAYS, SEMESTER, YEAR, CREDITS, INSTRUCTOR) "
                       "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (course.course_CRN, course.course_title, course.course_dept, course.course_startTime, course.course_endTime, course.course_days, course.course_semester, course.course_year, course.course_credits, course.course_instructor))
        self.db_connection.commit()
    
    def remove_course(self, course_CRN):
        cursor = self.db_connection.cursor()
        cursor.execute("DELETE FROM COURSE_SCHEDULE WHERE CRN = ?", (course_CRN,))
        self.db_connection.commit()

class Student(User):
    def authenticate(self, username, password):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT ID, NAME, SURNAME FROM STUDENT WHERE USERNAME = ? AND PASSWORD = ?",
                       (username, password))
        student_data = cursor.fetchone()
        if student_data:
            student_id = student_data[0]
            student_name = student_data[1]
            self.user_type = "STUDENT"
            self.user_data = (student_id, student_name)
            return True
        return False

    def search_courses(self, params):
        cursor = self.db_connection.cursor()
        if(params == "ALL" or params == "all"):
            cursor.execute("SELECT CRN, TITLE, INSTRUCTOR FROM STUDENT_SCHEDULE")
            results = cursor.fetchall()

        else:
            cursor.execute("SELECT CRN, TITLE, INSTRUCTOR "
                       "FROM STUDENT_SCHEDULE "
                       "WHERE CRN LIKE ? OR TITLE LIKE ? OR DEPT LIKE ? " 
                       "OR STARTTIME = ? OR ENDTIME = ? OR DAYS LIKE ? "
                       "OR SEMESTER LIKE ? OR YEAR = ? OR CREDITS = ? "
                       "OR INSTRUCTOR LIKE ?",
                       (f"%{params}%", f"%{params}%", f"%{params}%", f"%{params}%", 
                        f"%{params}%", f"%{params}%", f"%{params}%", f"%{params}%",
                        f"%{params}%", f"%{params}%"))
            results = cursor.fetchall()
        return results

    def add_course(self, course):
        cursor = self.db_connection.cursor()
        cursor.execute("INSERT INTO STUDENT_SCHEDULE (CRN, TITLE, DEPT, STARTTIME, ENDTIME, DAYS, SEMESTER, YEAR, CREDITS, INSTRUCTOR) "
                       "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (course.course_CRN, course.course_title, course.course_dept, course.course_startTime, course.course_endTime, course.course_days, course.course_semester, course.course_year, course.course_credits, course.course_instructor))
        self.db_connection.commit()
    
    def remove_course(self, course_CRN):
        cursor = self.db_connection.cursor()
        cursor.execute("DELETE FROM STUDENT_SCHEDULE WHERE CRN = ?", (course_CRN,))
        self.db_connection.commit()


class Database:
    def initDatabase():
        # Creating database and connecting to it
        db_connection = sqlite3.connect("LeopardWeb.db")

        # Creating tables
        cursor = db_connection.cursor()
        ##################################################################################
        ####################### Creating Tables ##########################################
        ##################################################################################

        # Creating Courses table
        cursor.execute("DROP TABLE IF EXISTS COURSES")
        cursor.execute("CREATE TABLE IF NOT EXISTS COURSES ("
                       "CRN INTEGER PRIMARY KEY NOT NULL,"
                       "TITLE TEXT NOT NULL,"
                       "DEPT TEXT NOT NULL,"
                       "STARTTIME INTEGER NOT NULL,"
                       "ENDTIME INTEGER NOT NULL,"
                       "DAYS TEXT NOT NULL,"
                       "SEMESTER TEXT NOT NULL,"
                       "YEAR INTEGER NOT NULL,"
                       "CREDITS INTEGER NOT NULL,"
                       "INSTRUCTOR TEXT)")

        cursor.execute("INSERT INTO COURSES VALUES(33946, 'ADVANCED DIGITAL CIRCUIT DESIGN', 'BSEE', 800, 930, 'WEDNESDAY', 'SUMMER', 2023, 4, '');")
        cursor.execute("INSERT INTO COURSES VALUES(33950, 'APPLIED PROGRAMMING CONCEPTS', 'BSCO', 800, 950, 'TUESDAY', 'SUMMER', 2023, 3, '');")
        cursor.execute("INSERT INTO COURSES VALUES(33817, 'ALGORITHMS', 'BSCS', 1100, 1220, 'MONDAY', 'SUMMER', 2023, 4, '');")
        cursor.execute("INSERT INTO COURSES VALUES(33955, 'COMPUTER NETWORKS', 'BSCO', 1230, 1320, 'WEDNESDAY', 'SUMMER', 2023, 4, '');")
        cursor.execute("INSERT INTO COURSES VALUES(33959, 'SIGNALS AND SYSTEMS', 'BSEE', 1300, 1450, 'THURSDAY', 'SUMMER', 2023, 4, '');")

        cursor.execute("INSERT INTO COURSES VALUES(22275, 'DIGITAL LOGIC', 'BSEE', 900, 1050, 'FRIDAY', 'FALL', 2023, 4, '');")
        cursor.execute("INSERT INTO COURSES VALUES(83557, 'DIFFERENTIAL EQUATIONS', 'BSMA', 1350, 1530, 'TUESDAY', 'FALL', 2023, 3, '');")
        cursor.execute("INSERT INTO COURSES VALUES(23478, 'MICROCONTROLLERS USING C PROG', 'BSCO', 1100, 1220, 'FRIDAY', 'FALL', 2023, 4, '');")
        cursor.execute("INSERT INTO COURSES VALUES(94532, 'MULTIVARIABLE CALCULUS', 'BSMA', 1250, 1350, 'WEDNESDAY', 'FALL', 2023, 4, '');")
        cursor.execute("INSERT INTO COURSES VALUES(68533, 'NETWORK THEORY I', 'BSEE', 1340, 1530, 'THURSDAY', 'FALL', 2023, 4, '');")

        cursor.execute("INSERT INTO COURSES VALUES(34585, 'DESCRETE MATH', 'BSMA', 800, 930, 'FRIDAY', 'SPRING', 2023, 4, '');")
        cursor.execute("INSERT INTO COURSES VALUES(23457, 'ANALOG CIRCUIT DESIGN', 'BSEE', 830, 1200, 'TUESDAY', 'SPRING', 2023, 4, '');")
        cursor.execute("INSERT INTO COURSES VALUES(76453, 'COMPUTER ARCHITECTURE', 'BSCO', 1120, 1250, 'MONDAY', 'SPRING', 2023, 4, '');")
        cursor.execute("INSERT INTO COURSES VALUES(23453, 'DATA STRUCTURES', 'BSCS', 1030, 1220, 'WEDNESDAY', 'SPRING', 2023, 4, '');")
        cursor.execute("INSERT INTO COURSES VALUES(33922, 'LINEAR ALGEBRA AND MATRIX THEORY', 'BSMA', 1320, 1430, 'THURSDAY', 'SPRING', 2023, 4, '');")


        # Creating Course_Schedule table --> will grab rows from Courses table
        cursor.execute("DROP TABLE IF EXISTS COURSE_SCHEDULE")
        cursor.execute("CREATE TABLE IF NOT EXISTS COURSE_SCHEDULE ("
                       "CRN INTEGER PRIMARY KEY NOT NULL,"
                       "TITLE TEXT NOT NULL,"
                       "DEPT TEXT NOT NULL,"
                       "STARTTIME INTEGER NOT NULL,"
                       "ENDTIME INTEGER NOT NULL,"
                       "DAYS TEXT NOT NULL,"
                       "SEMESTER TEXT NOT NULL,"
                       "YEAR INTEGER NOT NULL,"
                       "CREDITS INTEGER NOT NULL,"
                       "INSTRUCTOR TEXT)")

        # Creating Student_Schedule table --> will grab rows from Course_schedule table
        cursor.execute("DROP TABLE IF EXISTS STUDENT_SCHEDULE")
        cursor.execute("CREATE TABLE IF NOT EXISTS STUDENT_SCHEDULE ("
                       "CRN INTEGER PRIMARY KEY NOT NULL,"
                       "TITLE TEXT NOT NULL,"
                       "DEPT TEXT NOT NULL,"
                       "STARTTIME INTEGER NOT NULL,"
                       "ENDTIME INTEGER NOT NULL,"
                       "DAYS TEXT NOT NULL,"
                       "SEMESTER TEXT NOT NULL,"
                       "YEAR INTEGER NOT NULL,"
                       "CREDITS INTEGER NOT NULL,"
                       "INSTRUCTOR TEXT)")

        # Creating Admin table
        cursor.execute("DROP TABLE IF EXISTS ADMIN")
        cursor.execute("CREATE TABLE IF NOT EXISTS ADMIN ("
                       "ID INTEGER PRIMARY KEY NOT NULL,"
                       "NAME TEXT NOT NULL,"
                       "SURNAME TEXT NOT NULL,"
                       "TITLE TEXT NOT NULL,"
                       "OFFICE TEXT NOT NULL,"
                       "EMAIL TEXT NOT NULL,"
                       "USERNAME TEXT NOT NULL UNIQUE,"
                       "PASSWORD TEXT NOT NULL UNIQUE)")

        # Inserting into Admin
        cursor.execute("INSERT INTO ADMIN VALUES(1, 'Jenn', 'Kosses', 'President', 'Dobbs 210', 'jkosses12', 'kossesjenn', 'jk135235')")

        # Creating Instructor table
        cursor.execute("DROP TABLE IF EXISTS INSTRUCTOR")
        cursor.execute("CREATE TABLE IF NOT EXISTS INSTRUCTOR ("
                       "ID INTEGER PRIMARY KEY NOT NULL,"
                       "NAME TEXT NOT NULL,"
                       "SURNAME TEXT NOT NULL,"
                       "TITLE TEXT NOT NULL,"
                       "HIREYEAR TEXT NOT NULL,"
                       "DEPT TEXT NOT NULL,"
                       "EMAIL TEXT NOT NULL,"
                       "USERNAME TEXT NOT NULL UNIQUE,"
                       "PASSWORD TEXT NOT NULL UNIQUE)")
        
        # Inserting into instructor
        
        cursor.execute("INSERT INTO INSTRUCTOR VALUES(1, 'Marisha', 'Rawlins', 'Professor', '2012', 'BSCO', 'marisha.rawlins@example.com', 'mrawlins12', 'mr1245')")
        cursor.execute("INSERT INTO INSTRUCTOR VALUES(2, 'John', 'Smith', 'Associate Professor', '2008', 'BSCS', 'john.smith@example.com', 'johnsmith08', 'js12345')")
        cursor.execute("INSERT INTO INSTRUCTOR VALUES(3, 'Emily', 'Johnson', 'Assistant Professor', '2015', 'BSEE', 'emily.johnson@example.com', 'emilyjohnson15', 'ej22345')")
        cursor.execute("INSERT INTO INSTRUCTOR VALUES(4, 'Michael', 'Williams', 'Instructor', '2019', 'BSCO', 'michael.williams@example.com', 'michaelwilliams19', 'mw32345')")
        cursor.execute("INSERT INTO INSTRUCTOR VALUES(5, 'Sarah', 'Brown', 'Professor', '2006', 'BSMA', 'sarah.brown@example.com', 'sarahbrown06', 'pw42345')")
        cursor.execute("INSERT INTO INSTRUCTOR VALUES(6, 'David', 'Lee', 'Associate Professor', '2011', 'BSCO', 'david.lee@example.com', 'davidlee11', 'pw52345')")
        cursor.execute("INSERT INTO INSTRUCTOR VALUES(7, 'Jessica', 'Miller', 'Assistant Professor', '2018', 'BSEE', 'jessica.miller@example.com', 'jessicamiller18', 'pw62345')")
        cursor.execute("INSERT INTO INSTRUCTOR VALUES(8, 'Christopher', 'Davis', 'Instructor', '2016', 'BSMA', 'christopher.davis@example.com', 'christopherdavis16', 'pw72345')")
        cursor.execute("INSERT INTO INSTRUCTOR VALUES(9, 'Samantha', 'Wilson', 'Professor', '2010', 'BSEE', 'samantha.wilson@example.com', 'samanthawilson10', 'pw82345')")
        cursor.execute("INSERT INTO INSTRUCTOR VALUES(10, 'Matthew', 'Martinez', 'Associate Professor', '2017', 'BSCO', 'matthew.martinez@example.com', 'matthewmartinez17', 'pw92345')")
        cursor.execute("INSERT INTO INSTRUCTOR VALUES(11, 'Ashley', 'Anderson', 'Assistant Professor', '2014', 'BSEE', 'ashley.anderson@example.com', 'ashleyanderson14', 'pw102345')")
        cursor.execute("INSERT INTO INSTRUCTOR VALUES(12, 'James', 'Thomas', 'Instructor', '2020', 'BSCO', 'james.thomas@example.com', 'jamesthomas20', 'pw112345')")
        cursor.execute("INSERT INTO INSTRUCTOR VALUES(13, 'Lauren', 'Taylor', 'Professor', '2005', 'BSCS', 'lauren.taylor@example.com', 'laurentaylor05', 'pw122345')")
        cursor.execute("INSERT INTO INSTRUCTOR VALUES(14, 'Daniel', 'Hernandez', 'Associate Professor', '2013', 'BSMA',  'daniel.hernandez@example.com','danielhernandez13', 'pw132345')")
        cursor.execute("INSERT INTO INSTRUCTOR VALUES(15, 'Elizabeth', 'King', 'Assistant Professor', '2019', 'BSCS', 'elizabeth.king@example.com', 'elizabethking19', 'pw142345')")


        # Creating Student table
        cursor.execute("DROP TABLE IF EXISTS STUDENT")
        cursor.execute("CREATE TABLE IF NOT EXISTS STUDENT ("
                       "ID INTEGER PRIMARY KEY NOT NULL,"
                       "NAME TEXT NOT NULL,"
                       "SURNAME TEXT NOT NULL,"
                       "GRADYEAR TEXT NOT NULL,"
                       "MAJOR TEXT NOT NULL,"
                       "EMAIL TEXT NOT NULL,"
                       "USERNAME TEXT NOT NULL UNIQUE,"
                       "PASSWORD TEXT NOT NULL UNIQUE)")

        # Inserting into Student
        cursor.execute("INSERT INTO STUDENT VALUES(1, 'Niamh', 'Conway', '2022', 'BSCE', 'nconway12', 'niamhc', 'nc1235')")
        cursor.execute("INSERT INTO STUDENT VALUES(2, 'Darcy', 'Wright', '2023', 'BSCS', 'dwright12', 'darcyw', 'dw14123')")
        cursor.execute("INSERT INTO STUDENT VALUES(3, 'Gavin', 'Dennis', '2022', 'BSCE', 'tstudent12', 'gavind', 'gd12633')")
        cursor.execute("INSERT INTO STUDENT VALUES(4, 'Ria', 'Hudson', '2022', 'BSCS', 'tstudent12', 'riah', 'rh12363')")
        cursor.execute("INSERT INTO STUDENT VALUES(5, 'Keith', 'Rice', '2021', 'BSEE', 'tstudent12', 'keithr', 'kr123453')")
        cursor.execute("INSERT INTO STUDENT VALUES(6, 'Findlay', 'Key', '2020', 'BSCE', 'tstudent12', 'findlayk', 'fk12213')")
        cursor.execute("INSERT INTO STUDENT VALUES(7, 'Marwa', 'Kerr', '2022', 'BSCS', 'tstudent12', 'marwak', 'mk12533')")
        cursor.execute("INSERT INTO STUDENT VALUES(8, 'Betsy', 'Parks', '2024', 'BSCE', 'tstudent12', 'betsyp', 'bp12623')")
        cursor.execute("INSERT INTO STUDENT VALUES(9, 'Damon', 'Lin', '2023', 'BSCE', 'tstudent12', 'damonl', 'dl12543')")
        cursor.execute("INSERT INTO STUDENT VALUES(10, 'Zaynab', 'Slater', '2023', 'BSCE', 'tstudent12', 'zaynabs', 'zs1283')")
        cursor.execute("INSERT INTO STUDENT VALUES(11, 'Caleb', 'Riley', '2021', 'BSCS', 'tstudent12', 'calebr', 'cr122633')")
        cursor.execute("INSERT INTO STUDENT VALUES(12, 'Ian', 'Ponce', '2019', 'BSCE', 'tstudent12', 'ianp', 'ip12523')")
        cursor.execute("INSERT INTO STUDENT VALUES(13, 'Alissa', 'Acosta', '2024', 'BSCE', 'tstudent12', 'alissaa', 'aa1213')")
        cursor.execute("INSERT INTO STUDENT VALUES(14, 'Nathanael', 'Robinson', '2024', 'BSCE', 'tstudent12', 'nathanaelr', 'nr18523')")
        cursor.execute("INSERT INTO STUDENT VALUES(15, 'Emily', 'Daugherty', '2025', 'BSCS', 'tstudent12', 'emilyd', 'ed19523')")
        cursor.execute("INSERT INTO STUDENT VALUES(16, 'Miriam', 'Knight', '2025', 'BSEE', 'tstudent12', 'miramk', 'mk151223')")
        cursor.execute("INSERT INTO STUDENT VALUES(17, 'Darius', 'Newman', '2024', 'BSCE', 'tstudent12', 'dariusn', 'dn12723')")
        cursor.execute("INSERT INTO STUDENT VALUES(18, 'Dan', 'Dawson', '2023', 'BSEE', 'tstudent12', 'dand', 'dd12983')")
        cursor.execute("INSERT INTO STUDENT VALUES(19, 'Jenny', 'Barber', '2022', 'BSCE', 'tstudent12', 'jennyb', 'jb1233')")
        cursor.execute("INSERT INTO STUDENT VALUES(20, 'Ivy', 'Wagner', '2022', 'BSEE', 'tstudent12', 'ivyw', 'iw12623')")

        # Committing the changes
        db_connection.commit()
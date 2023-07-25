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

    def search_courses(self, params):
        cursor = self.db_connection.cursor()
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


class Database:
    def initDatabase():
        # Creating database and connecting to it
        db_connection = sqlite3.connect("assignment5.db")

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

        cursor.execute("INSERT INTO COURSES VALUES(33946, 'ADVANCED DIGITAL CIRCUIT DESIGN', 'BSEE', 800, 930, 'WEDNESDAY, FRIDAY', 'SUMMER', 2023, 4, '');")
        cursor.execute("INSERT INTO COURSES VALUES(33950, 'APPLIED PROGRAMMING CONCEPTS', 'BSCO', 800, 950, 'TUESDAY, THURSDAY', 'SUMMER', 2023, 3, '');")
        cursor.execute("INSERT INTO COURSES VALUES(33817, 'ALGORITHMS', 'BSCS', 1100, 1220, 'MONDAY, WEDNESDAY', 'SUMMER', 2023, 4, '');")
        cursor.execute("INSERT INTO COURSES VALUES(33955, 'COMPUTER NETWORKS', 'BSCO', 1230, 1320, 'MONDAY, WEDNESDAY', 'SUMMER', 2023, 4, '');")
        cursor.execute("INSERT INTO COURSES VALUES(33959, 'SIGNALS AND SYSTEMS', 'BSEE', 1300, 1450, 'TUESDAY, THURSDAY', 'SUMMER', 2023, 4, '');")


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
                       "USERNAME TEXT NOT NULL,"
                       "PASSWORD TEXT NOT NULL)")

        # Inserting into Admin
        cursor.execute("INSERT INTO ADMIN VALUES(1, 'Test', 'Admin', 'President', 'Dobbs 210', 'tadmin12', 'testadmin', 'test123')")

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
                       "USERNAME TEXT NOT NULL,"
                       "PASSWORD TEXT NOT NULL)")
        
        # Inserting into instructor
        cursor.execute("INSERT INTO INSTRUCTOR VALUES(1, 'Test', 'Instructor', 'Professor', '2012', 'BCSE', 'tinstruct12', 'testinstructor', 'test123')")

        # Creating Student table
        cursor.execute("DROP TABLE IF EXISTS STUDENT")
        cursor.execute("CREATE TABLE IF NOT EXISTS STUDENT ("
                       "ID INTEGER PRIMARY KEY NOT NULL,"
                       "NAME TEXT NOT NULL,"
                       "SURNAME TEXT NOT NULL,"
                       "GRADYEAR TEXT NOT NULL,"
                       "MAJOR TEXT NOT NULL,"
                       "EMAIL TEXT NOT NULL,"
                       "USERNAME TEXT NOT NULL,"
                       "PASSWORD TEXT NOT NULL)")

        # Inserting into Student
        cursor.execute("INSERT INTO STUDENT VALUES(1, 'Test', 'Student', '2022', 'BCSE', 'tstudent12', 'teststudent', 'test123')")

        # Committing the changes
        db_connection.commit()
import sqlite3
from GUI import GUI
from Database import *

#GUI.testGUI()
#GUI.testGUI2()
Database.initDatabase()

GUI.login()


##################################################################################
####################### Main Menu Loop ###########################################
##################################################################################
while True:
    GUI.display_menu(user.user_type)

    choice = input("Enter your choice: ")

    # Add/remove course from semester schedule
    if choice == "1":
        ar = input("Select (1) if you want to ADD a course or (2) if you want to REMOVE a course: ")
        if ar == "1":
            course_CRN = input("Enter the CRN of the course you want to add to the semesester schedule: ")
            cursor.execute("INSERT INTO COURSE_SCHEDULE SELECT * FROM COURSES WHERE COURSES.CRN = ?",
                            (course_CRN,))
            db_connection.commit()
            print("Course successfully added")
        elif ar == "2":
            course_CRN = input("Enter the CRN of the course you want to remove from the semesester schedule: ")
            cursor.execute("DELETE FROM COURSE_SCHEDULE WHERE CRN = ?",
                            (course_CRN,))
            db_connection.commit()
            print("Course successfully removed")
        else:
            print("Invalid choice")

    # Search for courses
    elif choice == "2":
        search_query = input("Enter a field to search courses by (Any parameter): ")
        print(user.search_courses(search_query))

    # Add/remove instructor
    elif choice == "3" and user.user_type == "ADMIN":
        instructor_id = input("Enter the instructor ID: ")
        instructor_name = input("Enter the instructor name: ")
        username = input("Enter the instructor username: ")
        password = input("Enter the instructor password: ")
        cursor.execute("INSERT INTO Instructor (instructor_id, instructor_name, username, password) "
                       "VALUES (?, ?, ?, ?)",
                       (instructor_id, instructor_name, username, password))
        db_connection.commit()
        print("Instructor added to the system.")

    # Add/remove student
    elif choice == "4" and user.user_type == "ADMIN":
        print("add/remove student")

    # Add/remove course
    elif choice == "5" and user.user_type == "ADMIN":
        ar = input("Select (1) if you want to ADD a course or (2) if you want to REMOVE a course: ")
        if ar == '1':
            course_CRN = input("Input the course CRN: ")
            course_title = input("Input course name: ")
            course_dept = input("Enter the department abbreviation the course belongs to: ")
            course_startTime = input("Enter the start time of the course in military time, represented as an integer: ")
            course_endTime = input("Enter the end time of the course in military time, represented as an integer: ")
            course_days = input("Enter the days this course is taught on separated by commas: ")
            course_semester = input("Enter the semester this course is taught in: ")
            course_year = input("Enter the year that this semester is taught: ")
            course_credits = input("Enter the number of credits this course is worth: ")
            course_instructor = input("Enter the ID or Name of the instructor who teaches this course: ")

            cursor.execute("INSERT INTO COURSES (CRN, TITLE, DEPT, STARTTIME, ENDTIME, DAYS, SEMESTER, YEAR, CREDITS, INSTRUCTOR) " 
                           "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           (course_CRN, course_title, course_dept, course_startTime, 
                            course_endTime, course_days, course_semester, course_year, course_credits, course_instructor))
            db_connection.commit()
        elif ar == '2':
            course_CRN = input("Enter the CRN of the course you would like to remove from the system: ")
            cursor.execute("DELETE FROM COURSES WHERE CRN = ?", (course_CRN,))
            db_connection.commit()
        else:
            print("Invalid choice")
        
    elif choice == "4" and user.user_type == "INSTRUCTOR":
        instructor_name = input("Enter the instructor name to print the roster: ")
        instructor.print_roster(instructor_name)

    elif choice == "5" and user.user_type == "STUDENT":
        params = input("Enter the search parameters: ")
        results = student.search_courses(params)
        for course in results:
            print(f"Course CRN: {course[0]}")
            print(f"Course Name: {course[1]}")
            print(f"Instructor: {course[2]}")
            print()

    elif choice == "6":
        break

    else:
        print("Invalid choice. Please try again.")

# Closing the database connection
db_connection.close()

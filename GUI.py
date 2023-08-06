from encodings import search_function
from tkinter import *
import tkinter as tk
import sqlite3
from Database import *

# Connect to the database
db_connection = sqlite3.connect("LeopardWeb.db")
cursor = db_connection.cursor()
Database.initDatabase()

# Creating instances of Admin, Instructor, and Student
admin = Admin(db_connection)
instructor = Instructor(db_connection)
student = Student(db_connection)
user = None

class GUI:
    # The login function for user authentication
    def login():
        # Create the login window
        login = Tk()
        login.title("Login")

        # Labels and Entry widgets for username and password
        query = tk.Label(
            text="Please enter your username and password",
            width=50,
            height=10
            )

        # Adjust size
        login.geometry("1000x600")
        bg = PhotoImage(file = "wentworth-logo-1-2.png")

        # Create Canvas
        canvas1 = Canvas(login, width = 500, height = 200)
  
        # Display image
        canvas1.create_image( 0, 0, image = bg, anchor = "nw")

        #Calculating the center coordinates of the window
        center_x = login.winfo_screenwidth() // 2
        center_y = login.winfo_screenwidth() // 2

        #displaying image centered to the window
        canvas1.create_image(center_x, center_y, image = bg)

        usern = tk.Label(
            text="Username: ",
            width=10,
            height=1
        )

        passw = tk.Label(
            text="Password: ",
            width=10,
            height=1
        )

        username = tk.Entry()
        password = tk.Entry(show="*")

        query.pack()
        usern.pack()
        username.pack()
        passw.pack()
        password.pack()

        # Confirm button for authentication
        confirm = tk.Button(login, text='Confirm', width=15, command=lambda: GUI.auth(username.get(), password.get(), login))
        # Exit button
        exit_b = tk.Button(login, text='Exit', width=15, command=login.destroy)

        confirm.pack()
        exit_b.pack()

        login.bind('<Return>', lambda event : confirm.invoke())
        canvas1.place(relx=0.5, rely=0.5, anchor="center")
        login.mainloop()

    def logout(current_window):
        current_window.destroy()
        GUI.login()

    # Helper function to get the Entry widget value
    def checkEntry(entry):
        entry.get()

    # Function for user authentication
    def auth(username, password, login_window):
        # Authenticating the user
        global user
       
        while True:

            # Check in the Admin table
            if admin.authenticate(username, password):
                user = admin

            # Check in the Instructor table
            elif instructor.authenticate(username, password):
                user = instructor

            # Check in the Student table
            elif student.authenticate(username, password):
                user = student

            if user:
                break
            else:
                print("Authentication failed. Please try again.")
                return

        print("Authentication successful!")
        print(f"Welcome, {user.user_type} {user.user_data[1]}!")

        # Close the login window after successful login
        login_window.destroy()

        # Display the menu based on the user type in the new main application window
        GUI.display_menu(user.user_type)

    # Function to display the main application menu
    def display_menu(user_type):
        main_app = Tk()
        main_app.title(f"{user_type} Main Application")

        menu_label = tk.Label(
            text=f"{user_type} MENU:",
            width=50,
            height=10
        )
        menu_label.pack()

        if user_type == "ADMIN":
            main_app['background'] = '#FF8880'
            menu_label['background'] = '#FF8880'
            # Add buttons for admin actions
            button1 = tk.Button(main_app, text="Add course to course database", bg='red', command=lambda: GUI.addCourse(user_type, main_app))
            button2 = tk.Button(main_app, text="Remove course from course database", bg='red', command=lambda: GUI.removeCourse(user_type, main_app))
            button3 = tk.Button(main_app, text="Search for course(s)", bg='red', command=lambda: GUI.searchCourses(user_type, main_app))
            button4 = tk.Button(main_app, text="Add Instructor to the system", bg='red', command=lambda: GUI.addInstructor(user_type, main_app))
            button5 = tk.Button(main_app, text="Remove Instructor from the system", bg='red', command=lambda: GUI.removeInstructor(user_type, main_app))
            button6 = tk.Button(main_app, text="Add Student to the system", bg='red', command=lambda: GUI.addStudent(user_type, main_app))
            button7 = tk.Button(main_app, text="Remove Student from the system", bg='red', command=lambda: GUI.removeStudent(user_type, main_app))
            button8 = tk.Button(main_app, text="Logout", bg='red', command=lambda: GUI.logout(main_app))

            # Pack buttons
            button1.pack()
            button2.pack()
            button3.pack()
            button4.pack()
            button5.pack()
            button6.pack()
            button7.pack()
            button8.pack()

        elif user_type == "INSTRUCTOR":
            main_app['background'] = '#FFF98A'
            menu_label['background'] = '#FFF98A'
            # Add buttons for instructor actions
            button1 = tk.Button(main_app, text="Add course to semester schedule", bg='yellow', command=lambda: GUI.addCourse(user_type, main_app))
            button2 = tk.Button(main_app, text="Remove course from semester schedule", bg='yellow', command=lambda: GUI.removeCourse(user_type, main_app))
            button3 = tk.Button(main_app, text="Search for course(s)", bg='yellow', command=lambda: GUI.searchCourses(user_type, main_app))
            button4 = tk.Button(main_app, text="Logout", bg='yellow', command=lambda: GUI.logout(main_app))

            # Pack buttons
            button1.pack()
            button2.pack()
            button3.pack()
            button4.pack()

        elif user_type == "STUDENT":
            main_app['background'] = '#AFFC9A'
            menu_label['background'] = '#AFFC9A'
            # Add buttons for student actions
            button1 = tk.Button(main_app, text="Add course to student schedule", bg='#30D402', command=lambda: GUI.addCourse(user_type, main_app))
            button2 = tk.Button(main_app, text="Remove course from student schedule", bg='#30D402', command=lambda: GUI.removeCourse(user_type, main_app))
            button3 = tk.Button(main_app, text="Search for course(s)", bg='#30D402', command=lambda:GUI.searchCourses(user_type, main_app))
            button4 = tk.Button(main_app, text="Logout", bg='#30D402', command=lambda: GUI.logout(main_app))

            # Pack buttons
            button1.pack()
            button2.pack()
            button3.pack()
            button4.pack()

        main_app.mainloop()

    def backToMenu(x):
        x.destroy()
        GUI.display_menu(user.user_type)

    # Search for courses
    def searchCourses(user_type, main_app):
        main_app.destroy()
        search_menu = Tk()
        search_menu.title(f"{user_type} Search application")

        # Label for course list
        search_label = Label(search_menu, width=55, height=5, text = "SEARCH COURSES")
        search_label2 = Label(search_menu, width=55, height=5, text = "To print all courses, type 'all' into search bar")
        search_label.pack()
        search_label2.pack(side=BOTTOM)

        # Pulls courses from the database and adds them to listbox (should pull from different database depending on user)
        search_list = Listbox(search_menu, bg='white', height=10, width=50, font='Arial')
        GUI.printCourses(user_type, search_list, "ALL")
        search_list.pack()

        # Search box
        sb_frame = Frame(search_menu)
        search_box = Label(sb_frame, text = "Search for course: ")
        search_box.pack()

        modify = Entry(sb_frame)
        modify.pack(side=LEFT, fill=BOTH, expand=1)
        modify.focus_set()

        search_button = Button(sb_frame, text="Search", command=lambda: GUI.printCourses(user_type, search_list, modify.get()))
        search_button.pack(side=RIGHT)
        sb_frame.pack(side=TOP)

        #Back Button to get back to the main menu
        button1 = tk.Button(search_menu, text="Back to Menu", bg='red', command=lambda: GUI.backToMenu(search_menu))
        button1.pack()
        
        search_menu.bind('<Return>', lambda event : search_button.invoke())
        search_menu.mainloop()

    def printCourses(user_type, search_list, search_term):
        if user_type == 'ADMIN':
            courses = admin.search_courses(search_term)
            search_list.delete(0, END)
            for x in courses:
                search_list.insert(END, f"{x}")
        elif user_type == 'INSTRUCTOR':
            courses = instructor.search_courses(search_term)
            search_list.delete(0, END)
            for x in courses:
                search_list.insert(END, f"{x}")
        elif user_type == 'STUDENT':
            courses = student.search_courses(search_term)
            search_list.delete(0, END)
            for x in courses:
                search_list.insert(END, f"{x}")

    def addCourse(user_type, main_app):
        main_app.destroy()
        # ar stands for add/remove
        ar_menu = Tk()
        ar_menu.title(f"{user_type} Add courses")

        # Label for course list
        ar_label = Label(ar_menu, width=150, height=10, text = "ADD COURSES")
        ar_label.pack()

        # Pulls courses from the database and adds them to listbox (should pull from different database depending on user)
        ar_list = Listbox(ar_menu, bg='white', height=10, width=100, font='Arial')
        GUI.printCourses(user_type, ar_list, "ALL")
        ar_list.pack()
        #printCourses(user_type, ar_list)

        # Search box
        ar_frame1 = Frame(ar_menu)
        ar_frame2 = Frame(ar_menu)
        ar_frame3 = Frame(ar_menu)
        ar_frame4 = Frame(ar_menu)
        ar_frame5 = Frame(ar_menu)
        ar_frame6 = Frame(ar_menu)
        ar_frame7 = Frame(ar_menu)
        ar_frame8 = Frame(ar_menu)
        ar_frame9 = Frame(ar_menu)
        ar_frame10 = Frame(ar_menu)

        # CRN
        ar_box = Label(ar_frame1, text = "CRN: ")
        ar_box.pack(side=TOP)
        modify_CRN = Entry(ar_frame1)
        modify_CRN.pack(side=LEFT)
        modify_CRN.focus_set()
        # Title
        ar_box2 = Label(ar_frame2, text = "Title: ")
        ar_box2.pack(side=TOP)
        modify_Title = Entry(ar_frame2)
        modify_Title.pack(side=LEFT)
        modify_Title.focus_set()
        # Department
        ar_box3 = Label(ar_frame3, text = "Department: ")
        ar_box3.pack(side=TOP)
        modify_Dept = Entry(ar_frame3)
        modify_Dept.pack(side=LEFT)
        modify_Dept.focus_set()
        # Start time
        ar_box4 = Label(ar_frame4, text = "Start time (military): ")
        ar_box4.pack(side=TOP)
        modify_sTime = Entry(ar_frame4)
        modify_sTime.pack(side=LEFT)
        modify_sTime.focus_set()
        # End time
        ar_box5 = Label(ar_frame5, text = "End time (military): ")
        ar_box5.pack(side=TOP)
        modify_eTime = Entry(ar_frame5)
        modify_eTime.pack(side=LEFT)
        modify_eTime.focus_set()
        # Days
        ar_box6 = Label(ar_frame6, text = "Days: ")
        ar_box6.pack(side=TOP)
        modify_Days = Entry(ar_frame6)
        modify_Days.pack(side=LEFT)
        modify_Days.focus_set()
        # Semester
        ar_box7 = Label(ar_frame7, text = "Semester: ")
        ar_box7.pack(side=TOP)
        modify_Semester = Entry(ar_frame7)
        modify_Semester.pack(side=LEFT)
        modify_Semester.focus_set()
        # Year
        ar_box8 = Label(ar_frame8, text = "Year: ")
        ar_box8.pack(side=TOP)
        modify_Year = Entry(ar_frame8)
        modify_Year.pack(side=LEFT)
        modify_Year.focus_set()
        # Credits
        ar_box9 = Label(ar_frame9, text = "Credits: ")
        ar_box9.pack(side=TOP)
        modify_Credits = Entry(ar_frame9)
        modify_Credits.pack(side=LEFT)
        modify_Credits.focus_set()
        # Instructor
        ar_box10 = Label(ar_frame10, text = "Instructor: ")
        ar_box10.pack(side=TOP)
        modify_Instructor = Entry(ar_frame10)
        modify_Instructor.pack(side=LEFT)
        modify_Instructor.focus_set()
        

        #ar_button = Button(ar_frame1, text="Add", command=lambda: user.add_course(modify_CRN.get()))
        #ar_button.pack(side=LEFT)
        ar_frame1.pack(side=LEFT)
        ar_frame2.pack(side=LEFT)
        ar_frame3.pack(side=LEFT)
        ar_frame4.pack(side=LEFT)
        ar_frame5.pack(side=LEFT)
        ar_frame6.pack(side=LEFT)
        ar_frame7.pack(side=LEFT)
        ar_frame8.pack(side=LEFT)
        ar_frame9.pack(side=LEFT)
        ar_frame10.pack(side=LEFT)

        ar_button = Button(ar_frame10, text="Add", command=lambda: GUI.addHelper(user_type, ar_list, modify_CRN.get(), modify_Title.get(), modify_Dept.get(), modify_sTime.get(), modify_eTime.get(), modify_Days.get(), modify_Semester.get(), modify_Year.get(), modify_Credits.get(), modify_Instructor.get()))
        ar_button.pack(side=LEFT)


        # Add the "Back to Menu" button
        back_frame = Frame(ar_menu)
        back_button = Button(back_frame, text="Back to Menu", command=lambda: GUI.backToMenu(ar_menu))
        back_button.pack(side=BOTTOM)
        back_frame.pack(side=BOTTOM)  # Pack this frame at the bottom of ar_menu

        ar_menu.bind('<Return>', lambda event : ar_button.invoke())
        ar_menu.mainloop()

    def addHelper(user_type, ar_list, CRN, title, dept, startTime, endTime, days, semester, year, credits, instructor):
        if user_type == "ADMIN":
            cursor.execute("INSERT INTO COURSES (CRN, TITLE, DEPT, STARTTIME, ENDTIME, DAYS, SEMESTER, YEAR, CREDITS, INSTRUCTOR) "
                       "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (CRN, title, dept, startTime, endTime, days, semester, year, credits, instructor))
            db_connection.commit()
            GUI.printCourses(user_type, ar_list, "ALL")
        if user_type == "INSTRUCTOR":
            cursor.execute("INSERT INTO COURSE_SCHEDULE (CRN, TITLE, DEPT, STARTTIME, ENDTIME, DAYS, SEMESTER, YEAR, CREDITS, INSTRUCTOR) "
                       "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (CRN, title, dept, startTime, endTime, days, semester, year, credits, instructor))
            db_connection.commit()
            GUI.printCourses(user_type, ar_list, "ALL")
        if user_type == "STUDENT":
            cursor.execute("INSERT INTO STUDENT_SCHEDULE (CRN, TITLE, DEPT, STARTTIME, ENDTIME, DAYS, SEMESTER, YEAR, CREDITS, INSTRUCTOR) "
                       "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (CRN, title, dept, startTime, endTime, days, semester, year, credits, instructor))
            db_connection.commit()
            GUI.printCourses(user_type, ar_list, "ALL")

    def removeCourse(user_type, main_app):
        main_app.destroy()
        # ar stands for add/remove
        ar_menu = Tk()
        ar_menu.title(f"{user_type} Remove courses")

        # Label for course list
        ar_label = Label(ar_menu, width=55, height=5, text = "REMOVE COURSES")
        ar_label.pack()

        # Pulls courses from the database and adds them to listbox (should pull from different database depending on user)
        ar_list = Listbox(ar_menu, bg='white', height=10, width=50, font='Arial')
        GUI.printCourses(user_type, ar_list, "ALL")
        ar_list.pack()

        # Search box
        ar_frame = Frame(ar_menu)
        ar_box = Label(ar_frame, text = "Enter course to remove: ")
        ar_box.pack()

        modify = Entry(ar_frame)
        modify.pack(side=LEFT, fill=BOTH, expand=1)
        modify.focus_set()
        
        ar_button = Button(ar_frame, text="Remove", command=lambda: GUI.removeHelper(user_type, modify.get(), ar_list))
        ar_button.pack(side=LEFT)
        ar_button.pack(side=RIGHT)

        # Create a frame for the "Back to Menu" button at the bottom
        back_frame = Frame(ar_menu)
        back_button = Button(back_frame, text="Back to Menu", command=lambda: GUI.backToMenu(ar_menu))
        back_button.pack(side=BOTTOM)
        back_frame.pack(side=BOTTOM)  # Pack this frame at the bottom of ar_menu

        ar_frame.pack(side=TOP)

        ar_menu.bind('<Return>', lambda event : ar_button.invoke())
        ar_menu.mainloop()

    def removeHelper(user_type, param, ar_list):
        if user_type == "ADMIN":
            admin.remove_course(param)
            GUI.printCourses(user_type, ar_list, "ALL")
        if user_type == "INSTRUCTOR":
            instructor.remove_course(param)
            GUI.printCourses(user_type, ar_list, "ALL")
        if user_type == "STUDENT":
            student.remove_course(param)
            GUI.printCourses(user_type, ar_list, "ALL")

    def addInstructor(user_type, main_app):
        main_app.destroy()
        # ar stands for add/remove
        ar_Instructor = Tk()
        ar_Instructor.title(f"{user_type} Add Instructor")

        # Label for course list
        ar_label = Label(ar_Instructor, width=55, height=5, text = "ADD INSTRUCTOR")
        ar_label.pack()

        # Pulls instructors from the database and adds them to listbox (should pull from different database depending on user)
        ar_list = Listbox(ar_Instructor, bg='white', height=10, width=50, font='Arial')
        GUI.printInstructors(ar_list)
        ar_list.pack()

        # Search box
        ar_frame1 = Frame(ar_Instructor)
        ar_frame2 = Frame(ar_Instructor)
        ar_frame3 = Frame(ar_Instructor)
        ar_frame4 = Frame(ar_Instructor)
        ar_frame5 = Frame(ar_Instructor)
        ar_frame6 = Frame(ar_Instructor)
        ar_frame7 = Frame(ar_Instructor)
        ar_frame8 = Frame(ar_Instructor)
        ar_frame9 = Frame(ar_Instructor)

        # ID
        ar_box1 = Label(ar_frame1, text = "ID: ")
        ar_box1.pack(side=TOP)
        modify_ID = Entry(ar_frame1)
        modify_ID.pack(side=LEFT)
        modify_ID.focus_set()
        # Name
        ar_box2 = Label(ar_frame2, text = "Name: ")
        ar_box2.pack(side=TOP)
        modify_Name = Entry(ar_frame2)
        modify_Name.pack(side=LEFT)
        modify_Name.focus_set()
        # Surname
        ar_box3 = Label(ar_frame3, text = "Surname: ")
        ar_box3.pack(side=TOP)
        modify_Surname = Entry(ar_frame3)
        modify_Surname.pack(side=LEFT)
        modify_Surname.focus_set()
        # Title
        ar_box4 = Label(ar_frame4, text = "Title: ")
        ar_box4.pack(side=TOP)
        modify_Title = Entry(ar_frame4)
        modify_Title.pack(side=LEFT)
        modify_Title.focus_set()
        # Hire year
        ar_box5 = Label(ar_frame5, text = "Hire year: ")
        ar_box5.pack(side=TOP)
        modify_Hireyear = Entry(ar_frame5)
        modify_Hireyear.pack(side=LEFT)
        modify_Hireyear.focus_set()
        # Department
        ar_box6 = Label(ar_frame6, text = "Department: ")
        ar_box6.pack(side=TOP)
        modify_Dept = Entry(ar_frame6)
        modify_Dept.pack(side=LEFT)
        modify_Dept.focus_set()
        # Email
        ar_box7 = Label(ar_frame7, text = "Email: ")
        ar_box7.pack(side=TOP)
        modify_Email = Entry(ar_frame7)
        modify_Email.pack(side=LEFT)
        modify_Email.focus_set()
        # Username
        ar_box8 = Label(ar_frame8, text = "Username: ")
        ar_box8.pack(side=TOP)
        modify_Username = Entry(ar_frame8)
        modify_Username.pack(side=LEFT)
        modify_Username.focus_set()
        # Password
        ar_box9 = Label(ar_frame9, text = "Password: ")
        ar_box9.pack(side=TOP)
        modify_Password = Entry(ar_frame9)
        modify_Password.pack(side=LEFT)
        modify_Password.focus_set()
        

        #ar_button = Button(ar_frame1, text="Add", command=lambda: user.add_course(modify_CRN.get()))
        #ar_button.pack(side=LEFT)
        ar_frame1.pack(side=LEFT)
        ar_frame2.pack(side=LEFT)
        ar_frame3.pack(side=LEFT)
        ar_frame4.pack(side=LEFT)
        ar_frame5.pack(side=LEFT)
        ar_frame6.pack(side=LEFT)
        ar_frame7.pack(side=LEFT)
        ar_frame8.pack(side=LEFT)
        ar_frame9.pack(side=LEFT)


        ar_button = Button(ar_frame9, text="Add", command=lambda: GUI.addInstructorHelper(user_type, ar_list, modify_ID.get(), modify_Name.get(), modify_Surname.get(), modify_Title.get(), modify_Hireyear.get(), modify_Dept.get(), modify_Email.get(), modify_Username.get(), modify_Password.get()))
        ar_button.pack(side=LEFT)


        # Add the "Back to Menu" button
        back_frame = Frame(ar_Instructor)
        back_button = Button(back_frame, text="Back to Menu", command=lambda: GUI.backToMenu(ar_Instructor))
        back_button.pack(side=BOTTOM)
        back_frame.pack(side=BOTTOM)  # Pack this frame at the bottom of ar_menu

        ar_Instructor.bind('<Return>', lambda event : ar_button.invoke())
        ar_Instructor.mainloop()

    def addInstructorHelper(user_type, ar_list, ID, name, surname, title, hireyear, dept, email, username, password):
        cursor.execute("INSERT INTO INSTRUCTOR (ID, NAME, SURNAME, TITLE, HIREYEAR, DEPT, EMAIL, USERNAME, PASSWORD) "
                       "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (ID, name, surname, title, hireyear, dept, email, username, password))
        db_connection.commit()
        GUI.printInstructors(ar_list)

    def printInstructors(ar_list):
        cursor.execute("SELECT * FROM INSTRUCTOR")
        instructors = cursor.fetchall()
        ar_list.delete(0, END)
        for x in instructors:
            ar_list.insert(END, f"{x}")
        

    def removeInstructor(user_type, main_app):
        main_app.destroy()
        # ar stands for add/remove
        ar_Instructor = Tk()
        ar_Instructor.title(f"{user_type} Remove Instructor")

        # Label for course list
        ar_label = Label(ar_Instructor, width=55, height=5, text = "REMOVE INSTRUCTOR")
        ar_label.pack()

        # Pulls courses from the database and adds them to listbox (should pull from different database depending on user)
        ar_list = Listbox(ar_Instructor, bg='white', height=10, width=50, font='Arial')
        GUI.printCourses(user_type, ar_list, "ALL")
        ar_list.pack()

        ar_Instructor.mainloop()


    def addStudent(user_type, main_app):
        main_app.destroy()
        # ar stands for add/remove
        ar_Student = Tk()
        ar_Student.title(f"{user_type} Add Student")

        # Label for course list
        ar_label = Label(ar_Student, width=55, height=5, text = "ADD STUDENT")
        ar_label.pack()

        # Pulls courses from the database and adds them to listbox (should pull from different database depending on user)
        ar_list = Listbox(ar_Student, bg='white', height=10, width=50, font='Arial')
        GUI.printCourses(user_type, ar_list, "ALL")
        ar_list.pack()

        ar_Student.mainloop()

    def removeStudent(user_type, main_app):
        main_app.destroy()
        # ar stands for add/remove
        ar_Student = Tk()
        ar_Student.title(f"{user_type} Remove Student")

        # Label for course list
        ar_label = Label(ar_Student, width=55, height=5, text = "REMOVE STUDENT")
        ar_label.pack()

        # Pulls courses from the database and adds them to listbox (should pull from different database depending on user)
        ar_list = Listbox(ar_Student, bg='white', height=10, width=50, font='Arial')
        GUI.printCourses(user_type, ar_list, "ALL")
        ar_list.pack()

        ar_Student.mainloop()

    # Test GUI functions (optional)
    def testGUI():
        r = tk.Tk()
        r.title('Counting Seconds')
        button = tk.Button(r, text='Stop', width=25, command=r.destroy)
        button.pack()
        #r.mainloop()

    def testGUI2():
        r = tk.Tk()
        r.title('Counting Seconds')
        button = tk.Button(r, text='Stop', width=25, command=r.destroy)
        button.pack()
        r.mainloop()

# Call the login function to start the application
GUI.login()



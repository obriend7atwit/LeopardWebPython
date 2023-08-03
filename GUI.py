from encodings import search_function
from tkinter import *
import tkinter as tk
import sqlite3
from Database import *

# Connect to the database
db_connection = sqlite3.connect("assignment5.db")
cursor = db_connection.cursor()

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
            button4 = tk.Button(main_app, text="Add/Remove Instructor from the system", bg='red', command=lambda: print("Button 4 clicked"))
            button5 = tk.Button(main_app, text="Add/Remove Student from the system", bg='red', command=lambda: print("Button 5 clicked"))
            button6 = tk.Button(main_app, text="Exit", bg='red', command=main_app.destroy)

            # Pack buttons
            button1.pack()
            button2.pack()
            button3.pack()
            button4.pack()
            button5.pack()
            button6.pack()

        elif user_type == "INSTRUCTOR":
            main_app['background'] = '#FFF98A'
            menu_label['background'] = '#FFF98A'
            # Add buttons for instructor actions
            button1 = tk.Button(main_app, text="Add course to semester schedule", bg='yellow', command=lambda: GUI.addCourse(user_type, main_app))
            button2 = tk.Button(main_app, text="Remove course from semester schedule", bg='yellow', command=lambda: GUI.removeCourse(user_type, main_app))
            button3 = tk.Button(main_app, text="Search for course(s)", bg='yellow', command=lambda: GUI.searchCourses(user_type, main_app))
            button4 = tk.Button(main_app, text="Print course roster", bg='yellow', command=lambda: print("Button 3 clicked"))
            button5 = tk.Button(main_app, text="Exit", bg='yellow', command=main_app.destroy)

            # Pack buttons
            button1.pack()
            button2.pack()
            button3.pack()
            button4.pack()
            button5.pack()

        elif user_type == "STUDENT":
            main_app['background'] = '#AFFC9A'
            menu_label['background'] = '#AFFC9A'
            # Add buttons for student actions
            button1 = tk.Button(main_app, text="Add course to student schedule", bg='#30D402', command=lambda: GUI.addCourse(user_type, main_app))
            button2 = tk.Button(main_app, text="Remove course from student schedule", bg='#30D402', command=lambda: GUI.removeCourse(user_type, main_app))
            button3 = tk.Button(main_app, text="Search for course(s)", bg='#30D402', command=lambda:GUI.searchCourses(user_type, main_app))
            button4 = tk.Button(main_app, text="Search all courses", bg='#30D402', command=lambda: print("Button 3 clicked"))
            button5 = tk.Button(main_app, text="Exit", bg='#30D402', command=main_app.destroy)

            # Pack buttons
            button1.pack()
            button2.pack()
            button3.pack()
            button4.pack()
            button5.pack()

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
        search_label = Label(search_menu, width=55, height=5, text = "ALL COURSES")
        search_label.pack()

        # Pulls courses from the database and adds them to listbox (should pull from different database depending on user)
        search_list = Listbox(search_menu, bg='white', height=10, width=50, font='Arial')
        search_list.pack()

        # Search box
        sb_frame = Frame(search_menu)
        search_box = Label(sb_frame, text = "Search for course: ")
        search_box.pack()

        modify = Entry(sb_frame)
        modify.pack(side=LEFT, fill=BOTH, expand=1)
        modify.focus_set()

        search_button = Button(sb_frame, text="Search", command=lambda: GUI.printCourses(user_type, search_list, modify.get()))
        search_button.pack(side=LEFT)
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
        ar_list.pack()
        #printCourses(user_type, ar_list)

        # Search box
        ar_frame = Frame(ar_menu)

        # CRN
        ar_box = Label(ar_frame, text = "CRN: ")
        ar_box.pack(side=BOTTOM)
        modify_CRN = Entry(ar_frame)
        modify_CRN.pack(side=LEFT, fill=BOTH, expand=1)
        modify_CRN.focus_set()
        # Title
        ar_box = Label(ar_frame, text = "Title: ")
        ar_box.pack(side=LEFT)
        modify_Title = Entry(ar_frame)
        modify_Title.pack(side=LEFT, fill=BOTH, expand=1)
        modify_Title.focus_set()
        # Department
        ar_box = Label(ar_frame, text = "Department: ")
        ar_box.pack(side=LEFT)
        modify_Dept = Entry(ar_frame)
        modify_Dept.pack(side=LEFT, fill=BOTH, expand=1)
        modify_Dept.focus_set()
        # Start time
        ar_box = Label(ar_frame, text = "Start time (military): ")
        ar_box.pack(side=LEFT)
        modify_sTime = Entry(ar_frame)
        modify_sTime.pack(side=LEFT, fill=BOTH, expand=1)
        modify_sTime.focus_set()
        # End time
        ar_box = Label(ar_frame, text = "End time (military): ")
        ar_box.pack(side=LEFT)
        modify_eTime = Entry(ar_frame)
        modify_eTime.pack(side=LEFT, fill=BOTH, expand=1)
        modify_eTime.focus_set()
        # Days
        ar_box = Label(ar_frame, text = "Days: ")
        ar_box.pack(side=LEFT)
        modify_Days = Entry(ar_frame)
        modify_Days.pack(side=LEFT, fill=BOTH, expand=1)
        modify_Days.focus_set()
        # Semester
        ar_box = Label(ar_frame, text = "Semester: ")
        ar_box.pack(side=LEFT)
        modify_Semester = Entry(ar_frame)
        modify_Semester.pack(side=LEFT, fill=BOTH, expand=1)
        modify_Semester.focus_set()
        # Year
        ar_box = Label(ar_frame, text = "Year: ")
        ar_box.pack(side=LEFT)
        modify_Year = Entry(ar_frame)
        modify_Year.pack(side=LEFT, fill=BOTH, expand=1)
        modify_Year.focus_set()
        # Credits
        ar_box = Label(ar_frame, text = "Credits: ")
        ar_box.pack(side=LEFT)
        modify_Credits = Entry(ar_frame)
        modify_Credits.pack(side=LEFT, fill=BOTH, expand=1)
        modify_Credits.focus_set()
        # Instructor
        ar_box = Label(ar_frame, text = "Instructor: ")
        ar_box.pack(side=LEFT)
        modify_Instructor = Entry(ar_frame)
        modify_Instructor.pack(side=LEFT, fill=BOTH, expand=1)
        modify_Instructor.focus_set()

        ar_button = Button(ar_frame, text="Add", command=lambda: user.add_course(modify.get()))
        ar_button.pack(side=LEFT)
        ar_button.pack(side=RIGHT)

        # Add the "Back to Menu" button
        back_button = Button(ar_frame, text="Back to Menu", bg='red', command=lambda: GUI.backToMenu(ar_menu))
        back_button.pack(side=RIGHT)

        ar_frame.pack(side=TOP)

        ar_menu.bind('<Return>', lambda event : ar_button.invoke())
        ar_menu.mainloop()

    def addHelper(user_type, params, ar_list):
        if user_type == "ADMIN":
            admin.add_course(params)
            GUI.printCourses(user_type, ar_list, "ALL")
        if user_type == "INSTRUCTOR":
            instructor.add_course(params)
            GUI.printCourses(user_type, ar_list, "ALL")
        if user_type == "STUDENT":
            student.add_course(params)
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
        ar_box = Label(ar_frame, text = "Search for course: ")
        ar_box.pack()

        modify = Entry(ar_frame)
        modify.pack(side=LEFT, fill=BOTH, expand=1)
        modify.focus_set()
        
        ar_button = Button(ar_frame, text="Remove", command=lambda: GUI.removeHelper(user_type, modify.get(), ar_list))
        ar_button.pack(side=LEFT)
        ar_button.pack(side=RIGHT)

        # Create a frame for the "Back to Menu" button at the bottom
        back_frame = Frame(ar_menu)
        back_button = Button(back_frame, text="Back to Menu", bg='red', command=lambda: GUI.backToMenu(ar_menu))
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



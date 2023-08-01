from encodings import search_function
from tkinter import *
import tkinter as tk
import sqlite3
from Database import *
# ... (The rest of import statements and class definitions go here)

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
        password = tk.Entry()

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

        login.mainloop()

    # Helper function to get the Entry widget value
    def checkEntry(entry):
        entry.get()

    # Function for user authentication
    def auth(username, password, login_window):
        # Authenticating the user
        user = None  # Initialize user to None
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
            button1 = tk.Button(main_app, text="Add/Remove course from semester schedule", bg='red', command=lambda: print("Button 1 clicked"))
            button2 = tk.Button(main_app, text="Search for course(s)", bg='red', command=lambda: GUI.searchCourses(user_type, main_app))
            button3 = tk.Button(main_app, text="Add/Remove Instructor from the system", bg='red', command=lambda: print("Button 3 clicked"))
            button4 = tk.Button(main_app, text="Add/Remove Student from the system", bg='red', command=lambda: print("Button 4 clicked"))
            button5 = tk.Button(main_app, text="Add/Remove Course to system", bg='red', command=lambda: print("Button 5 clicked"))
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
            button1 = tk.Button(main_app, text="Add course to semester schedule", bg='yellow', command=lambda: print("Button 1 clicked"))
            button2 = tk.Button(main_app, text="Search for course(s)", bg='yellow', command=lambda: print("Button 2 clicked"))
            button3 = tk.Button(main_app, text="Print course roster", bg='yellow', command=lambda: print("Button 3 clicked"))
            button4 = tk.Button(main_app, text="Exit", bg='yellow', command=main_app.destroy)

            # Pack buttons
            button1.pack()
            button2.pack()
            button3.pack()

        elif user_type == "STUDENT":
            main_app['background'] = '#AFFC9A'
            menu_label['background'] = '#AFFC9A'
            # Add buttons for student actions
            button1 = tk.Button(main_app, text="Add course to semester schedule", bg='#30D402', command=lambda: print("Button 1 clicked"))
            button2 = tk.Button(main_app, text="Search for course(s)", bg='#30D402', command=lambda: print("Button 2 clicked"))
            button3 = tk.Button(main_app, text="Search all courses", bg='#30D402', command=lambda: print("Button 3 clicked"))
            button4 = tk.Button(main_app, text="Exit", bg='#30D402', command=main_app.destroy)

            # Pack buttons
            button1.pack()
            button2.pack()
            button3.pack()

        main_app.mainloop()

    # Search for courses
    def searchCourses(user_type, main_app):
        main_app.destroy()
        search_menu = Tk()
        search_menu.title(f"{user_type} Search application")

        # Label for course list
        search_label = Label(search_menu, width=50, height=10, text = "ALL COURSES")
        search_label.pack()

        # Pulls courses from the database and adds them to listbox (should pull from different database depending on user)
        search_list = Listbox(search_menu, bg='white', height=10, width=30, font='Arial')

        #if user_type == "ADMIN":
        #    admin_courses = 
        search_list.insert(1, "Test1")
        search_list.insert(2, "Test2")
        search_list.insert(3, "Test3")
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



        button1 = tk.Button(search_menu, text="Back", bg='red', command=lambda: print("Button 2 clicked"))
        button1.pack()

        search_menu.mainloop()

    def printCourses(user_type, search_list, search_term):
        if user_type == 'ADMIN':
            courses = admin.search_courses(search_term)
            search_list.delete(0, END)
            for x in courses:
                search_list.insert(END, f"{x}")
        elif user_type == 'INSTRUCTOR':
            search_list.insert(1, "Admin courses")
        elif user_type == 'STUDENT':
            search_list.insert(1, "Admin courses")

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



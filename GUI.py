from tkinter import *
import tkinter as tk
from Database import *
#from LeopardWebPython import *

db_connection = sqlite3.connect("assignment5.db")
cursor = db_connection.cursor()

# Creating instances of Admin, Instructor, and Student
admin = Admin(db_connection)
instructor = Instructor(db_connection)
student = Student(db_connection)

user = None

class GUI:
    def login():
        login = Tk()
        login.title("Login")

        query = tk.Label(
            text="Please enter your username and password",
            width=50,
            height=10
            )

        usern = tk.Label(
            text = "Username: ",
            width = 10,
            height = 1
            )

        passw = tk.Label(
            text = "Password: ",
            width = 10,
            height = 1
            )

        username = tk.Entry()
        password = tk.Entry()

        query.pack()
        usern.pack()
        username.pack()
        passw.pack()
        password.pack()
        u = GUI.checkEntry(username)
        p = GUI.checkEntry(username)
        confirm = tk.Button(login, text='Confirm', width=15, command= lambda : GUI.auth(username.get(), password.get()))
        confirm.pack()

        login.mainloop()

    def checkEntry(entry):
        entry.get()

    def auth(username, password):
        # Authenticating the user
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
        return user


    def display_menu(user_type):
        #user_type = user
        print("MENU:")

        if user_type == "ADMIN":
            print("1. Add/Remove course from semester schedule")
            print("2. Search for course(s)")
            print("3. Add/Remove Instructor from the system")
            print("4. Add/Remove Student from the system")
            print("5. Add/Remove Course to system")
            print("6. Exit")
        if user_type == "INSTRUCTOR":
            print("1. Add course to semester schedule")
            print("2. Search for course(s)")
            print("3. Print course roster")
        if user_type == "STUDENT":
            print("1. Add course to semester schedule")
            print("2. Search for course(s)")
            print("3. Search all courses")


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



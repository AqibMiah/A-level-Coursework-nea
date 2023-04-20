
import tkinter as tk #importing the tkinter library to create my UI
import sqlite3 #importing the sql library to run sql commands
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter import messagebox
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import matplotlib.pyplot as plt

conn = sqlite3.connect("Coursework database.db") #connects my database to this python file
cur = conn.cursor() # creates a cursor to navigate through the database and make changes

#Function to create my database
def setupDB():
    cur.execute("""CREATE TABLE IF NOT EXISTS "tbl_Employees" (
    "employeeID" TEXT NOT NULL UNIQUE,
	"firstname" TEXT NOT NULL,
	"lastname" TEXT NOT NULL,
	"username" TEXT NOT NULL UNIQUE,
	"phoneNumber" TEXT NOT NULL UNIQUE,
	"email" TEXT NOT NULL UNIQUE,
	"gender" TEXT NOT NULL,
	"password" TEXT NOT NULL,
	"dateOfBirth" TEXT NOT NULL,
	"managerID" TEXT NOT NULL,
	PRIMARY KEY("employeeID"),
	FOREIGN KEY("managerID") REFERENCES "tbl_Managers"("managerID"))""")

    cur.execute("""CREATE TABLE IF NOT EXISTS "tbl_Managers" (
	"managerID"	TEXT NOT NULL UNIQUE,
	"firstname"	TEXT NOT NULL,
	"lastname"	TEXT NOT NULL,
	"username"	TEXT NOT NULL UNIQUE,
	"phoneNumber"	TEXT NOT NULL UNIQUE,
	"email"	TEXT NOT NULL UNIQUE,
	"gender"	TEXT NOT NULL,
	"password"	TEXT NOT NULL,
	"dateOfBirth"	TEXT NOT NULL,
	PRIMARY KEY("managerID"))""")

    cur.execute("""CREATE TABLE IF NOT EXISTS "tbl_Inventory" (
	"productID"	TEXT NOT NULL UNIQUE,
	"productName"	TEXT NOT NULL,
	"productType"	TEXT NOT NULL,
	"quantity"	INTEGER NOT NULL,
	"price"	REAL NOT NULL,
	"supplierID"	TEXT NOT NULL,
	"stockLimit" INTEGER NOT NULL,
	PRIMARY KEY("productID"),
	FOREIGN KEY("supplierID") REFERENCES "tbl_suppliers"("supplierID"))""")

    cur.execute("""CREATE TABLE IF NOT EXISTS "tbl_Orders" (
	"orderID"	TEXT NOT NULL UNIQUE,
	"orderQuantity"	INTEGER NOT NULL,
	"productID"	TEXT NOT NULL,
	"managerID"	TEXT NOT NULL,
	PRIMARY KEY("orderID"),
	FOREIGN KEY("productID") REFERENCES "tbl_Inventory"("productID"),
	FOREIGN KEY("managerID") REFERENCES "tbl_Managers"("managerID"))""")

    cur.execute("""CREATE TABLE IF NOT EXISTS "tbl_suppliers" (
	"supplierID"	TEXT NOT NULL UNIQUE,
	"supplierName"	TEXT NOT NULL UNIQUE,
	"supplierEmail"	TEXT NOT NULL UNIQUE,
	"supplierNumber"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("supplierID"))""")

conn.commit() #commits the changes made to the database file

def createChartForMM():
    cur.execute("SELECT productID, SUM(orderQuantity) as total_quantity "
                "FROM tbl_Orders "
                "WHERE productID IN ('PD0001', 'PD0002', 'PD0003', 'PD0004', 'PD0005', 'PD0006', 'PD0007', 'PD0008', 'PD0009', 'PD0010')"
                "GROUP BY productID")
    MMChartData = cur.fetchall()
    print(MMChartData)

    MMChart_totals = {}
    for product in MMChartData:
        MMChart_totals[product[0]] = product[1]

    MMChartNames = list(MMChart_totals.keys())
    MMChartValues = list(MMChart_totals.values())

    plt.title('Report')
    plt.xlabel('ProductID')
    plt.ylabel('Total Order Quantity')
    axis = plt.gca()
    axis.xaxis.set_tick_params(labelsize=6)

    plt.bar(range(len(MMChart_totals)), MMChartValues, tick_label=MMChartNames)

    fileName = 'Products MM Data'
    plt.savefig(os.path.expanduser(f'~/Downloads/{fileName}'))
    plt.close()




"""
#populate employee table
employeeFile=open("employeeTable.csv","r") #opening up a ready made csv file and reading its contents
for employeeLine in employeeFile:
    employeeLine = employeeLine.strip() #this justs removes blank spaces at the end and front usually \n
    employeeID,firstname,lastname,username,phoneNumber,email,gender,password,dateOfBirth,managerID=employeeLine.split(",")
    cur.execute("INSERT INTO tbl_Employees VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [employeeID,firstname,lastname,username,phoneNumber,email,gender,password,dateOfBirth,managerID])

#populate manager table
managerFile=open("managerTable.csv","r")
for managerLine in managerFile:
    managerLine = managerLine.strip()
    managerID,firstname,lastname,username,phoneNumber,email,gender,password,dateOfBirth=managerLine.split(",")
    cur.execute("INSERT INTO tbl_Managers VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", [managerID,firstname,lastname,username,phoneNumber,email,gender,password,dateOfBirth])

#populate inventory table
inventoryFile=open("inventoryTable.csv","r")
for inventoryLine in inventoryFile:
    inventoryLine = inventoryLine.strip()
    productID,productName,productType,quantity,price,supplierID,stockLimit = inventoryLine.split(",")
    cur.execute("INSERT INTO tbl_Inventory VALUES (?, ?, ?, ?, ?, ?, ?)", [productID,productName,productType,quantity,price,supplierID,stockLimit])

#populate order table
orderFile=open("orderTable.csv","r")
for orderLine in orderFile:
    orderLine = orderLine.strip()
    orderID,orderQuantity,productID,managerID = orderLine.split(",")
    cur.execute("INSERT INTO tbl_Orders VALUES (?, ?, ?, ?)", [orderID,orderQuantity,productID,managerID])

#populate supplier table
supplierFile=open("supplierTable.csv","r")
for supplierLine in supplierFile:
    supplierLine = supplierLine.strip()
    supplierID,supplierName,supplierEmail,supplierNumber = supplierLine.split(",")
    cur.execute("INSERT INTO tbl_Suppliers VALUES (?, ?, ?, ?)", [supplierID,supplierName,supplierEmail,supplierNumber])

conn.commit()
"""

window = tk.Tk()

#window.iconbitmap("/Users/aqibmiah/Desktop/BP logo.png")
window.geometry("1450x1000")
window.title("BP Express")
window.config(bg="WHITE")

bpExpress_label = tk.Label(text="BP Express", bg="WHITE", fg="BLACK")
bpExpress_label.config(font=('Helvetica bold', 16))
bpExpress_label.place(anchor="nw")  # anchor to the top left side of the screen

bplogo_image = Image.open("BP logo.png").resize((28,24)) #load image and resize
bplogo_image_login= ImageTk.PhotoImage(bplogo_image) #use correct library for the use of an image

bplogo_panel = tk.Label(image=bplogo_image_login) #create a label where the picture goes
bplogo_panel.image=bplogo_image_login #use correct library to properly display image
bplogo_panel.place(x=1415, y=920)#place the picture

eye_image = Image.open("Eye Icon.png").resize((28,24)) #load image and resize
eye_image_login= ImageTk.PhotoImage(eye_image) #use correct library for the use of an image



def loginPage(): #created a function called loginPage
    global passwordLoginEntry
    global isManager
    global idEntry

    login_label = tk.Label(text="Log In", bg="WHITE", fg="BLACK", font=('Helvetica bold', 50))  # create a label to display the title of the page
    login_label.place(x=655, y=0)  # place the widget on the screen at a specific coordinate

    rumanager_label = tk.Label(text="Are you a Manager?", bg="WHITE", fg="BLACK", font=('Helvetica bold', 16))
    rumanager_label.place(x=655, y=175)

    emLoginLabel = tk.Label(text="EmployeeID", bg="WHITE", fg="BLACK", font=('Helvetica bold', 16))
    emLoginLabel.place(x=575, y=250)


    def renderLoginPage(): #Function to change the ID label when a specific radiobutton is pressed

        if not isManager.get(): #Checks if the person is an employee or a manager
            emLoginLabel.config(text="EmployeeID", bg="WHITE", fg="BLACK", font=('Helvetica bold', 16))#change the label text depending on the condition
        else:
            emLoginLabel.config(text="ManagerID", bg="WHITE", fg="BLACK", font=('Helvetica bold', 16))#change the label text depending on the condition

    idEntry = tk.Entry(bg="ORANGE", fg="WHITE") #Create an entry box to input their ID
    idEntry.place(x=675, y=250)

    passwordLoginLabel = tk.Label(text="Password", bg="WHITE", fg="BLACK", font=('Helvetica bold', 16))# Create a Label to show where to enter the password
    passwordLoginLabel.place(x=575, y=290)

    passwordLoginEntry = tk.Entry(bg="ORANGE", fg="WHITE")# creates and entry box to enter the password
    passwordLoginEntry.config(show="*") #Disguise the actual text in "*" signs which will make the password more secure
    passwordLoginEntry.place(x=675, y=290)

    def eyeIconLoginBtn():  # function to display eye icon
        eyeIconBtn = tk.Button(image=eye_image_login, command=lambda: showPassLogin(eyeIconBtn))  # createa button with that image and pass in parameters via a function
        eyeIconBtn.place(x=870, y=290)

    eyeIconLoginBtn()  # call function to be displayed

    def showPassLogin(eyeIconBtn):  # function to show the password entered
        eyeIconBtn.place_forget()  # hide the eye icon button
        passwordLoginEntry.config(show="")#change the way the password is viewed. now it will be represented with nothing and can be viewed normaly
        eyeIconBtn2 = tk.Button(image=eye_image_login, command=lambda: hidePassLogin(eyeIconBtn2))  # create a new eye icon to hide the password
        eyeIconBtn2.place(x=870, y=290)

    def hidePassLogin(eyeIconBtn2):  # function to hide the password entered
        eyeIconBtn2.place_forget()  # hides the hide eye icon
        passwordLoginEntry.config(show="*")#change the way the password is viewed. now it will be represented * signs
        eyeIconLoginBtn()  # call the function which contains the original eye icon essentially looping everything


    createAccLoginBtn = tk.Button(text="Create Account", bg="ORANGE",fg="BLACK", command=lambda: createAccountPage(), height=3, width=10) #create a button going to the create account page
    createAccLoginBtn.place(x=610, y=340)

    loginAccLoginBtn = tk.Button(text="Login", bg="ORANGE", fg="BLACK", command=lambda: attemptLogin(idEntry, passwordLoginEntry), height=3, width=10)#create a button going to validate the login details
    loginAccLoginBtn.place(x=760, y=340)

    isManager = tk.BooleanVar(window, value=False)  # Create a variable for strings, and initialize the variable
    tk.Radiobutton(window, text="YES", variable=isManager, value=True, bg="ORANGE", fg="WHITE", command=renderLoginPage).place(x=660, y=210)  # create a radio button with text = yes and configured features
    tk.Radiobutton(window, text="NO", variable=isManager, value=False, bg="ORANGE", fg="WHITE", command=renderLoginPage).place(x=750, y=210)


loginPage() # call the login page so something can be shown when first runnning the code.


def createAccountPage(): #define function to create an account
    global passwordEntry
    global reenterPasswordEntry
    global isManager
    #globalise 3 variables to be used everywhere

    window.withdraw()# withdraw window called window

    createAccountPageTop = tk.Toplevel(bg="WHITE")#create a new top level window
    createAccountPageTop.geometry("1450x1000")#set new window measurments

    createAccountLabel = tk.Label(createAccountPageTop, text="Create Account", bg="WHITE", fg="BLACK", font=('Helvetica bold', 50))# create a label to display text
    createAccountLabel.pack(side="top")# place the label at the top of the screen which automatically places it in the centre

    firstNameLabel = tk.Label(createAccountPageTop, text="First Name: ", bg="WHITE", fg="BLACK", font=('Helvetica bold', 16))#create a label called first name
    firstNameLabel.place(x=300, y=100)
    firstNameEntry = tk.Entry(createAccountPageTop, bg ="ORANGE", fg="WHITE")#create an entry box to enter the first name
    firstNameEntry.place(x=430, y=100)

    lastNameLabel = tk.Label(createAccountPageTop, text="Last Name: ", bg="WHITE", fg="BLACK", font=('Helvetica bold', 16))#create a label called last name
    lastNameLabel.place(x=300, y=150)
    lastNameEntry = tk.Entry(createAccountPageTop, bg="ORANGE", fg="WHITE")#create an entry box to enter the last name
    lastNameEntry.place(x=430, y=150)

    isManagerLabel = tk.Label(createAccountPageTop, text="Are You A Manager?", bg="WHITE", fg="BLACK", font=('Helvetica bold', 16))#create a label with text Are you a manager
    isManagerLabel.place(x=370, y=200)

    emIDLabel = tk.Label(createAccountPageTop, text="EmployeeID: ", bg="WHITE", fg="BLACK", font=('Helvetica bold', 16))#create a label with text EmployeeID
    emIDLabel.place(x=300, y=280)
    emIDEntry = tk.Entry(createAccountPageTop, bg="ORANGE", fg="WHITE")#create an entry box to input their ID
    emIDEntry.place(x=430, y=280)

    def showWhatManager():
        global whatManagerLabel
        global whatManagerEntry
        whatManagerLabel = tk.Label(createAccountPageTop, text = "ManagerID: ", bg="WHITE", fg="BLACK", font=('Helvetica bold', 16)) #create a label asking for managerID
        whatManagerLabel.place(x=300, y=330)
        whatManagerEntry = tk.Entry(createAccountPageTop, bg="ORANGE", fg="WHITE")
        whatManagerEntry.place(x=430, y=330)
    showWhatManager()

    def hideWhatManager():
        whatManagerLabel.place_forget()#hides the label
        whatManagerEntry.place_forget()

    def renderCreateAccPage():#function to change the text of the id, if they press yes then they get a different label shown and vice versa
        if not isManagerCA.get():#gets the value isManager since it is boolean it can use the not function to reverse the boolean expression
            emIDLabel.config(text="EmployeeID: ", bg="WHITE", fg="BLACK", font=('Helvetica bold', 16))# changes the label called emIDLabel to fit the characteristic of the radio button choice
            showWhatManager()
        else:
            emIDLabel.config(text="ManagerID: ", bg="WHITE", fg="BLACK", font=('Helvetica bold', 16))
            hideWhatManager()



    dobLabel = tk.Label(createAccountPageTop, text="Date Of Birth: ", bg="WHITE", fg="BLACK", font=('Helvetica bold', 16))#create a label with text Date Of Birth
    dobLabel.place(x=830, y=100)



    days = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]# Create a list of possible day choices
    daysClicked = tk.StringVar()# store the result as a string and in daysClicked
    daysClicked.set("DD")#Set the initial value to DD for the day
    daysDrop = tk.OptionMenu(createAccountPageTop, daysClicked, *days)#create the drop down menu and use the values from the days list and store in daysClicked
    daysDrop.config(bg="ORANGE", fg="WHITE")# change the colour of the drop down menu
    daysDrop.place(x=770, y=150)


    months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]# Create a list of possible month choices
    monthsClicked = tk.StringVar()# store the result as a string and in monthsClicked
    monthsClicked.set("MM")#Set the initial value to MM for the month
    monthsDrop = tk.OptionMenu(createAccountPageTop, monthsClicked, *months)#create the drop down menu and use the values from the months list and store in monthsClicked
    monthsDrop.config(bg="ORANGE", fg="WHITE")# change the colour of the drop down menu
    monthsDrop.place(x=850, y=150)

    dobYearEntry = tk.Entry(createAccountPageTop, bg="ORANGE", fg="WHITE", width=8)# create an entry box to enter the year since there will be too many values to put in the list
    dobYearEntry.place(x=935, y=150)

    genderLabel = tk.Label(createAccountPageTop, text="Gender", bg="WHITE", fg="BLACK", font=('Helvetica bold', 16))#create a label with text gender
    genderLabel.place(x=847, y=190)

    phoneNumberLabel = tk.Label(createAccountPageTop, text="Phone Number:", bg="WHITE", fg="BLACK", font=('Helvetica bold', 16))#create a label with text Phone Number
    phoneNumberLabel.place(x=730, y=280)
    phoneNumberEntry = tk.Entry(createAccountPageTop, bg="ORANGE", fg="WHITE")#create an entry box for the input of the phone number
    phoneNumberEntry.place(x=890, y=280)

    emailLabel = tk.Label(createAccountPageTop, text="Email: ", bg="WHITE", fg="BLACK", font=('Helvetica bold', 16))#create a label with text email
    emailLabel.place(x=730, y=330)
    emailEntry = tk.Entry(createAccountPageTop, bg="ORANGE", fg="WHITE")# create an entry box to enter the email
    emailEntry.place(x=890, y=330)

    passwordLabel = tk.Label(createAccountPageTop, text="Password:", bg="WHITE", fg="BLACK", font=('Helvetica bold', 16))#create a password label
    passwordLabel.place(x=730, y=380)
    passwordEntry = tk.Entry(createAccountPageTop, bg="ORANGE", fg="WHITE")#create an entry box to enter password
    passwordEntry.config(show="*")
    passwordEntry.place(x=890, y=380)

    reenterPasswordLabel = tk.Label(createAccountPageTop, text="Re-enter Password:", bg="WHITE", fg="BLACK", font=('Helvetica bold', 16))#create a re-enter password label
    reenterPasswordLabel.place(x=730, y=430)
    reenterPasswordEntry = tk.Entry(createAccountPageTop, bg="ORANGE", fg="WHITE")#create an entry box to re-enter enter password
    reenterPasswordEntry.config(show="*")
    reenterPasswordEntry.place(x=890, y=430)



    loginCreateAccBtn = tk.Button(createAccountPageTop, text="Login Page", bg="ORANGE",fg="BLACK", command=lambda: showLoginPage(createAccountPageTop), height=3, width=10)#create a button to go back to the login page
    loginCreateAccBtn.place(x=550, y=520)

    createAccountCreateAccBtn = tk.Button(createAccountPageTop, text="Create Account", bg="ORANGE", fg="BLACK", height=3, width=10, command=lambda: validateCreateAccount())#create a button to proceed with the account being logged into
    createAccountCreateAccBtn.place(x=710, y=520)

    whatGender = tk.StringVar(createAccountPageTop)# create a variable for strings
    tk.Radiobutton(createAccountPageTop, text="Male", variable=whatGender, value="M", bg="ORANGE", fg="WHITE", width=7).place(x=800, y=220)#create a radio button with configured features
    tk.Radiobutton(createAccountPageTop, text="Female", variable=whatGender, value="F", bg="ORANGE", fg="WHITE", width=7).place(x=890, y=220)


    isManagerCA = tk.BooleanVar(createAccountPageTop, value=False)  # Create a variable for boolean, and initialize the variable
    tk.Radiobutton(createAccountPageTop, text="YES", variable=isManagerCA, value=True, bg="ORANGE", fg="WHITE", command=renderCreateAccPage).place(x=380, y=235)#create a radio button with text = yes and configured features
    tk.Radiobutton(createAccountPageTop, text="NO", variable=isManagerCA, value=False, bg="ORANGE", fg="WHITE", command=renderCreateAccPage).place(x=460, y=235)

    def eyeIconCreateAccBtn():  # function to display eye icon
        eyeIconBtn3 = tk.Button(createAccountPageTop, image=eye_image_login, command=lambda: showPassCreateAcc(eyeIconBtn3))#create a button with that image and pass in parameters via a function
        eyeIconBtn3.place(x=1090, y=380)

    eyeIconCreateAccBtn()

    def eyeIconCreateAccReenter():
        eyeIconBtn5 = tk.Button(createAccountPageTop, image=eye_image_login, command=lambda: showPassCreateAccReenter(eyeIconBtn5))#create a button with that image and pass in parameters via a function
        eyeIconBtn5.place(x=1090, y=430)

    eyeIconCreateAccReenter()

    def showPassCreateAcc(eyeIconBtn3):
        eyeIconBtn3.place_forget()
        passwordEntry.config(show="")
        eyeIconBtn4 = tk.Button(createAccountPageTop, image=eye_image_login, command=lambda: hidePassCreateAcc(eyeIconBtn4))
        eyeIconBtn4.place(x=1090, y=380)

    def hidePassCreateAcc(eyeIconBtn4):
        eyeIconBtn4.place_forget()
        passwordEntry.config(show="*")
        eyeIconCreateAccBtn()

    def showPassCreateAccReenter(eyeIconBtn5):
        eyeIconBtn5.place_forget()
        reenterPasswordEntry.config(show="")
        eyeIconBtn6 = tk.Button(createAccountPageTop, image=eye_image_login, command=lambda: hidePassCreateAccReenter(eyeIconBtn6))
        eyeIconBtn6.place(x=1090, y=430)

    def hidePassCreateAccReenter(eyeIconBtn6):
        eyeIconBtn6.place_forget()
        reenterPasswordEntry.config(show="*")
        eyeIconCreateAccReenter()

    def validateCreateAccount():
        firstName = firstNameEntry.get()
        lastName = lastNameEntry.get()
        emID = emIDEntry.get()
        phoneNumber = phoneNumberEntry.get()
        email = emailEntry.get()
        password = passwordEntry.get()
        reenterPassword = reenterPasswordEntry.get()
        whatManager = whatManagerEntry.get()
        firstNameflag = False
        lastNameflag = False
        idFlag = False
        internalIDFlag1 = False
        internalIDFlag2 = False
        internalIDFlag5 = False
        phoneNumberFlag = False
        internalDigitFlag = False
        internal11Flag = False
        internal07Flag = False
        emailFlag = False
        passwordFlag = False
        internalPasswordLenFlag = False
        internalPasswordUpperFlag = False
        internalPasswordLowerFlag = False
        internalPasswordSymbolFlag = False
        internalPasswordDigitFlag = False
        reenterPasswordFlag = False
        whatManagerFlag = False
        internalIDFlag3 = False
        internalIDFlag4 = False
        internalIDFlag6 = False

        #fetch the details entered by the user and create multiple boolean flags to use later

        if firstName.isalpha(): #check if the name is only letters
            firstNameSanitation = firstName[0].upper() + firstName[1:].lower() #sanitaise the name so the first letter is capitalised
            firstNameflag = True # toggle flag
        else:
            messagebox.showerror('First name error', 'Your first name isnt only letters, make sure that there are only letters in your first name')# show error message

        if lastName.isalpha():
            lastNameSanitation = lastName[0].upper() + lastName[1:].lower()#sanitaise the name so the first letter is capitalised
            lastNameflag = True
        else:
            messagebox.showerror('Last name error', 'Your last name isnt only letters, make sure that there are only letters in your last name')# show error message

        if not isManagerCA.get(): #checks if the user is a manager or an employee
            cur.execute("SELECT * FROM tbl_Employees WHERE employeeID=?", [emID])# checks for the user in the employee table
            emNoID = cur.fetchone() is None #returns true or false if record exists or not

            if emNoID == False: #Check if the ID exists or not
                messagebox.showerror('EmployeeID Exists', 'Your employeeID already exists, please choose a different one')# show error message
            else:
                internalIDFlag1 = True

            if emID[0:2] != "EM": # checks if the first 2 letters are right or not
                messagebox.showerror('ID error', 'The employeeID doesnt start of with the letters "EM", which must be changed and it must be followed by 4 numbers')# show error message
            else:
                internalIDFlag2 = True


            if len(emID) != 6: # checks if the length of the ID is 6 characters or not
                messagebox.showerror('ID Error', 'Make sure the length of the ID is 6 with EM at the start and 4 numbers after it')# show error message
            else:
                internalIDFlag5 = True

            numbersEmID = (emID[2:6]) # gets the last 4 characters of the entered ID


            if numbersEmID.isnumeric() == False: #Check if the last 4 characters are numbers or not
                messagebox.showerror('ID Error', 'Make sure the length of the ID is 6 with EM at the start and 4 numbers after it')# show error message
            else:
                internalIDFlag6 = True

            if internalIDFlag1 and internalIDFlag2 and internalIDFlag5 and internalIDFlag6 == True:
                idFlag = True

        else:
            cur.execute("SELECT * FROM tbl_Managers WHERE managerID=?", [emID])#Check manager table
            maNoID = cur.fetchone() is None

            if maNoID == False:#Check if the ID exists or not
                messagebox.showerror('ManagerID Exists', 'Your managerID already exists, please choose a different one')# show error message
            else:
                internalIDFlag1 = True

            if emID[0:2] != "MA": # checks if the first 2 letters are right or not
                messagebox.showerror('ID error', 'The ManagerID doesnt start of with the letters "MA", which must be changed and 4 numbers following it')# show error message
            else:
                internalIDFlag2 = True

            if len(emID) != 6: # checks if the length of the ID is 6 characters or not
                messagebox.showerror('ID Error', 'Make sure the length of the ID is 6 with MA at the start and 4 numbers after it')# show error message
            else:
                internalIDFlag5 = True

            numbersMaID = (emID[2:6])# gets the last 4 characters of the entered ID

            if numbersMaID.isnumeric() == False:#Check if the last 4 characters are numbers or not
                messagebox.showerror('ID Error', 'Make sure the length of the ID is 6 with MA at the start and 4 numbers after it')# show error message
            else:
                internalIDFlag6 = True

            if internalIDFlag1 and internalIDFlag2 and internalIDFlag5 and internalIDFlag6 == True:
                idFlag = True

        dayDOB = daysClicked.get()
        monthDOB = monthsClicked.get()
        yearDOB = dobYearEntry.get()
        createAccountDOB = (dayDOB + '/' + monthDOB + '/' + yearDOB)

        if phoneNumber.isdigit(): # checks if the number entered is a digit or not
            internalDigitFlag = True
        else:
            messagebox.showerror('Phone number error', 'Your phone number isnt only numbers')# show error message

        if len(phoneNumber) == 11: #checks the length of the phone number
            internal11Flag = True
        else:
            messagebox.showerror('Phone number error', 'Your phone number isnt 11 numbers long')# show error message

        if phoneNumber[0:2] == "07": #Checks the starting value of the phone number
            internal07Flag = True
        else:
            messagebox.showerror('phone number error', 'Your Phone number doesnt start with "07", make sure it does')# show error message

        if internalDigitFlag and internal11Flag and internal07Flag == True:
            phoneNumberFlag =True

        if "@" in email: # checks if the email contains the '@' symbol
            emailFlag = True
        else:
            messagebox.showerror('Email error', 'The email doesnt contain an "@" symbol like it should, reeneter your email')# show error message

        if len(password)<10: #checks the length of the password
            messagebox.showerror('Password error', 'Your password is less than 10 characters long, make sure it is longer!')# show error message
        else:
            internalPasswordLenFlag = True

        if any(letterU.isupper() for letterU in password): #checks if there is an uppercase letter
            internalPasswordUpperFlag = True
        else:
            messagebox.showerror('Password error', 'Your password doesnt contain an uppercase letter, ensure it does!')# show error message

        if any(letterL.islower() for letterL in password):#checks if there is an lowerecase letter
            internalPasswordLowerFlag = True
        else:
            messagebox.showerror('Password errror', 'Your password doesnt contain a lowercase letter, ensure it does!')# show error message

        if any(num.isdigit() for num in password): #checks if there is a number in the password
            internalPasswordDigitFlag = True
        else:
            messagebox.showerror('Password errror', 'Your password doesnt contain a number, ensure it does!')# show error message

        symbolInPassword = ["!", "@","£","$","%","&","*","(",")",":",";",".","/",","] # create a list of symbols to be used in the password

        if any(symbol in password for symbol in symbolInPassword): #Check if the password has any symbols in it
            internalPasswordSymbolFlag = True
        else:
            messagebox.showerror('Password error', 'Your password does not contain a symbol, make sure there is a symbol!')# show error message

        if internalPasswordLenFlag and internalPasswordUpperFlag and internalPasswordLowerFlag and internalPasswordDigitFlag and internalPasswordSymbolFlag == True:
            passwordList = []
            for i in password:
                newAscii = ord(i) + 2
                newChar = chr(newAscii)
                passwordList.append(newChar)

            print(passwordList)

            newPass = ''.join(passwordList)
            print(newPass)

            #encrypts the password

            passwordFlag = True

        if reenterPassword == password:#Check if the 2 fields have the same value
            reenterPasswordFlag = True
        else:
            messagebox.showerror('Reenter password error', 're enter password does not match the password entered, make sure they match!')# show error message

        if not isManagerCA.get():
            cur.execute("SELECT * FROM tbl_Managers WHERE managerID=?", [whatManager])#check manager table
            maNoID = cur.fetchone() is None

            if maNoID == True:
                messagebox.showerror('ManagerID doesnt Exists', 'ManagerID Doesnt exist, input a valid managerID')# show error message
            else:
                internalIDFlag3 = True

            if whatManager[0:2] != "MA":
                messagebox.showerror('ID error', 'The ManagerID doesnt start of with the letters "MA", which must be changed')# show error message
            else:
                internalIDFlag4 = True

            if internalIDFlag3 and internalIDFlag4 == True:
                whatManagerFlag = True

        else:
            whatManagerFlag = True


        def createUserName(): #defined a function to create a username
            if not isManagerCA.get():
                emUsername = ("E" + firstNameSanitation[0] + lastNameSanitation[0] + emID[2:6]) #create the username
                print(emUsername)
                updateDBCreateAccount(emUsername)#call a function and pass in an argument
            else:
                maUsername = ("M" + firstNameSanitation[0] + lastNameSanitation[0] + emID[2:6])
                print(maUsername)
                updateDBCreateAccount(maUsername)


        def updateDBCreateAccount(username):
            gender = whatGender.get()
            if not isManagerCA.get():
                cur.execute("INSERT INTO tbl_Employees VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",[emID, firstNameSanitation, lastNameSanitation, username, phoneNumber, email, gender, newPass, createAccountDOB, whatManager])
                conn.commit()
                #insert new data in the database
                messagebox.showerror('Account created', 'Account was created successfully, you may now login')
                createAccountToLogin(createAccountPageTop)
                # go to login page
            else:
                cur.execute("INSERT INTO tbl_Managers VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",[emID,firstNameSanitation, lastNameSanitation, username, phoneNumber, email, gender, newPass, createAccountDOB])
                conn.commit()
                messagebox.showerror('Account created', 'Account was created successfully, you may now login')
                createAccountToLogin(createAccountPageTop)


        if (firstNameflag and lastNameflag and idFlag and phoneNumberFlag and emailFlag and passwordFlag and reenterPasswordFlag and whatManagerFlag) == True:
            createUserName() #calls the function to create the username



    bpExpress_label = tk.Label(createAccountPageTop, text="BP Express", bg="WHITE", fg="BLACK")
    bpExpress_label.config(font=('Helvetica bold', 16))
    bpExpress_label.place(anchor="nw")  # anchor to the top left side of the screen

    bplogo_image = Image.open("BP logo.png").resize((28, 24))  # load image and resize
    bplogo_image_login = ImageTk.PhotoImage(bplogo_image)  # use correct library for the use of an image

    bplogo_panel = tk.Label(createAccountPageTop, image=bplogo_image_login)  # create a label where the picture goes
    bplogo_panel.image = bplogo_image_login  # use correct library to properly display image
    bplogo_panel.place(x=1415, y=920)  # place the picture



def showLoginPage(createAccountPageTop):
    createAccountPageTop.withdraw()#Withdraw the createaccountpagetop window
    window.deiconify()#show the window that was withdrawn to be used again.

def attemptLogin(ID, Password):

    if not isManager.get(): #checks if the person logging in is a manager or not
        emID = ID.get() #gets the value of the id entry box
        emPass = Password.get() #Gets the value in the password entry
        cur.execute("SELECT * FROM tbl_Employees WHERE employeeID=?", [emID])
        emNoID = cur.fetchone() is None

        if emNoID == True:
            messagebox.showerror('Login error', 'Your ID and/or Password was incorrect, please re-enter')  # if the password is wrong pop up a message box saying so

        cur.execute("SELECT password "
                    "FROM tbl_Employees "
                    "WHERE employeeID=?", [emID]) #SQL statements to fetch the desired password
        emCorrectPass= cur.fetchone()[0] #stores the password in a variable and extracts it from the tuple

        decryptPassList = []
        for i in emCorrectPass:
            newAscii = ord(i) - 2
            newChar = chr(newAscii)
            decryptPassList.append(newChar)

        emDeEncrpytedPass = ''.join(decryptPassList)
        print(emDeEncrpytedPass)

        #decrypt password in the database

        if emDeEncrpytedPass == emPass:
            loginToMainMenu()#if the password is correct go to new function
        else:
            messagebox.showerror('Login error', 'Your ID and/or Password was incorrect, please re-enter')#if the password is wrong pop up a message box saying so

    else:
        maID = ID.get()#gets the value of the id entry box
        maPass = Password.get()#Gets the value in the password entry
        cur.execute("SELECT * FROM tbl_Managers WHERE managerID=?", [maID])
        maNoID = cur.fetchone() is None

        if maNoID == True:
            messagebox.showerror('Login error', 'Your ID and/or Password was incorrect, please re-enter')  # if the password is wrong pop up a message box saying so

        cur.execute("SELECT password "
                    "FROM tbl_Managers "
                    "WHERE managerID=?", [maID])#SQL statements to fetch the desired password
        maCorrectPass = cur.fetchone()[0]#stores the password in a variable and extracts it from the tuple

        decryptPassList = []
        for i in maCorrectPass:
            newAscii = ord(i) - 2
            newChar = chr(newAscii)
            decryptPassList.append(newChar)

        maDeEncrpytedPass = ''.join(decryptPassList)
        if maDeEncrpytedPass == maPass:
            loginToMainMenu()#if the password is correct go to new function
        else:
            messagebox.showerror('Login error', 'Your ID and/or Password was incorrect, please re-enter')#if the password is wrong pop up a message box saying so

###################################################################################################################################################
#########################################################Event handlers############################################################################
def loginToMainMenu():
    window.withdraw()
    mainMenu()

def createAccountToLogin(createAccountTop):
    createAccountTop.withdraw()
    window.deiconify()

def mainMenuToLogin(mainTop):
    mainTop.withdraw()
    window.deiconify()

def settingsToMenu(settingsTop):
    settingsTop.withdraw()
    mainMenuTop.deiconify()

def menuToSettings():
    mainMenuTop.withdraw()
    settingsPage()

def inventoryToMenu(inventoryTop):
    inventoryTop.withdraw()
    mainMenuTop.deiconify()

def menuToInventory():
    mainMenuTop.withdraw()
    inventory()

def feedbackToMenu(feedbackTop):
    feedbackTop.withdraw()
    mainMenuTop.deiconify()

def menuToFeedback():
    mainMenuTop.withdraw()
    feedBack()

def reportToMenu(reportTop):
    reportTop.withdraw()
    mainMenuTop.deiconify()

def menuToReport():
    mainMenuTop.withdraw()
    report()

def withdrawChangePass(changePasswordTop):
    changePasswordTop.withdraw()
    settingsPage()

def addProdcutToMenu(addProductTop):
    addProductTop.withdraw()
    mainMenuTop.deiconify()

def menuToAddProduct():
    mainMenuTop.withdraw()
    addProduct()

def addSupplierToMenu(supplierTop):
    supplierTop.withdraw()
    mainMenuTop.deiconify()

def menuToAddSupplier():
    mainMenuTop.withdraw()
    addSupplier()

def orderProductToMenu(orderProductTop):
    orderProductTop.withdraw()
    mainMenuTop.deiconify()

def menuToOrderProduct():
    mainMenuTop.withdraw()
    orderProduct()


###################################################################################################################################################

def settingsPage(): # define a function to go to settings

    settingsPageTop = tk.Toplevel(bg="WHITE")#Creates a new top level called settingsPageTop
    settingsPageTop.geometry("1450x1000")  # set new window measurments

    settingsLabel = tk.Label(settingsPageTop, text="Settings", bg="WHITE", fg="BLACK", font=('Helvetica bold', 50))#Create a label at the top of the screen with text Settings
    settingsLabel.pack(side="top")

    emIDSettingsLabel = tk.Label(settingsPageTop, text="EmployeeID: ", bg="WHITE", fg="BLACK", font=('Helvetica bold', 16))
    emIDSettingsLabel.place(x=330, y=100)

    settingsID = idEntry.get() #gets the data from the entry box

    if not isManager.get():# check if the account is a managers account
        cur.execute("SELECT employeeID FROM tbl_Employees WHERE employeeID=?", [settingsID])#check database
        DBIDfetch = cur.fetchone()[0]
        AccountID = tk.StringVar()#put the data in tkinter format
        AccountID.set(DBIDfetch) #insert the data into the tkinter format

        cur.execute("SELECT firstname FROM tbl_Employees WHERE employeeID=?", [settingsID])#check database
        DBFNfetch = cur.fetchone()[0]
        accountFN = tk.StringVar()#put the data in tkinter format
        accountFN.set(DBFNfetch)

        cur.execute("SELECT lastname FROM tbl_Employees WHERE employeeID=?", [settingsID])#check database
        DBLNfetch = cur.fetchone()[0]
        accountLN = tk.StringVar()#put the data in tkinter format
        accountLN.set(DBLNfetch)

        cur.execute("SELECT phoneNumber FROM tbl_Employees WHERE employeeID=?", [settingsID])#check database
        DBPNfetch = cur.fetchone()[0]
        accountPN = tk.StringVar()#put the data in tkinter format
        accountPN.set(DBPNfetch)

        cur.execute("SELECT email FROM tbl_Employees WHERE employeeID=?", [settingsID])#check database
        DBEfetch = cur.fetchone()[0]
        accountE = tk.StringVar()#put the data in tkinter format
        accountE.set(DBEfetch)

        cur.execute("SELECT dateOfBirth FROM tbl_Employees WHERE employeeID=?", [settingsID])#check database
        DBDOBfetch = cur.fetchone()[0]
        dayFetch = DBDOBfetch[0:2]#Splice the DOB
        monthFetch = DBDOBfetch[3:5]#Splice the DOB
        yearFetch = DBDOBfetch[6:10]#Splice the DOB
        accountYear = tk.StringVar()#put the data in tkinter format
        accountYear.set(yearFetch)

    else:
        cur.execute("SELECT managerID FROM tbl_Managers WHERE managerID=?", [settingsID])#check database
        DBIDfetch = cur.fetchone()[0]
        AccountID = tk.StringVar()#put the data in tkinter format
        AccountID.set(DBIDfetch)

        cur.execute("SELECT firstname FROM tbl_Managers WHERE managerID=?", [settingsID])#check database
        DBFNfetch = cur.fetchone()[0]
        accountFN = tk.StringVar()#put the data in tkinter format
        accountFN.set(DBFNfetch)

        cur.execute("SELECT lastname FROM tbl_Managers WHERE managerID=?", [settingsID])#check database
        DBLNfetch = cur.fetchone()[0]
        accountLN = tk.StringVar()#put the data in tkinter format
        accountLN.set(DBLNfetch)

        cur.execute("SELECT phoneNumber FROM tbl_Managers WHERE managerID=?", [settingsID])#check database
        DBPNfetch = cur.fetchone()[0]
        accountPN = tk.StringVar()#put the data in tkinter format
        accountPN.set(DBPNfetch)

        cur.execute("SELECT email FROM tbl_Managers WHERE managerID=?", [settingsID])#check database
        DBEfetch = cur.fetchone()[0]
        accountE = tk.StringVar()#put the data in tkinter format
        accountE.set(DBEfetch)

        cur.execute("SELECT dateOfBirth FROM tbl_Managers WHERE managerID=?", [settingsID])#check database
        DBDOBfetch = cur.fetchone()[0]
        dayFetch = DBDOBfetch[0:2] #Splice the DOB
        monthFetch = DBDOBfetch[3:5]#Splice the DOB
        yearFetch = DBDOBfetch[6:10]#Splice the DOB
        accountYear = tk.StringVar()#put the data in tkinter format
        accountYear.set(yearFetch)

    emIDSettingsEntry = tk.Entry(settingsPageTop, textvariable=AccountID, state="disabled") #create a entry box that is static
    emIDSettingsEntry.configure({"disabledbackground": "ORANGE", "disabledforeground": "WHITE"}) # Change the colour of the entry box and text
    emIDSettingsEntry.place(x=480, y=100)


    if not isManager.get():
        emIDSettingsLabel.config(text="EmployeeID: ", bg="WHITE", fg="BLACK", font=('Helvetica bold', 16))# change text
    else:
        emIDSettingsLabel.config(text="ManagerID: ", bg="WHITE", fg="BLACK", font=('Helvetica bold', 16))

    firstNameSettingsLabel = tk.Label(settingsPageTop, text="First Name: ", bg="WHITE", fg="BLACK", font=('Helvetica bold', 16))# create a label
    firstNameSettingsLabel.place(x=330, y=150)
    firstNameSettingsEntry = tk.Entry(settingsPageTop, textvariable=accountFN, bg="ORANGE", fg="WHITE")# create a entry box and store data
    firstNameSettingsEntry.place(x=480, y=150)

    lastNameSettingsLabel = tk.Label(settingsPageTop, text="Last Name: ", bg="WHITE", fg="BLACK", font=('Helvetica bold', 16))
    lastNameSettingsLabel.place(x=330, y=200)
    lastNameSettingsEntry = tk.Entry(settingsPageTop, textvariable=accountLN, bg="ORANGE", fg="WHITE")# create a entry box and store data
    lastNameSettingsEntry.place(x=480, y=200)

    phoneNumberSettingsLabel = tk.Label(settingsPageTop, text="Phone Number: ", bg="WHITE", fg="BLACK", font=('Helvetica bold', 16))
    phoneNumberSettingsLabel.place(x=330, y=250)
    phoneNumberSettingsEntry = tk.Entry(settingsPageTop, textvariable=accountPN, bg="ORANGE", fg="WHITE")# create a entry box and store data
    phoneNumberSettingsEntry.place(x=480, y=250)

    emailSettingsLabel = tk.Label(settingsPageTop, text="Email: ", bg="WHITE", fg="BLACK", font=('Helvetica bold', 16))
    emailSettingsLabel.place(x=330, y=300)
    emailSettingsEntry = tk.Entry(settingsPageTop, textvariable=accountE, bg="ORANGE", fg="WHITE")# create a entry box and store data
    emailSettingsEntry.place(x=480, y=300)

    dobSettingsLabel = tk.Label(settingsPageTop, text="Date Of Birth: ", bg="WHITE", fg="BLACK", font=('Helvetica bold', 16))  # create a label with text Date Of Birth
    dobSettingsLabel.place(x=830, y=100)

    days = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"]  # Create a list of possible day choices
    daysSettingsClicked = tk.StringVar()  # store the result as a string and in daysClicked
    daysSettingsClicked.set(dayFetch)  # Set the initial value to DD for the day
    daysDrop = tk.OptionMenu(settingsPageTop, daysSettingsClicked, *days)  # create the drop down menu and use the values from the days list and store in daysClicked
    daysDrop.config(bg="ORANGE", fg="WHITE")  # change the colour of the drop down menu
    daysDrop.place(x=770, y=150)

    months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]  # Create a list of possible month choices
    monthsSettingsClicked = tk.StringVar()  # store the result as a string and in monthsClicked
    monthsSettingsClicked.set(monthFetch)  # Set the initial value to MM for the month
    monthsDrop = tk.OptionMenu(settingsPageTop, monthsSettingsClicked, *months)  # create the drop down menu and use the values from the months list and store in monthsClicked
    monthsDrop.config(bg="ORANGE", fg="WHITE")  # change the colour of the drop down menu
    monthsDrop.place(x=850, y=150)

    dobYearSettingsEntry = tk.Entry(settingsPageTop, textvariable=accountYear, bg="ORANGE", fg="WHITE", width=8)  # create an entry box to enter the year since there will be too many values to put in the list
    dobYearSettingsEntry.place(x=935, y=150)

    changePasswordSettingsBtn = tk.Button(settingsPageTop, text="Change Password", bg="ORANGE", fg="BLACK", width=20, height=5, command=lambda: changePassword(settingsPageTop)) # go to different page
    changePasswordSettingsBtn.place(x=792, y=210)

    cancelSettingsBtn = tk.Button(settingsPageTop, text="Cancel", bg="ORANGE", fg="BLACK", width=10, height=3, command=lambda: settingsToMenu(settingsPageTop)) # go to different page
    cancelSettingsBtn.place(x=580, y=380)

    applyChangesSettingsBtn = tk.Button(settingsPageTop, text="Apply Changes", bg="ORANGE", fg="BLACK", width=10, height=3, command=lambda: settingsUpdate()) # update changes
    applyChangesSettingsBtn.place(x=740, y=380)

    def settingsUpdate(): # define a function to validate and update the db
        firstName = firstNameSettingsEntry.get()
        lastName = lastNameSettingsEntry.get()
        phoneNumber = phoneNumberSettingsEntry.get()
        email = emailSettingsEntry.get()
        firstNameflag = False
        lastNameflag = False
        phoneNumberFlag = False
        internalDigitFlag = False
        internal11Flag = False
        internal07Flag = False
        emailFlag = False

        # get entry details and initialise boolean flags

        if firstName.isalpha():
            firstNameSanitation = firstName[0].upper() + firstName[1:]
            firstNameflag = True
        else:
            messagebox.showerror('First name error', 'Your first name isnt only letters, make sure that there are only letters in your first name')

        if lastName.isalpha():
            lastNameSanitation = lastName[0].upper() + lastName[1:]
            lastNameflag = True
        else:
            messagebox.showerror('Last name error', 'Your last name isnt only letters, make sure that there are only letters in your last name')

        dayDOB = daysSettingsClicked.get()
        monthDOB = monthsSettingsClicked.get()
        yearDOB = dobYearSettingsEntry.get()
        newSettingsDOB = (dayDOB + '/' + monthDOB + '/' + yearDOB)

        if phoneNumber.isdigit():
            internalDigitFlag = True
        else:
            messagebox.showerror('Phone number error', 'Your phone number isnt only numbers')

        if len(phoneNumber) == 11:
            internal11Flag = True
        else:
            messagebox.showerror('Phone number error', 'Your phone number isnt 11 numbers long')

        if phoneNumber[0:2] == "07":
            internal07Flag = True
        else:
            messagebox.showerror('phone number error', 'Your Phone number doesnt start with "07", make sure it does')

        if internalDigitFlag and internal11Flag and internal07Flag == True:
            phoneNumberFlag = True

        if "@" in email:
            emailFlag = True
        else:
            messagebox.showerror('Email error', 'The email doesnt contain an "@" symbol like it should, reeneter your email')


        def updateDBSettings(): # define function to update the db
            if not isManager.get():
                cur.execute("UPDATE tbl_Employees SET firstname=?, lastname=?, phoneNumber=?, email=?, dateOfBirth=? WHERE employeeID=?",[firstNameSanitation, lastNameSanitation, phoneNumber, email, newSettingsDOB, settingsID])
                conn.commit()
                messagebox.showerror('Account updated', 'Account has been updated successfully')
            else:
                cur.execute("UPDATE tbl_Managers SET firstname=?, lastname=?, phoneNumber=?, email=?, dateOfBirth=? WHERE managerID=?",[firstNameSanitation, lastNameSanitation, phoneNumber, email, newSettingsDOB, settingsID])
                conn.commit()
                messagebox.showerror('Account updated', 'Account has been updated successfully')

        if (firstNameflag and lastNameflag and phoneNumberFlag and emailFlag) == True:
            updateDBSettings() # call the updatedb function



    bpExpress_label = tk.Label(settingsPageTop, text="BP Express", bg="WHITE", fg="BLACK")
    bpExpress_label.config(font=('Helvetica bold', 16))
    bpExpress_label.place(anchor="nw")  # anchor to the top left side of the screen

    bplogo_image = Image.open("BP logo.png").resize((28, 24))  # load image and resize
    bplogo_image_login = ImageTk.PhotoImage(bplogo_image)  # use correct library for the use of an image

    bplogo_panel = tk.Label(settingsPageTop, image=bplogo_image_login)  # create a label where the picture goes
    bplogo_panel.image = bplogo_image_login  # use correct library to properly display image
    bplogo_panel.place(x=1415, y=920)  # place the picture


def changePassword(settingsPageTop): #Change password function with 1 argument
    settingsPageTop.withdraw() #withdraw the settings page

    changePasswordTop = tk.Toplevel(bg="WHITE") #Create a new window
    changePasswordTop.geometry("1450x1000")#set window size

    changePasswordLabel = tk.Label(changePasswordTop, text="Change Password", bg="WHITE", fg="BLACK", font=('Helvetica bold', 50))
    changePasswordLabel.pack(side="top")

    currentPasswordChangePassLabel = tk.Label(changePasswordTop, text="Current Password: ", bg="WHITE", fg="BLACK", font=('Helvetica bold', 16))
    currentPasswordChangePassLabel.place(x=540, y=100)
    currentPasswordChangePassEntry = tk.Entry(changePasswordTop, bg="ORANGE", fg="WHITE")
    currentPasswordChangePassEntry.place(x=700, y=100)

    newPasswordChangePassLabel = tk.Label(changePasswordTop, text="New Password: ", bg="WHITE", fg="BLACK", font=('Helvetica bold', 16))
    newPasswordChangePassLabel.place(x=540, y=150)
    newPasswordChangePassEntry = tk.Entry(changePasswordTop, bg="ORANGE", fg="WHITE")
    newPasswordChangePassEntry.config(show="*")
    newPasswordChangePassEntry.place(x=700, y=150)

    reEnterPasswordChangePassLabel = tk.Label(changePasswordTop, text="Re-enter Password: ", bg="WHITE", fg="BLACK", font=('Helvetica bold', 16))
    reEnterPasswordChangePassLabel.place(x=540, y=200)
    reEnterPasswordChangePassEntry = tk.Entry(changePasswordTop, bg="ORANGE", fg="WHITE")
    reEnterPasswordChangePassEntry.config(show="*")
    reEnterPasswordChangePassEntry.place(x=700, y=200)

    def eyeIconNewPass():
        eyeIconBtn10 = tk.Button(changePasswordTop, image=eye_image_login, command=lambda: showNewPassChangePass(eyeIconBtn10))  # createa button with that image and pass in parameters via a function
        eyeIconBtn10.place(x=900, y=150)

    eyeIconNewPass()

    def showNewPassChangePass(eyeIconBtn10):
        eyeIconBtn10.place_forget()  # hide the eye icon button
        newPasswordChangePassEntry.config(show="")
        eyeIconBtn11 = tk.Button(changePasswordTop, image=eye_image_login, command=lambda: hideNewPassChangePass(eyeIconBtn11))  # create a new eye icon to hide the password
        eyeIconBtn11.place(x=900, y=150)

    def hideNewPassChangePass(eyeIconBtn11):
        eyeIconBtn11.place_forget()
        newPasswordChangePassEntry.config(show="*")# hides the label that showed the password
        eyeIconNewPass()  # call the function which contains the original eye icon essentially looping everything

    def eyeIconReEnterPass():
        eyeIconBtn12 = tk.Button(changePasswordTop, image=eye_image_login, command=lambda: showReEnterPassChangePass(eyeIconBtn12))
        eyeIconBtn12.place(x=900, y=200)

    eyeIconReEnterPass()

    def showReEnterPassChangePass(eyeIconBtn12):
        eyeIconBtn12.place_forget()  # hide the eye icon button
        reEnterPasswordChangePassEntry.config(show="")
        eyeIconBtn13 = tk.Button(changePasswordTop, image=eye_image_login, command=lambda: hideReEnterPassChangePass(eyeIconBtn13))  # create a new eye icon to hide the password
        eyeIconBtn13.place(x=900, y=200)

    def hideReEnterPassChangePass(eyeIconBtn13):
        eyeIconBtn13.place_forget()
        reEnterPasswordChangePassEntry.config(show="*")
        eyeIconReEnterPass()

    cancelChangePassBtn = tk.Button(changePasswordTop, text="Cancel", bg="ORANGE", fg="BLACK", width=13, height=3, command= lambda: withdrawChangePass(changePasswordTop))#change page
    cancelChangePassBtn.place(x=565, y=250)

    changePasswordChangePassBtn = tk.Button(changePasswordTop, text="Change Password", bg="ORANGE", fg="BLACK", width=13, height=3, command=lambda: getRealPass()) # change the password
    changePasswordChangePassBtn.place(x=745, y=250)

    changePasswordID = idEntry.get() # gets the value entered by the user

    def changePasswordValidation(realCurrentPassword):
        currentPass = currentPasswordChangePassEntry.get()
        newPass = newPasswordChangePassEntry.get()
        reenterPass = reEnterPasswordChangePassEntry.get()

        currentPasswordFlag = False
        newPassFlag = False
        internalPasswordLenFlag = False
        internalPasswordUpperFlag = False
        internalPasswordLowerFlag = False
        internalPasswordSymbolFlag = False
        internalPasswordDigitFlag = False
        reenterPassFlag = False

        # get values from entry boxes and initialise flags

        if currentPass != realCurrentPassword: # check if the password entered by the user is the same one as in the database
            messagebox.showerror('Wrong password', 'The current password you entered is wrong!')
        else:
            currentPasswordFlag = True

        if len(newPass)<10: #check password length
            messagebox.showerror('Password error', 'Your password is less than 10 characters long, make sure it is longer!')
        else:
            internalPasswordLenFlag = True

        if any(letterU.isupper() for letterU in newPass): # check if there is a capital letter
            internalPasswordUpperFlag = True
        else:
            messagebox.showerror('Password error', 'Your password doesnt contain an uppercase letter, ensure it does!')

        if any(letterL.islower() for letterL in newPass): # check if there is a lowercase letter
            internalPasswordLowerFlag = True
        else:
            messagebox.showerror('Password errror', 'Your password doesnt contain a lowercase letter, ensure it does!')

        if any(num.isdigit() for num in newPass): # check if there is a number
            internalPasswordDigitFlag = True
        else:
            messagebox.showerror('Password errror', 'Your password doesnt contain a number, ensure it does!')

        symbolInPassword = ["!", "@","£","$","%","&","*","(",")",":",";",".","/",","] # create a list of symbols

        if any(symbol in newPass for symbol in symbolInPassword): # check if there are any symbols
            internalPasswordSymbolFlag = True
        else:
            messagebox.showerror('Password error', 'Your password does not contain a symbol, make sure there is a symbol!')

        if internalPasswordLenFlag and internalPasswordUpperFlag and internalPasswordLowerFlag and internalPasswordDigitFlag and internalPasswordSymbolFlag == True:
            newPassList = []
            for i in newPass:
                newAscii = ord(i) + 2
                newChar = chr(newAscii)
                newPassList.append(newChar)


            newPassChange = ''.join(newPassList)
            newPassFlag = True

            # encrpyt the password

        if reenterPass == newPass: # check if reenterd password matches the new password
            reenterPassFlag = True
        else:
            messagebox.showerror('Reenter password error', 're enter password does not match the password entered, make sure they match!')

        def updatePassDB(): # define a function to update the database with the enw password
            if not isManager.get():
                cur.execute("UPDATE tbl_Employees SET password=? WHERE employeeID=?", [newPassChange, changePasswordID])
                conn.commit()
                messagebox.showerror('Successful Pass Change', 'Password was changed successfully!')
                #update the database with the new password

            else:
                cur.execute("UPDATE tbl_Managers SET password=? WHERE managerID=?", [newPassChange, changePasswordID])
                conn.commit()
                messagebox.showerror('Successful Pass Change', 'Password was changed successfully!')

        if (currentPasswordFlag and newPassFlag and reenterPassFlag) == True:
            updatePassDB() # call function


    def getRealPass(): # define a fucntion to get the password from the database
        if not isManager.get():
            cur.execute("SELECT password FROM tbl_Employees WHERE employeeID=?",[changePasswordID])
            realCurrentPassword = cur.fetchone()[0]

            decryptPassList = []

            for i in realCurrentPassword:
                newAscii = ord(i) - 2
                newChar = chr(newAscii)
                decryptPassList.append(newChar)

            decrpytedPass = ''.join(decryptPassList)
            changePasswordValidation(decrpytedPass)
            # decrypt the password
        else:
            cur.execute("SELECT password FROM tbl_Managers WHERE managerID=?",[changePasswordID])
            realCurrentPassword = cur.fetchone()[0]
            decryptPassList = []

            for i in realCurrentPassword:
                newAscii = ord(i) - 2
                newChar = chr(newAscii)
                decryptPassList.append(newChar)

            decrpytedPass = ''.join(decryptPassList)
            changePasswordValidation(decrpytedPass)
            # decrypt the password

    bpExpress_label = tk.Label(changePasswordTop, text="BP Express", bg="WHITE", fg="BLACK")
    bpExpress_label.config(font=('Helvetica bold', 16))
    bpExpress_label.place(anchor="nw")  # anchor to the top left side of the screen

    bplogo_image = Image.open("BP logo.png").resize((28, 24))  # load image and resize
    bplogo_image_login = ImageTk.PhotoImage(bplogo_image)  # use correct library for the use of an image

    bplogo_panel = tk.Label(changePasswordTop, image=bplogo_image_login)  # create a label where the picture goes
    bplogo_panel.image = bplogo_image_login  # use correct library to properly display image
    bplogo_panel.place(x=1415, y=920)  # place the picture



def addProduct(): # define function to add a product

    addProductTop = tk.Toplevel(bg="WHITE") # create a new window
    addProductTop.geometry("1450x1000")# resize the window

    addProductLabel = tk.Label(addProductTop, text="Add Product", bg="WHITE", fg="BLACK", font=('Helvetica bold', 50))#create a label
    addProductLabel.pack(side="top")

    productIDAddProductLabel = tk.Label(addProductTop, text="Product ID: ", bg="WHITE", fg="BLACK", font=('Helvetica bold', 16))#create a label
    productIDAddProductLabel.place(x=560, y=100)
    productIDAddProductEntry = tk.Entry(addProductTop, bg="ORANGE", fg="WHITE")# create entry box
    productIDAddProductEntry.place(x=700, y=100)

    productNameAddProductLabel = tk.Label(addProductTop, text="Product Name: ", bg="WHITE", fg="BLACK", font=('Helvetica bold', 16))#create a label
    productNameAddProductLabel.place(x=560, y=150)
    productNameAddProductEntry = tk.Entry(addProductTop, bg="ORANGE", fg="WHITE")# create entry box
    productNameAddProductEntry.place(x=700, y=150)

    productTypeAddProductLabel = tk.Label(addProductTop, text="Product Type: ", bg="WHITE", fg="BLACK", font=('Helvetica bold', 16))#create a label
    productTypeAddProductLabel.place(x=560, y=200)
    productTypeAddProductEntry = tk.Entry(addProductTop, bg="ORANGE", fg="WHITE")# create entry box
    productTypeAddProductEntry.place(x=700, y=200)

    quantityAddProductLabel = tk.Label(addProductTop, text="Quantity: ", bg="WHITE", fg="BLACK", font=('Helvetica bold', 16))#create a label
    quantityAddProductLabel.place(x=560, y=250)
    quantityAddProductEntry = tk.Entry(addProductTop, bg="ORANGE", fg="WHITE")# create entry box
    quantityAddProductEntry.place(x=700, y=250)

    priceAddProductLabel = tk.Label(addProductTop, text="Price: ", bg="WHITE", fg="BLACK", font=('Helvetica bold', 16))#create a label
    priceAddProductLabel.place(x=560, y=300)
    priceAddProductEntry = tk.Entry(addProductTop, bg="ORANGE", fg="WHITE")# create entry box
    priceAddProductEntry.place(x=700, y=300)

    supplierIDAddProductLabel = tk.Label(addProductTop, text="SupplierID: ", bg="WHITE", fg="BLACK", font=('Helvetica bold', 16))#create a label
    supplierIDAddProductLabel.place(x=560, y=350)
    supplierIDAddProductEntry = tk.Entry(addProductTop, bg="ORANGE", fg="WHITE")# create entry box
    supplierIDAddProductEntry.place(x=700, y=350)

    stockLimitAddProductLabel = tk.Label(addProductTop, text="Stock Limit: ", bg="WHITE", fg="BLACK", font=('Helvetica bold', 16))#create a label
    stockLimitAddProductLabel.place(x=560, y=400)
    stockLimitAddProductEntry = tk.Entry(addProductTop, bg="ORANGE", fg="WHITE")# create entry box
    stockLimitAddProductEntry.place(x=700, y=400)

    cancelAddProductButton = tk.Button(addProductTop, text="Cancel", bg="ORANGE", fg="BLACK", width=10, height=3, command=lambda: addProdcutToMenu(addProductTop))#go to main menu
    cancelAddProductButton.place(x=595, y=450)

    addProductAddProductButtton = tk.Button(addProductTop, text="Add Product", bg="ORANGE", fg="BLACK", width=10, height=3, command=lambda: validateAddProduct())# validate data with the press of a button
    addProductAddProductButtton.place(x=745, y=450)

    def validateAddProduct(): # define a function to add the product to the database
        global intStockLimit
        productID = productIDAddProductEntry.get()
        productIDFlag = False
        newProductIDInternalFlag = False
        lenProductIDInternalFlag = False
        PDProductIDInternalFlag = False
        quantity = quantityAddProductEntry.get()
        quantityFlag = False
        price = priceAddProductEntry.get()
        priceFlag = False
        supplierID = supplierIDAddProductEntry.get()
        supplierIDFlag = False
        productName = productNameAddProductEntry.get()
        productType = productTypeAddProductEntry.get()
        stockLimit = stockLimitAddProductEntry.get()
        stockLimitFlag = False

        #get data and initialise boolean flags

        cur.execute("SELECT * FROM tbl_Inventory WHERE productID=?", [productID]) # check inventory table
        pNoID = cur.fetchone() is None

        if pNoID == False: # check if the product id exists or not
            messagebox.showerror('ProductID already exists', 'ProductID already exists, choose a different one')
        else:
            newProductIDInternalFlag = True

        if len(productID) != 6: # check if the length of the ID is 6
            messagebox.showerror('wrong length', 'productID isnt 6 characters long, make sure that it is')
        else:
            lenProductIDInternalFlag = True

        if productID[0:2] != "PD": # check the first 2 letters
            messagebox.showerror('Wrong ID', 'ProductID doesnt start with PD, make sure to change this')
        else:
            PDProductIDInternalFlag = True

        if newProductIDInternalFlag and lenProductIDInternalFlag and PDProductIDInternalFlag == True:
            productIDFlag = True


        try:
            intQuantity = int(quantity) #check if the value entered is an integer or not
            if isinstance(intQuantity, int):
                if intQuantity < 0: # check if the integer is less than 0
                    messagebox.showerror('Quantity error', 'Quantity entered is not positive, ensure it is')
                else:
                    quantityFlag = True

        except ValueError:
            messagebox.showerror('Quantity error', 'Quantity entered is not a whole number, ensure that it is a whole number')






        try:
            floatPrice = float(price) # cast into float
            formatFloatPrice = "{:.2f}".format(floatPrice) # reformat the price to 2.dp
            if price == formatFloatPrice: #check if they are the same
                priceFlag = True
            else:
                messagebox.showerror('Price Error', 'Price entered must be to 2.dp ecluding any currency symbols. Eg. 1.00, thank you!')

        except ValueError:
            messagebox.showerror('Price Error', 'Price entered must be to 2.dp ecluding any currency symbols. Eg. 1.00, thank you!')


        cur.execute("SELECT * FROM tbl_suppliers WHERE supplierID=?", [supplierID]) # check suppliers table
        sNoID = cur.fetchone() is None

        if sNoID == True: #Check if it exists or not
            messagebox.showerror('No SupplierID', 'The supplierId entered doesnt exist, make sure that the supplierID exists')

        else:
            supplierIDFlag = True

        try:
            intStockLimit = int(stockLimit)#check if the value entered is an integer or not
            if isinstance(intStockLimit, int):
                if intStockLimit < 0: # check if the integer is less than 0
                    messagebox.showerror('Quantity error', 'Stock Limit entered is not positive, ensure it is')
                else:
                    stockLimitFlag = True
            else:
                messagebox.showerror('Stock limit error', 'Stock limit entered was not a number, make sure it is a whole number!')

        except ValueError:
            messagebox.showerror('Stock limit error', 'Stock limit entered was not a number, make sure it is a whole number!')

        def insertDBAddProduct():
            cur.execute("INSERT INTO tbl_Inventory VALUES (?, ?, ?, ?, ?, ?, ?)", [productID, productName, productType, quantity, price, supplierID, intStockLimit])
            conn.commit()
            messagebox.showerror('Update Successful', 'The Product Has been added successfully')
            # add data to database

        if quantityFlag and priceFlag and productIDFlag and supplierIDFlag and stockLimitFlag == True:
            insertDBAddProduct() # call the function


    bpExpress_label = tk.Label(addProductTop, text="BP Express", bg="WHITE", fg="BLACK")
    bpExpress_label.config(font=('Helvetica bold', 16))
    bpExpress_label.place(anchor="nw")  # anchor to the top left side of the screen

    bplogo_image = Image.open("BP logo.png").resize((28, 24))  # load image and resize
    bplogo_image_login = ImageTk.PhotoImage(bplogo_image)  # use correct library for the use of an image

    bplogo_panel = tk.Label(addProductTop, image=bplogo_image_login)  # create a label where the picture goes
    bplogo_panel.image = bplogo_image_login  # use correct library to properly display image
    bplogo_panel.place(x=1415, y=920)  # place the picture

def addSupplier(): # define function to add supplier
    addSupplierTop = tk.Toplevel(bg="WHITE") # create new window
    addSupplierTop.geometry("1450x1000")#resize new window

    addSupplierLabel = tk.Label(addSupplierTop, text="Add Supplier", bg="WHITE", fg="BLACK", font=('Helvetica bold', 50))
    addSupplierLabel.pack(side="top")

    supplierIDAddSupplierLabel = tk.Label(addSupplierTop, text="SupplierID: ", bg="WHITE", fg="BLACK", font=('Helvetica bold', 16))
    supplierIDAddSupplierLabel.place(x=560, y=100)
    supplierIDAddSupplierEntry = tk.Entry(addSupplierTop, bg="ORANGE", fg="WHITE")
    supplierIDAddSupplierEntry.place(x=700, y=100)

    supplierNameAddSupplierLabel = tk.Label(addSupplierTop, text="Supplier Name: ", bg="WHITE", fg="BLACK", font=('Helvetica bold', 16))
    supplierNameAddSupplierLabel.place(x=560, y=150)
    supplierNameAddSupplierEntry = tk.Entry(addSupplierTop, bg="ORANGE", fg="WHITE")
    supplierNameAddSupplierEntry.place(x=700, y=150)

    supplierEmailAddSupplierLabel = tk.Label(addSupplierTop, text="Supplier Email: ", bg="WHITE", fg="BLACK", font=('Helvetica bold', 16))
    supplierEmailAddSupplierLabel.place(x=560, y=200)
    supplierEmailAddSupplierEntry = tk.Entry(addSupplierTop, bg="ORANGE", fg="WHITE")
    supplierEmailAddSupplierEntry.place(x=700, y=200)

    supplierNumberAddSupplierLabel = tk.Label(addSupplierTop, text="Supplier Number: ", bg="WHITE", fg="BLACK", font=('Helvetica bold', 16))
    supplierNumberAddSupplierLabel.place(x=560, y=250)
    supplierNumberAddSupplierEntry = tk.Entry(addSupplierTop, bg="ORANGE", fg="WHITE")
    supplierNumberAddSupplierEntry.place(x=700, y=250)

    cancelAddSupplierButton = tk.Button(addSupplierTop, text="Cancel", bg="ORANGE", fg="BLACK", width=10, height=3, command=lambda: addSupplierToMenu(addSupplierTop))
    cancelAddSupplierButton.place(x=595, y=350)

    addProductAddSupplierButtton = tk.Button(addSupplierTop, text="Add Product", bg="ORANGE", fg="BLACK", width=10, height=3, command=lambda: validateAddSupplier())
    addProductAddSupplierButtton.place(x=745, y=350)

    def validateAddSupplier(): # define function to validate the supplier
        supplierID = supplierIDAddSupplierEntry.get()
        supplierIDFlag = False
        newSupplierIDFlag = False
        lenSupplierIDFlag = False
        spSupplierIDFlag = False
        email = supplierEmailAddSupplierEntry.get()
        emailFlag = False
        phoneNumber = supplierNumberAddSupplierEntry.get()
        phoneNumberFlag = False
        supplierName = supplierNameAddSupplierEntry.get()

        #get values and start boolean flags

        cur.execute("SELECT * FROM tbl_suppliers WHERE supplierID=?", [supplierID])
        sNoID = cur.fetchone() is None

        if sNoID == False: #check if ID exists or not
            messagebox.showerror('SupplierID exists', 'The supplierID you entered already exists, make sure to choose a new one!')
        else:
            newSupplierIDFlag = True

        if len(supplierID) != 6: # checks ID length
            messagebox.showerror('SupplierID error',  'Supplier Id that you entered isnt 6 characters long, make sure it is!')
        else:
            lenSupplierIDFlag = True

        if supplierID[0:2] != "SP": #checks first 2 letters
            messagebox.showerror('SupplierID error', 'SupplierID must start with "SP", ensure this has been done!')
        else:
            spSupplierIDFlag = True

        if newSupplierIDFlag and lenSupplierIDFlag and spSupplierIDFlag == True:
            supplierIDFlag = True

        if not "@" in email: #checks for the '@' symbol
            messagebox.showerror('Email error', 'Email that was entered does not contain a "@" symbol which mean it isnt a valid email')
        else:
            emailFlag = True

        if not phoneNumber.isdigit(): #checks if the phone number is a number or not
            messagebox.showerror('Phone number invalid', 'The phone number entered is invalid, make sure that there are no spaces or letters in the phone number!')
        else:
            phoneNumberFlag = True

        def updateDBAddSupplier(): # define a function to update the database table

            cur.execute("INSERT INTO tbl_suppliers VALUES (?, ?, ?, ?)", [supplierID, supplierName, email, phoneNumber])
            conn.commit()
            messagebox.showerror('Added Supplier', 'Added the Supplier successfully!')
            #update database with new info

        if supplierIDFlag and emailFlag and phoneNumberFlag == True:
            updateDBAddSupplier()

    bpExpress_label = tk.Label(addSupplierTop, text="BP Express", bg="WHITE", fg="BLACK")
    bpExpress_label.config(font=('Helvetica bold', 16))
    bpExpress_label.place(anchor="nw")  # anchor to the top left side of the screen

    bplogo_image = Image.open("BP logo.png").resize((28, 24))  # load image and resize
    bplogo_image_login = ImageTk.PhotoImage(bplogo_image)  # use correct library for the use of an image

    bplogo_panel = tk.Label(addSupplierTop, image=bplogo_image_login)  # create a label where the picture goes
    bplogo_panel.image = bplogo_image_login  # use correct library to properly display image
    bplogo_panel.place(x=1415, y=920)  # place the picture

def orderProduct(): #define a function to order a product

    orderProductTop = tk.Toplevel(bg="WHITE") #create new window
    orderProductTop.geometry("1450x1000")#resize new window

    orderProductLabel = tk.Label(orderProductTop, text="Order Product", bg="WHITE", fg="BLACK", font=('Helvetica bold', 50))
    orderProductLabel.pack(side="top")

    productIDOrderProductLabel = tk.Label(orderProductTop, text="ProductID: ", bg="WHITE", fg="BLACK", font=('Helvetica bold', 16))
    productIDOrderProductLabel.place(x=560, y=100)
    productIDOrderProductEntry = tk.Entry(orderProductTop, bg="ORANGE", fg="WHITE")
    productIDOrderProductEntry.place(x=700, y=100)

    stockQuantityOrderProductLabel = tk.Label(orderProductTop, text="Stock Quantity: ", bg="WHITE", fg="BLACK", font=('Helvetica bold', 16))
    stockQuantityOrderProductLabel.place(x=560, y=150)
    stockQuantityOrderProductEntry = tk.Entry(orderProductTop, bg="ORANGE", fg="WHITE")
    stockQuantityOrderProductEntry.place(x=700, y=150)

    showTotalPriceOrderProductBtn = tk.Button(orderProductTop, text="Show Price", bg="ORANGE", fg="BLACK", command=lambda: validateShowPrice(), width=10, height=3)
    showTotalPriceOrderProductBtn.place(x=660, y=300)

    cancelOrderProductBtn = tk.Button(orderProductTop, text="Cancel", bg="ORANGE", fg="BLACK", width=10, height=3, command=lambda: orderProductToMenu(orderProductTop))
    cancelOrderProductBtn.place(x=580, y=400)

    orderProductOrderProductBtn = tk.Button(orderProductTop, text="Order Product", bg="ORANGE", fg="BLACK", width=10, height=3, command=lambda: validateOrderProduct())
    orderProductOrderProductBtn.place(x=740, y=400)

    def validateShowPrice(): #define function to show the price
        productID = productIDOrderProductEntry.get()
        productIDFlag = False
        quantity = stockQuantityOrderProductEntry.get()
        quantityFlag = False

        #get new values in entry box and initialise boolean flags.


        cur.execute("SELECT * FROM tbl_Inventory WHERE productID=?", [productID])
        pNoID = cur.fetchone() is None

        if pNoID == True: # check if ID exists or not
            messagebox.showerror('ProductID error', 'ProductID chosen does not exist, make sure you enter a productID that exists')
        else:
            productIDFlag = True

        try:
            intQuantity = int(quantity) #check if value is an integer
            if isinstance(intQuantity, int):
                if intQuantity < 0: #check if value is less than 0
                    messagebox.showerror('Negative value', 'Value entered is not greater than 0, ensure it is')
                else:
                    quantityFlag = True

        except ValueError:
            messagebox.showerror('Quantity Error', 'Quantity entered is not a whole number, ensure that the number entered is an integer')

        def renderTotalPrice(): #define a function to create a total price
            realQuantity = stockQuantityOrderProductEntry.get() #get the quantity
            intRealQuantity = int(realQuantity) #cast it into an integer
            productChosen = productIDOrderProductEntry.get() #get the productID
            cur.execute("SELECT price FROM tbl_Inventory WHERE productID=?", [productChosen])#Check db for price
            productPrice = cur.fetchone()[0]#extract from tuple
            floatProductPrice = float(productPrice) #cast into a float
            finalPriceTemp = (floatProductPrice*intRealQuantity) #multiply them together
            finalPrice = ('{:.2f}'.format(finalPriceTemp))#reformat to 2.dp
            totalPriceOnLabel(finalPrice) #call a function and apss it in

        if productIDFlag and quantityFlag == True:
            renderTotalPrice()

    totalPriceOrderProductLabel = tk.Label(orderProductTop, text="Total Cost: £", bg="WHITE", fg="BLACK", font=('Helvetica bold', 16))
    totalPriceOrderProductLabel.place(x=630, y=250)

    priceTextLabel = tk.Label(orderProductTop, text=" ", bg="WHITE", fg="BLACK", font=('Helvetica bold', 16))
    priceTextLabel.place(x=725, y=250)

    def totalPriceOnLabel(finalPrice): #define function to show the price
        priceTextLabel.config(text=finalPrice) # change the price label with new price

    def validateOrderProduct(): #define function to validate the order
        productID = productIDOrderProductEntry.get()
        productIDFlag = False
        quantity = stockQuantityOrderProductEntry.get()
        quantityFlag = False
        managerID = idEntry.get()

        cur.execute("SELECT * FROM tbl_Inventory WHERE productID=?", [productID])
        pNoID = cur.fetchone() is None

        if pNoID == True:
            messagebox.showerror('ProductID error', 'ProductID chosen does not exist, make sure you enter a productID that exists')
        else:
            productIDFlag = True

        try:
            intQuantity = int(quantity) # check if it is an integer
            if isinstance(intQuantity, int):
                quantityFlag = True

        except ValueError:
            messagebox.showerror('Quantity Error', 'Quantity entered is not a whole number, ensure that the number entered is an integer')


        cur.execute("SELECT orderID FROM tbl_Orders ORDER BY orderID DESC LIMIT 1") #get the last records orderID
        latestOrderID = cur.fetchone()[0]

        def newOrderID(): #define function to create a new orderID

            numbersLatestOrderID = latestOrderID[2:6]# get the numbers of the last orderID
            intNumbersLatestOrderID = int(numbersLatestOrderID)#cast it into an integer
            newNumbersOrderID = intNumbersLatestOrderID + 1 # add 1 to the numbers
            newOrderIDNumberFinal = str(newNumbersOrderID).zfill(4)#pad with 0's where it can and cast
            newOrderID = "OR" + newOrderIDNumberFinal #add OR back at the front
            updateDBOrderProduct(newOrderID) #call function and pass in as an argument

        def updateDBOrderProduct(newOrderID): #define a fucntion to update the databse with new order

            cur.execute("INSERT INTO tbl_Orders VALUES(?,?,?,?)", [newOrderID, intQuantity, productID, managerID])
            conn.commit()
            #updaet the db
            updateOriginalQuantity(newOrderID)#call function with an argument

        def updateOriginalQuantity(newOrderID): #define function to update the original quantity

            cur.execute("SELECT quantity FROM tbl_Inventory WHERE productID=?", [productID])# get quantity from db
            oQuantity = cur.fetchone()[0]
            newInventoryQuantity = oQuantity + intQuantity #calcuations to add quantity into the orignal quantity
            cur.execute("UPDATE tbl_Inventory SET quantity=? WHERE productID=?", [newInventoryQuantity, productID])
            conn.commit()
            messagebox.showerror('Update Successfull', f'Your order has been successful! Your orderID is {newOrderID}')
            #update db and show a message with orderID

        if productIDFlag and quantityFlag == True:
            newOrderID()







    bpExpress_label = tk.Label(orderProductTop, text="BP Express", bg="WHITE", fg="BLACK")
    bpExpress_label.config(font=('Helvetica bold', 16))
    bpExpress_label.place(anchor="nw")  # anchor to the top left side of the screen

    bplogo_image = Image.open("BP logo.png").resize((28, 24))  # load image and resize
    bplogo_image_login = ImageTk.PhotoImage(bplogo_image)  # use correct library for the use of an image

    bplogo_panel = tk.Label(orderProductTop, image=bplogo_image_login)  # create a label where the picture goes
    bplogo_panel.image = bplogo_image_login  # use correct library to properly display image
    bplogo_panel.place(x=1415, y=920)  # place the picture

def inventory(): #define function to creat inventory page

    inventoryTop = tk.Toplevel(bg="WHITE") #create new window
    inventoryTop.geometry("1450x1000")

    inventoryLabel = tk.Label(inventoryTop, text="Inventory", bg="WHITE", fg="BLACK", font=('Helvetica bold', 50))
    inventoryLabel.pack(side="top")


    styleTable = ttk.Style() #access all the table styles

    styleTable.theme_use("default") # use the default theme

    styleTable.configure("Treeview",
                    background = "ORANGE",
                    foreground = "BLACK",
                    rowheight = 20,
                    fieldbackground = "WHITE"
                    ) #create configurations fot eh style of the table

    styleTable.map("Treeview",
                   background = [('selected', 'BLUE')]) # when clicked on a rown colour is bluw


    inventoryTable = ttk.Treeview(inventoryTop, height=30)#Create a table for wheere all the information will go
    inventoryTable['columns'] = ("ProductID", "Product Name", "Product Type", "Quantity", "Price", "SupplierID", "Stock Limit")#Specify columns and and names NOT HEADINGS!

    inventoryTable.column("#0", width=0, stretch=False)#hides the extra column making it 'invisible'
    inventoryTable.column("ProductID", width=200, minwidth=25)# create the column properly with correct sizes
    inventoryTable.column("Product Name", width=200, minwidth=25)# create the column properly with correct sizes
    inventoryTable.column("Product Type", width=200, minwidth=25)# create the column properly with correct sizes
    inventoryTable.column("Quantity", width=200, minwidth=25)# create the column properly with correct sizes
    inventoryTable.column("Price", width=200, minwidth=25)# create the column properly with correct sizes
    inventoryTable.column("SupplierID", width=200, minwidth=25)# create the column properly with correct sizes
    inventoryTable.column("Stock Limit", width=200, minwidth=25)

    inventoryTable.heading("ProductID", text="ProductID")#Set headings to the columns
    inventoryTable.heading("Product Name", text="Product Name")#Set headings to the columns
    inventoryTable.heading("Product Type", text="Product Type")#Set headings to the columns
    inventoryTable.heading("Quantity", text="Quantity")#Set headings to the columns
    inventoryTable.heading("Price", text="Price")#Set headings to the columns
    inventoryTable.heading("SupplierID", text="SupplierID")#Set headings to the columns
    inventoryTable.heading("Stock Limit", text="Stock Limit")

    scrollbar = ttk.Scrollbar(inventoryTop, orient=tk.VERTICAL, command=inventoryTable.yview) #create a scroll bar and make it vertical with a command
    scrollbar.place(relx=0.983, rely=0.085, relwidth=0.01, relheight=0.655) # place the scroll bare
    inventoryTable.configure(yscrollcommand=scrollbar.set) # assign scroll bar to the correct table

    inventoryTable.pack(pady=20)



    inventoryTable.tag_configure('oddrow', background="ORANGE")#create row color
    inventoryTable.tag_configure('evenrow', background="WHITE")#create row colour

    cur.execute("SELECT * FROM tbl_Inventory") # get every data from database table
    recordData = cur.fetchall()

    for i, recordData in enumerate(recordData): #change the colours and insert the data into the rowns
        if i % 2==0: #check if even row
            tags = ('evenrow',) #shows an orange colour
        else:
            tags = ('oddrow',) #shows a white colour

        inventoryTable.insert(parent='', index='end', text=f"Row {i}", values=recordData, tags=tags) #insert the data from the database into the table

    def updateInventoryTable(): #define the function to update the table
        inventoryTable.delete(*inventoryTable.get_children())#delete and clear all thed ata within the table
        inventoryTable.tag_configure('oddrow', background="ORANGE")# keep the colour consistent
        inventoryTable.tag_configure('evenrow', background="WHITE")

        cur.execute("SELECT * FROM tbl_Inventory")# check database with new info
        recordData = cur.fetchall()

        for i, recordData in enumerate(recordData): #display the rows and insert data in thetable
            if i % 2 == 0:
                tags = ('evenrow',)
            else:
                tags = ('oddrow',)

            inventoryTable.insert(parent='', index='end', text=f"Row {i}", values=recordData, tags=tags) #insert data into table

    productIDInventoryLabel = tk.Label(inventoryTop, text="ProductID: ", bg="WHITE", fg="BLACK", font=('Helvetica bold', 16))
    productIDInventoryLabel.place(x=200, y=770)
    productIDInventoryEntry = tk.Entry(inventoryTop, bg="ORANGE", fg="WHITE")
    productIDInventoryEntry.place(x=290, y=770)

    quantityInventoryLabel = tk.Label(inventoryTop, text="Quantity: ", bg="WHITE", fg="BLACK", font=('Helvetica bold', 16))
    quantityInventoryLabel.place(x=580, y=770)
    quantityInventoryEntry = tk.Entry(inventoryTop, bg="ORANGE", fg="WHITE")
    quantityInventoryEntry.place(x=670, y=770)

    reduceStockOrLimitLabel = tk.Label(inventoryTop, text="Restock: ", bg="WHITE", fg="BLACK", font=('Helvetica bold', 16))
    reduceStockOrLimitLabel.place(x=960, y=770)
    reduceStockOrLimitEntry = tk.Entry(inventoryTop, bg="ORANGE", fg="WHITE")
    reduceStockOrLimitEntry.place(x=1070, y=770)

    if not isManager.get(): # check if manager
        reduceStockOrLimitLabel.config(text="Restock: ", font=('Helvetica bold', 16))#show text if employee
    else:
        reduceStockOrLimitLabel.config(text= "Stock Limit: ", font=('Helvetica bold', 16)) #show text if manager

    def checkStockLimitReach(): #define a function to check if limit has been reached
        cur.execute("SELECT productID, quantity, stockLimit FROM tbl_Inventory")
        compareValueInRecords = cur.fetchall()

        for record in compareValueInRecords:#check tuple from database fetched data
            if record[1] < record[2]: # compare the quantity with stock limit
                messagebox.showerror('Level reached', f'Your stock limit for {record[0]} has been reached, make sure to restock!')#message to say which item is low on stock

    def validateRestock():
        global intQuantity
        global intRestockOrLimit
        global intQuantity2
        global intRestockOrLimit2

        productID = productIDInventoryEntry.get()
        productIDFlag = False
        quantity = quantityInventoryEntry.get()
        quantityFlag = False
        restockOrLimit = reduceStockOrLimitEntry.get()
        restockOrLimitFlag = False

        #initialse boolean flags



        cur.execute("SELECT productID FROM tbl_Inventory WHERE productID=?", [productID])
        pNoID = cur.fetchone() is None

        if pNoID == True: #check if productID exists
            messagebox.showerror('ProductID Error', 'No productID exists with the one you entered, ensure the productID exists')
        else:
            productIDFlag = True


        if restockOrLimit == "" and not quantity == "": #checks if fields are empty or not
            try:
                intQuantity = int(quantity) #checks if the value is an integer
                if isinstance(intQuantity, int):
                    if intQuantity >= 0: #checks if value is less than 0
                        quantityFlag = True
                    else:
                        messagebox.showerror('Quantity Error', 'Make sure the Quantity is greater than 0')
                else:
                    messagebox.showerror('Quantity Error', 'Ensure that the quantity entered is a number')

            except ValueError:
                messagebox.showerror('Quantity Error', 'Ensure that the quantity entered is a number')
                #show error message

            if quantityFlag and productIDFlag == True:
                cur.execute("UPDATE tbl_Inventory SET quantity=? WHERE productID=?", [intQuantity, productID])
                conn.commit()
                # update db
                messagebox.showerror('Success', 'Changes were successful!')
                updateInventoryTable() # call function to update db

        if quantity == "" and not restockOrLimit == "":#checks if fields are empty or not
            def showInventoryError():
                if not isManager.get():
                    messagebox.showerror('Restock Error', 'Make sure the value in the restock entry box is a number bigger than 0')
                else:
                    messagebox.showerror('Limit error', 'Ensure the value in the limit entry box is a number greater than 0')

            try:
                intRestockOrLimit = int(restockOrLimit)
                if isinstance(intRestockOrLimit, int):#checks if the value is an integer
                    if intRestockOrLimit >= 0:#checks if value is less than 0
                        restockOrLimitFlag = True
                    else:
                        showInventoryError()
                else:
                    showInventoryError()

            except ValueError:
                showInventoryError()

            if restockOrLimitFlag and productIDFlag == True:#checks if fields are empty or not
                if not isManager.get():
                    cur.execute("SELECT quantity FROM tbl_Inventory WHERE productID=?",[productID])
                    dbQuantity = cur.fetchone()[0]
                    intdbQuantity = int(dbQuantity)#checks if the value is an integer
                    newQuantity = int(intdbQuantity - intRestockOrLimit)# takes 2 values away
                    if newQuantity < 0:#checks if value is less than 0
                        messagebox.showerror('Quantity error', 'After restocking you have negative stock, this isnt possible')
                    else:
                        cur.execute("UPDATE tbl_Inventory SET quantity=? WHERE productID=?", [newQuantity, productID])
                        conn.commit()
                        #update db
                        messagebox.showerror('Success', 'Changes were successful!')
                        updateInventoryTable()
                else:
                    cur.execute("UPDATE tbl_Inventory SET stockLimit=? WHERE productID=?", [intRestockOrLimit, productID])
                    conn.commit()
                    #update db
                    messagebox.showerror('Success', 'Changes were successful!')
                    updateInventoryTable()

        if quantity == "" and restockOrLimit == "":#checks if fields are empty or not
            messagebox.showerror('Field error', 'Both fields were empty, make sure you are changing something')


        def showInventoryError1(): #define function to show the error
            if not isManager.get():
                messagebox.showerror('Restock Error', 'Make sure the value in the restock entry box is a number bigger than 0')
            else:
                messagebox.showerror('Limit error', 'Ensure the value in the limit entry box is a number greater than 0')

        if not quantity == "" and  not restockOrLimit == "":
            if not isManager.get():
                messagebox.showerror('Field error', 'Both Quantity and restock fields cant be filled in. Only choose 1!')
            else:
                try:
                    intQuantity2 = int(quantity)
                    if isinstance(intQuantity2, int):
                        if intQuantity2 >= 0:
                            quantityFlag = True
                        else:
                            messagebox.showerror('Quantity Error', 'Make sure the Quantity is greater than 0')
                    else:
                        messagebox.showerror('Quantity Error', 'Ensure that the quantity entered is a number')

                except ValueError:
                    messagebox.showerror('Quantity Error', 'Ensure that the quantity entered is a number')

                try:
                    intRestockOrLimit2 = int(restockOrLimit)
                    if isinstance(intRestockOrLimit2, int):
                        if intRestockOrLimit2 >= 0:
                            restockOrLimitFlag = True
                        else:
                            showInventoryError1()
                    else:
                        showInventoryError1()

                except ValueError:
                    showInventoryError1()

                if quantityFlag and restockOrLimitFlag and productIDFlag:
                    cur.execute("UPDATE tbl_Inventory SET quantity=?, stockLimit=? WHERE productID=?", [intQuantity2, intRestockOrLimit2, productID])
                    conn.commit()
                    messagebox.showerror('Success', 'Changes were successful!')
                    updateInventoryTable()





    cancelInventoryBtn = tk.Button(inventoryTop, text="Cancel", bg="ORANGE", fg="BLACK", height=3, width=10, command=lambda: inventoryToMenu(inventoryTop))
    cancelInventoryBtn.place(x=495, y=850)

    applyChangesInventoryBtn = tk.Button(inventoryTop, text="Apply Changes", bg="ORANGE", fg="BLACK", height=3, width=10, command=lambda: validateRestock())
    applyChangesInventoryBtn.place(x=645, y=850)

    checkStockLimitReachButton = tk.Button(inventoryTop, text="Check stock\n limit reach", bg="ORANGE", fg="BLACK", height=3, width=10, command=lambda: checkStockLimitReach())
    checkStockLimitReachButton.place(x=795, y=850)

    bpExpress_label = tk.Label(inventoryTop, text="BP Express", bg="WHITE", fg="BLACK")
    bpExpress_label.config(font=('Helvetica bold', 16))
    bpExpress_label.place(anchor="nw")  # anchor to the top left side of the screen

    bplogo_image = Image.open("BP logo.png").resize((28, 24))  # load image and resize
    bplogo_image_login = ImageTk.PhotoImage(bplogo_image)  # use correct library for the use of an image

    bplogo_panel = tk.Label(inventoryTop, image=bplogo_image_login)  # create a label where the picture goes
    bplogo_panel.image = bplogo_image_login  # use correct library to properly display image
    bplogo_panel.place(x=1415, y=920)  # place the picture

def report(): # define function to create report

    reportTop = tk.Toplevel(bg="WHITE") #create new window
    reportTop.geometry("1450x1000")

    reportLabel = tk.Label(reportTop, text="Report", bg="WHITE", fg="BLACK", font=('Helvetica bold', 50))
    reportLabel.pack(side="top")

    reportChoiceLabel = tk.Label(reportTop, text="What Data do you want to see?", bg="WHITE", fg="BLACK", font=('helvetica bold', 16))
    reportChoiceLabel.pack(pady=60)

    reportChartTypeLabel = tk.Label(reportTop, text="What sort of chart do you want?", bg="WHITE", fg="BLACK", font=('Helvetica bold', 16))
    reportChartTypeLabel.pack(pady=40)

    chartSavedNameLabel = tk.Label(reportTop, text="What do you want to store the name of the file?", bg="WHITE", fg="BLACK", font=('helvetica bold', 16))
    chartSavedNameLabel.pack(pady=40)
    chartSavedNameEntry = tk.Entry(reportTop, bg="ORANGE", fg="WHITE", font=('helvetica bold', 16))
    chartSavedNameEntry.place(x=630, y=390)


    emailReportLabel = tk.Label(reportTop, text="Email", bg="WHITE", fg="BLACK", font=('Helvetica bold', 16))
    emailReportLabel.pack(pady=40)
    emailReportEntry = tk.Entry(reportTop, bg="ORANGE", fg="WHITE")
    emailReportEntry.place(x=630, y=500)

    cancelReportBtn = tk.Button(reportTop, text="Cancel", bg="ORANGE", fg="BLACK", width=10, height=3, command=lambda: reportToMenu(reportTop))
    cancelReportBtn.place(x=590, y=550)

    emailReportBtn = tk.Button(reportTop, text="Email", bg="ORANGE", fg="BLACK", width=10, height=3, command=lambda: validateChoices())
    emailReportBtn.place(x=740, y=550)

    reportChoice = tk.BooleanVar(reportTop)
    tk.Radiobutton(reportTop, text="Product", variable=reportChoice, value=True, bg="ORANGE", fg="WHITE", width=10).place(x=610, y=170)
    tk.Radiobutton(reportTop, text="Suppliers", variable=reportChoice, value=False, bg="ORANGE", fg="WHITE", width=10).place(x=740, y=170)

    chartChoice = tk.BooleanVar(reportTop)
    tk.Radiobutton(reportTop, text="Pie Chart", variable=chartChoice, value=True, bg="ORANGE", fg="WHITE", width=10).place( x=610, y=290)
    tk.Radiobutton(reportTop, text="Bar Chart", variable=chartChoice, value=False, bg="ORANGE", fg="WHITE", width=10).place(x=740, y=290)

    choicesLabel1 = tk.Label(reportTop, text="Enter First 5 choices", bg="WHITE", fg="BLACK", font=('helvetica bold', 16))
    choicesLabel1.place(x=200, y=100)
    choicesLabel2 = tk.Label(reportTop, text="Enter the last 5 choices", bg="WHITE", fg="BLACK", font=('helvetica bold', 16))
    choicesLabel2.place(x=1050, y=100)


    idChoice1 = tk.Entry(reportTop, bg="ORANGE", fg="WHITE")
    idChoice1.place(x=190, y=140)
    idChoice2 = tk.Entry(reportTop, bg="ORANGE", fg="WHITE")
    idChoice2.place(x=190, y=180)
    idChoice3 = tk.Entry(reportTop, bg="ORANGE", fg="WHITE")
    idChoice3.place(x=190, y=220)
    idChoice4 = tk.Entry(reportTop, bg="ORANGE", fg="WHITE")
    idChoice4.place(x=190, y=260)
    idChoice5 = tk.Entry(reportTop, bg="ORANGE", fg="WHITE")
    idChoice5.place(x=190, y=300)
    idChoice6 = tk.Entry(reportTop, bg="ORANGE", fg="WHITE")
    idChoice6.place(x=1040, y=140)
    idChoice7 = tk.Entry(reportTop, bg="ORANGE", fg="WHITE")
    idChoice7.place(x=1040, y=180)
    idChoice8 = tk.Entry(reportTop, bg="ORANGE", fg="WHITE")
    idChoice8.place(x=1040, y=220)
    idChoice9 = tk.Entry(reportTop, bg="ORANGE", fg="WHITE")
    idChoice9.place(x=1040, y=260)
    idChoice10 = tk.Entry(reportTop, bg="ORANGE", fg="WHITE")
    idChoice10.place(x=1040, y=300)


    def validateChoices(): # define function to validate the choices
        idChoice1Get = idChoice1.get()
        idChoice2Get = idChoice2.get()
        idChoice3Get = idChoice3.get()
        idChoice4Get = idChoice4.get()
        idChoice5Get = idChoice5.get()
        idChoice6Get = idChoice6.get()
        idChoice7Get = idChoice7.get()
        idChoice8Get = idChoice8.get()
        idChoice9Get = idChoice9.get()
        idChoice10Get = idChoice10.get()

        if reportChoice.get():
            cur.execute("SELECT * FROM tbl_Inventory WHERE productID=?",[idChoice1Get]) #Check if ID exists in db or not
            idChoice1Check = not(cur.fetchone() is None)
            cur.execute("SELECT * FROM tbl_Inventory WHERE productID=?", [idChoice2Get])
            idChoice2Check = not(cur.fetchone() is None)
            cur.execute("SELECT * FROM tbl_Inventory WHERE productID=?",[idChoice3Get])
            idChoice3Check = not(cur.fetchone() is None)
            cur.execute("SELECT * FROM tbl_Inventory WHERE productID=?", [idChoice4Get])
            idChoice4Check = not(cur.fetchone() is None)
            cur.execute("SELECT * FROM tbl_Inventory WHERE productID=?",[idChoice5Get])
            idChoice5Check = not(cur.fetchone() is None)
            cur.execute("SELECT * FROM tbl_Inventory WHERE productID=?", [idChoice6Get])
            idChoice6Check = not(cur.fetchone() is None)
            cur.execute("SELECT * FROM tbl_Inventory WHERE productID=?",[idChoice7Get])
            idChoice7Check = not(cur.fetchone() is None)
            cur.execute("SELECT * FROM tbl_Inventory WHERE productID=?", [idChoice8Get])
            idChoice8Check = not (cur.fetchone() is None)
            cur.execute("SELECT * FROM tbl_Inventory WHERE productID=?", [idChoice9Get])
            idChoice9Check = not (cur.fetchone() is None)
            cur.execute("SELECT * FROM tbl_Inventory WHERE productID=?", [idChoice10Get])
            idChoice10Check = not (cur.fetchone() is None)


            if (idChoice1Check and idChoice2Check and idChoice3Check and idChoice4Check and idChoice5Check and idChoice6Check and idChoice7Check and idChoice8Check and idChoice9Check and idChoice10Check) == True:
                reportFunctionality(idChoice1Get,idChoice2Get,idChoice3Get,idChoice4Get,idChoice5Get,idChoice6Get,idChoice7Get, idChoice8Get, idChoice9Get, idChoice10Get)
            else:
                tk.messagebox.showerror('Invalid ID', 'An Id you entered is invalid and does not exist. Please make sure it exists')

        else:
            cur.execute("SELECT * FROM tbl_suppliers WHERE supplierID=?", [idChoice1Get])
            idChoice1Check = not(cur.fetchone() is None)
            cur.execute("SELECT * FROM tbl_suppliers WHERE supplierID=?", [idChoice2Get])
            idChoice2Check = not(cur.fetchone() is None)
            cur.execute("SELECT * FROM tbl_suppliers WHERE supplierID=?", [idChoice3Get])
            idChoice3Check = not(cur.fetchone() is None)
            cur.execute("SELECT * FROM tbl_suppliers WHERE supplierID=?", [idChoice4Get])
            idChoice4Check = not(cur.fetchone() is None)
            cur.execute("SELECT * FROM tbl_suppliers WHERE supplierID=?", [idChoice5Get])
            idChoice5Check = not(cur.fetchone() is None)
            cur.execute("SELECT * FROM tbl_suppliers WHERE supplierID=?", [idChoice6Get])
            idChoice6Check = not(cur.fetchone() is None)
            cur.execute("SELECT * FROM tbl_suppliers WHERE supplierID=?", [idChoice7Get])
            idChoice7Check = not(cur.fetchone() is None)
            cur.execute("SELECT * FROM tbl_suppliers WHERE supplierID=?", [idChoice8Get])
            idChoice8Check = not (cur.fetchone() is None)
            cur.execute("SELECT * FROM tbl_suppliers WHERE supplierID=?", [idChoice9Get])
            idChoice9Check = not (cur.fetchone() is None)
            cur.execute("SELECT * FROM tbl_suppliers WHERE supplierID=?", [idChoice10Get])
            idChoice10Check = not (cur.fetchone() is None)


            if (idChoice1Check and idChoice2Check and idChoice3Check and idChoice4Check and idChoice5Check and idChoice6Check and idChoice7Check and idChoice8Check and idChoice9Check and idChoice10Check) == True:
                reportFunctionality(idChoice1Get,idChoice2Get,idChoice3Get,idChoice4Get,idChoice5Get,idChoice6Get,idChoice7Get, idChoice8Get, idChoice9Get, idChoice10Get)
            else:
                tk.messagebox.showerror('Invalid ID','An Id you entered is invalid and does not exist. Please make sure it exists')



    def reportFunctionality(PS1,PS2,PS3,PS4,PS5,PS6,PS7,PS8,PS9,PS10): #function to get data from the database
        email = emailReportEntry.get()


        if "@" in email: #check if there is an '@' sybol in the email
            if reportChoice.get():
                cur.execute("SELECT productID, SUM(orderQuantity) as total_quantity "
                            "FROM tbl_Orders "
                            "WHERE productID IN (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                            "GROUP BY productID",[PS1,PS2,PS3,PS4,PS5,PS6,PS7,PS8,PS9,PS10])
                products = cur.fetchall()
                #check database for info about ID's entered
                print(products)
                product_totals = {} # create an empty dictionary
                for product in products: #use for loop to loop through data
                    product_totals[product[0]] = product[1] #add data to dictionary

                productNames = list(product_totals.keys()) #create a list of keys
                productValues = list(product_totals.values()) #create a list of values

                print(product_totals)


                if chartChoice.get():
                    plt.title('Report')
                    plt.pie(productValues, labels=productNames, autopct='%1.1f%%') #create a pie chart with percentages

                    fileName = chartSavedNameEntry.get()
                    plt.savefig(f'/Users/aqibmiah/Downloads/{fileName}') #store png file in downloads
                    plt.close() #close plt file
                    sendEmail() #call function to send the email



                else:
                    plt.title('Report') #create a title for the png
                    plt.xlabel('ProductID') #set a x axis name
                    plt.ylabel('Total Order Quantity') #set a y axis name
                    axis = plt.gca() # get all values seperatly on x axis
                    axis.xaxis.set_tick_params(labelsize=6) #change the sizes of those names on the x axis

                    plt.bar(range(len(product_totals)), productValues, tick_label=productNames) # create the bar chart

                    fileName = chartSavedNameEntry.get()
                    plt.savefig(f'/Users/aqibmiah/Downloads/{fileName}') #save chart to downloads with file name
                    plt.close()
                    sendEmail()


            else:
                cur.execute("""SELECT s.supplierID, SUM(o.orderQuantity) as total_supplier_quantity
                FROM tbl_Orders o
                JOIN tbl_Inventory i ON o.productID = i.productID
                JOIN tbl_suppliers s ON i.supplierID = s.supplierID
                WHERE s.supplierID IN (?, ?, ?, ?, ?, ?, ?, ?, ? ,?)
                GROUP BY s.supplierID""", [PS1,PS2,PS3,PS4,PS5,PS6,PS7,PS8,PS9,PS10]) # use sql to join tables together to then use that data

                sR = cur.fetchall()

                supplier_totals = {}
                for supplier in sR:
                    supplier_totals[supplier[0]] = supplier[1]

                supplierNames = list(supplier_totals.keys())
                supplierValues = list(supplier_totals.values())

                print(supplier_totals)

                if chartChoice.get():
                    plt.title('Report')
                    plt.pie(supplierValues, labels=supplierNames, autopct='%1.1f%%')

                    fileName = chartSavedNameEntry.get()
                    plt.savefig(f'/Users/aqibmiah/Downloads/{fileName}')
                    plt.close()
                    sendEmail()


                else:
                    plt.title('Report')
                    plt.xlabel('SupplierID')
                    plt.ylabel('Total Order Quantity')
                    ax = plt.gca()
                    ax.xaxis.set_tick_params(labelsize=6)

                    plt.bar(range(len(supplier_totals)), supplierValues, tick_label=supplierNames)

                    fileName = chartSavedNameEntry.get()
                    plt.savefig(f'/Users/aqibmiah/Downloads/{fileName}')
                    plt.close()
                    sendEmail()
        else:
            tk.messagebox.showerror('invalid email', 'Email entered is invalid please check again')

    def sendEmail(): # define a function to send the email
        emailMessage = MIMEMultipart() # create multiple parts of the email under a variable name

        emailMessage['From'] = 'aqibmiah2005@gmail.com' # set a from source
        emailMessage['To'] = emailReportEntry.get() # set a to source
        emailMessage['Subject'] = "Report" # create a subject for the email
        message = MIMEText('In this email data is attached about bpexpress!') # add a message to the email

        emailMessage.attach(message) # attach the message to the email

        fileName = chartSavedNameEntry.get() + ".png" # get the file name
        pngName = f'/Users/aqibmiah/Downloads/{fileName}'# allocate the file
        with open(pngName, 'rb') as reportChart:# open the file
            pngData = reportChart.read() # read the png

        imageAttached = MIMEImage(pngData, name=os.path.basename(pngName))# convert to MIME form
        emailMessage.attach(imageAttached)# attach the png to the emiail

        sender = 'aqibmiah2005@gmail.com' # set a smtplib sender
        receiver = emailReportEntry.get() # set a smptlib reciever


        emailSend = smtplib.SMTP('smtp.gmail.com', 587) #connect to smtp server with correct port
        emailSend.starttls() #establish secure connection
        emailSend.login('aqibmiah2005@gmail.com', 'smtp password required') #login to smpt server
        emailSend.sendmail(sender, receiver, emailMessage.as_string()) # send the email
        emailSend.quit()#quit
        tk.messagebox.showerror('email sent', 'Email was sent!')



    bpExpress_label = tk.Label(reportTop, text="BP Express", bg="WHITE", fg="BLACK")
    bpExpress_label.config(font=('Helvetica bold', 16))
    bpExpress_label.place(anchor="nw")  # anchor to the top left side of the screen

    bplogo_image = Image.open("BP logo.png").resize((28, 24))  # load image and resize
    bplogo_image_login = ImageTk.PhotoImage(bplogo_image)  # use correct library for the use of an image

    bplogo_panel = tk.Label(reportTop, image=bplogo_image_login)  # create a label where the picture goes
    bplogo_panel.image = bplogo_image_login  # use correct library to properly display image
    bplogo_panel.place(x=1415, y=920)  # place the picture

def mainMenu():
    global mainMenuTop

    mainMenuTop = tk.Toplevel(bg="WHITE") # create new window
    mainMenuTop.geometry("1450x1000") # resize window

    createChartForMM() #call function at the start to get chart data


    topMainMenuFrame = tk.Frame(mainMenuTop, width=1200, height=100, highlightcolor="WHITE", highlightbackground="BLACK", highlightthickness=5, bg="WHITE")#create frame to place things inside
    topMainMenuFrame.pack(pady=100)
    leftMainMenuFrame = tk.Frame(mainMenuTop, width=200, height=700, highlightcolor="WHITE", highlightbackground="BLACK", highlightthickness=5, bg="WHITE")#create frame to place things inside
    leftMainMenuFrame.place(x=125, y=195)
    mainMainMenuFrame = tk.Frame(mainMenuTop, width=1005, height=700, highlightcolor="WHITE", highlightbackground="BLACK", highlightthickness=5, bg="WHITE")#create frame to place things inside
    mainMainMenuFrame.place(x=320, y=195)

    mainMenuLabel = tk.Label(topMainMenuFrame, text="Main Menu", bg="WHITE", fg="BLACK", font=('helvetica bold', 50))
    mainMenuLabel.place(x=1, y=10)


    navigationPanelLabel = tk.Label(leftMainMenuFrame, text="Navigation Panel", bg="WHITE", fg="BLACK", font=('helvetica bold', 23))
    navigationPanelLabel.place(x=0, y=0)
    canvas = tk.Canvas(leftMainMenuFrame, width=190, height=1, bg="BLACK")
    canvas.place(x=0, y=30)

    def showCorrectMenu(): #define fucntion to show the correct main menu
        if not isManager.get():
            settingsMenuBtn = tk.Button(leftMainMenuFrame, text="Settings", bg="ORANGE", fg="BLACK", command=lambda: menuToSettings(), width=18, height=2) #Create a button in the navigation panel
            settingsMenuBtn.place(x=0, y=35)

            inventoryMenuBtn = tk.Button(leftMainMenuFrame, text="Inventory", bg="ORANGE", fg="BLACK", command=lambda: menuToInventory(), width=18, height=2)#Create a button in the navigation panel
            inventoryMenuBtn.place(x=0, y=79)

            feedBackMenuBtn = tk.Button(leftMainMenuFrame, text="Feedback", bg="ORANGE", fg="BLACK", command=lambda: menuToFeedback(), width=18, height=2)#Create a button in the navigation panel
            feedBackMenuBtn.place(x=0, y=123)

            logoutMenuBtn = tk.Button(leftMainMenuFrame, text="Log Out", bg="ORANGE", fg="BLACK", command=lambda: mainMenuToLogin(mainMenuTop), width=18, height=2)#Create a button in the navigation panel
            logoutMenuBtn.place(x=0, y=167)

        else:
            settingsMenuBtn = tk.Button(leftMainMenuFrame, text="Settings", bg="ORANGE", fg="BLACK", command=lambda: menuToSettings(), width=18, height=2)#Create a button in the navigation panel
            settingsMenuBtn.place(x=0, y=35)

            inventoryMenuBtn = tk.Button(leftMainMenuFrame, text="Inventory", bg="ORANGE", fg="BLACK", command=lambda: menuToInventory(), width=18, height=2)#Create a button in the navigation panel
            inventoryMenuBtn.place(x=0, y=79)

            addProductMenuBtn = tk.Button(leftMainMenuFrame, text="Add Product", bg="ORANGE", fg="BLACK", command=lambda: menuToAddProduct(), width=18, height=2)#Create a button in the navigation panel
            addProductMenuBtn.place(x=0, y=123)

            orderProductMenuBtn = tk.Button(leftMainMenuFrame, text="Order Product", bg="ORANGE", fg="BLACK", command=lambda: menuToOrderProduct(), width=18, height=2)#Create a button in the navigation panel
            orderProductMenuBtn.place(x=0, y=167)

            reportMenuBtn = tk.Button(leftMainMenuFrame, text="Report", bg="ORANGE", fg="BLACK", command=lambda: menuToReport(), width=18, height=2)#Create a button in the navigation panel
            reportMenuBtn.place(x=0, y=211)

            feedBackMenuBtn = tk.Button(leftMainMenuFrame, text="Feedback", bg="ORANGE", fg="BLACK", command=lambda: menuToFeedback(), width=18, height=2)#Create a button in the navigation panel
            feedBackMenuBtn.place(x=0, y=255)

            addSupplierMenuBtn = tk.Button(leftMainMenuFrame, text="Add Supplier", bg="ORANGE", fg="BLACK", command=lambda: menuToAddSupplier(), width=18, height=2)#Create a button in the navigation panel
            addSupplierMenuBtn.place(x=0, y=299)

            logoutMenuBtn = tk.Button(leftMainMenuFrame, text="Log Out", bg="ORANGE", fg="BLACK", command=lambda: mainMenuToLogin(mainMenuTop), width=18, height=2)#Create a button in the navigation panel
            logoutMenuBtn.place(x=0, y=343)


    showCorrectMenu()#show correct menu function call

    dashBoardLabel = tk.Label(mainMainMenuFrame, text="Dashboard", bg="WHITE", fg="BLACK", font=('helvetica bold', 50))#create text on the top frame
    dashBoardLabel.place(x=0, y=0)

    def widget1MainMenu():#define function to choose the first widget
        widget1MenuBtn = tk.Button(mainMainMenuFrame, text="Add Widget", bg="ORANGE", fg="BLACK", width=35, height=6, cursor = "plus", command=lambda: addWidget1(widget1MenuBtn))
        widget1MenuBtn.place(x=50, y=90)

    def widget2MainMenu():#define function to choose the second widget
        widget2MenuBtn = tk.Button(mainMainMenuFrame, text="Add Widget", bg="ORANGE", fg="BLACK", width=35, height=6, cursor="plus", command=lambda: addWidget2(widget2MenuBtn))
        widget2MenuBtn.place(x=580, y=90)

    widget1MainMenu()#call function
    widget2MainMenu()#call function

    def addWidget1(widget1MenuBtn): #define function to add a widget
        addWidgetTop1 = tk.Toplevel(bg="WHITE")# create new window
        addWidgetTop1.geometry("600x600")

        whatWidget = tk.Label(addWidgetTop1, text="What widget do you want to add?", bg="WHITE", fg="BLACK", font=('helvetica bold', 16))
        whatWidget.pack(side="top")

        if not isManager.get(): # check if manager
            inventoryAddWidget = tk.Button(addWidgetTop1, text="Inventory", bg="ORANGE", fg="BLACK", width=20, height=3, command=lambda: addInventoryWidget1()) #allow for 2 widgets to be added
            inventoryAddWidget.place(x=190, y=100)

            feedBackAddWidget = tk.Button(addWidgetTop1, text="FeedBack", bg="ORANGE", fg="BLACK", width=20, height=3, command=lambda: addFeedBackWidget1())
            feedBackAddWidget.place(x=190, y=200)

            def addInventoryWidget1(): #define function to add the widget
                widget1MenuBtn.place_forget() #remove the add widget button
                addWidgetTop1.withdraw()#remove the page to choose the widget
                inventoryWidget1MenuBtn = tk.Button(mainMainMenuFrame, text="Inventory", bg="ORANGE", fg="BLACK", width=35, height=6, command=lambda: menuToInventory())
                inventoryWidget1MenuBtn.place(x=50, y=90)
                removeInventoryWidget1 = tk.Button(mainMainMenuFrame, text="Remove Widget", bg="ORANGE", fg="BLACK", width=10, height=3, command=lambda: removeInventoryWidget1func()) #create button to remove widget
                removeInventoryWidget1.place(x=160, y=200)

                def removeInventoryWidget1func(): #define function to remove the first widget
                    inventoryWidget1MenuBtn.place_forget()#hide the widget
                    removeInventoryWidget1.place_forget() # remove the remove widget sign
                    widget1MainMenu()#calll fucntion to get the add widget sign again

            def addFeedBackWidget1(): #define function to add the feedback widget
                widget1MenuBtn.place_forget()#remove the add widget button
                addWidgetTop1.withdraw()#remove the page to choose the widget
                feedBackWidget1MenuBtn = tk.Button(mainMainMenuFrame, text="Feedback", bg="ORANGE", fg="BLACK", width=35, height=6, command=lambda: menuToFeedback())
                feedBackWidget1MenuBtn.place(x=50, y=90)
                removefeedBackWidget1 = tk.Button(mainMainMenuFrame, text="Remove Widget", bg="ORANGE", fg="BLACK", width=10, height=3, command=lambda: removeFeedBackWidget1func())#create button to remove widget
                removefeedBackWidget1.place(x=160, y=200)

                def removeFeedBackWidget1func():#define function to remove the first widget
                    feedBackWidget1MenuBtn.place_forget()#hide the widget
                    removefeedBackWidget1.place_forget() # remove the remove widget sign
                    widget1MainMenu()#call fucntion to get the add widget sign again

        else:
            inventoryAddWidget = tk.Button(addWidgetTop1, text="Inventory", bg="ORANGE", fg="BLACK", width=20, height=3, command=lambda: addInventoryWidget12())
            inventoryAddWidget.place(x=190, y=100)

            addProductAddWidget = tk.Button(addWidgetTop1, text="Add Product", bg="ORANGE", fg="BLACK", width=20, height=3, command=lambda: addAddProductWidget1())
            addProductAddWidget.place(x=190, y=200)

            orderProductAddWidget = tk.Button(addWidgetTop1, text="Order Product", bg="ORANGE", fg="BLACK", width=20, height=3, command=lambda: addOrderProductWidget1())
            orderProductAddWidget.place(x=190, y=300)

            reportAddWidget = tk.Button(addWidgetTop1, text="Report", bg="ORANGE", fg="BLACK", width=20, height=3, command=lambda: addReportWidget1())
            reportAddWidget.place(x=190, y=400)

            feedBackAddWidget = tk.Button(addWidgetTop1, text="FeedBack", bg="ORANGE", fg="BLACK", width=20, height=3, command=lambda: addFeedBackWidget12())
            feedBackAddWidget.place(x=190, y=500)

            def addInventoryWidget12():#define function to add the widget
                widget1MenuBtn.place_forget()
                addWidgetTop1.withdraw()
                inventoryWidget12MenuBtn = tk.Button(mainMainMenuFrame, text="Inventory", bg="ORANGE", fg="BLACK", width=35, height=6, command=lambda: menuToInventory())
                inventoryWidget12MenuBtn.place(x=50, y=90)
                removeInventoryWidget12 = tk.Button(mainMainMenuFrame, text="Remove Widget", bg="ORANGE", fg="BLACK", width=10, height=3, command=lambda: removeInventoryWidget12func())
                removeInventoryWidget12.place(x=160, y=200)

                def removeInventoryWidget12func():#define function to remove the widget
                    inventoryWidget12MenuBtn.place_forget()
                    removeInventoryWidget12.place_forget()
                    widget1MainMenu()

            def addAddProductWidget1():#define function to add the widget
                widget1MenuBtn.place_forget()
                addWidgetTop1.withdraw()
                addProductWidget1MenuBtn = tk.Button(mainMainMenuFrame, text="Add Product", bg="ORANGE", fg="BLACK", width=35, height=6, command=lambda: menuToAddProduct())
                addProductWidget1MenuBtn.place(x=50, y=90)
                removeAddProductWidget1 = tk.Button(mainMainMenuFrame, text="Remove Widget", bg="ORANGE", fg="BLACK", width=10, height=3, command=lambda: removeAddProductWidget1func())
                removeAddProductWidget1.place(x=160, y=200)

                def removeAddProductWidget1func():#define function to remove the widget
                    addProductWidget1MenuBtn.place_forget()
                    removeAddProductWidget1.place_forget()
                    widget1MainMenu()

            def addOrderProductWidget1():#define function to add the widget
                widget1MenuBtn.place_forget()
                addWidgetTop1.withdraw()
                orderProductWidget1MenuBtn = tk.Button(mainMainMenuFrame, text="Order Product", bg="ORANGE", fg="BLACK", width=35, height=6, command=lambda: menuToOrderProduct())
                orderProductWidget1MenuBtn.place(x=50, y=90)
                removeOrderProductWidget1 = tk.Button(mainMainMenuFrame, text="Remove Widget", bg="ORANGE", fg="BLACK", width=10, height=3, command=lambda: removeOrderProductWidget1func())
                removeOrderProductWidget1.place(x=160, y=200)

                def removeOrderProductWidget1func():#define function to remove the widget
                    orderProductWidget1MenuBtn.place_forget()
                    removeOrderProductWidget1.place_forget()
                    widget1MainMenu()

            def addReportWidget1():#define function to add the widget
                widget1MenuBtn.place_forget()
                addWidgetTop1.withdraw()
                reportWidget1MenuBtn = tk.Button(mainMainMenuFrame, text="Report", bg="ORANGE", fg="BLACK", width=35, height=6, command=lambda: menuToReport())
                reportWidget1MenuBtn.place(x=50, y=90)
                removeReportWidget1 = tk.Button(mainMainMenuFrame, text="Remove Widget", bg="ORANGE", fg="BLACK", width=10, height=3, command=lambda: removeReportWidget1func())
                removeReportWidget1.place(x=160, y=200)

                def removeReportWidget1func():#define function to remove the widget
                    reportWidget1MenuBtn.place_forget()
                    removeReportWidget1.place_forget()
                    widget1MainMenu()

            def addFeedBackWidget12():#define function to add the widget
                widget1MenuBtn.place_forget()
                addWidgetTop1.withdraw()
                feedBackWidget12MenuBtn = tk.Button(mainMainMenuFrame, text="Feedback", bg="ORANGE", fg="BLACK", width=35, height=6, command=lambda: menuToFeedback())
                feedBackWidget12MenuBtn.place(x=50, y=90)
                removefeedBackWidget12 = tk.Button(mainMainMenuFrame, text="Remove Widget", bg="ORANGE", fg="BLACK", width=10, height=3, command=lambda: removeFeedBackWidget12func())
                removefeedBackWidget12.place(x=160, y=200)

                def removeFeedBackWidget12func():#define function to remove the widget
                    feedBackWidget12MenuBtn.place_forget()
                    removefeedBackWidget12.place_forget()
                    widget1MainMenu()



    def addWidget2(widget2MenuBtn):

        addWidgetTop2 = tk.Toplevel(bg="WHITE")
        addWidgetTop2.geometry("600x600")

        whatWidget = tk.Label(addWidgetTop2, text="What widget do you want to add?", bg="WHITE", fg="BLACK", font=('helvetica bold', 16))
        whatWidget.pack(side="top")

        if not isManager.get():
            inventoryAddWidget = tk.Button(addWidgetTop2, text="Inventory", bg="ORANGE", fg="BLACK", width=20, height=3, command=lambda: addInventoryWidget2())
            inventoryAddWidget.place(x=190, y=100)

            feedBackAddWidget = tk.Button(addWidgetTop2, text="FeedBack", bg="ORANGE", fg="BLACK", width=20, height=3, command=lambda: addFeedBackWidget2())
            feedBackAddWidget.place(x=190, y=200)

            def addInventoryWidget2():#define function to add the widget
                widget2MenuBtn.place_forget()
                addWidgetTop2.withdraw()
                inventoryWidget2MenuBtn = tk.Button(mainMainMenuFrame, text="Inventory", bg="ORANGE", fg="BLACK", width=35, height=6, command=lambda: menuToInventory())
                inventoryWidget2MenuBtn.place(x=580, y=90)
                removeInventoryWidget2 = tk.Button(mainMainMenuFrame, text="Remove Widget", bg="ORANGE", fg="BLACK", width=10, height=3, command=lambda: removeInventoryWidget2func())
                removeInventoryWidget2.place(x=700, y=200)

                def removeInventoryWidget2func():#define function to remove the widget
                    inventoryWidget2MenuBtn.place_forget()
                    removeInventoryWidget2.place_forget()
                    widget2MainMenu()

            def addFeedBackWidget2():#define function to add the widget
                widget2MenuBtn.place_forget()
                addWidgetTop2.withdraw()
                feedBackWidget2MenuBtn = tk.Button(mainMainMenuFrame, text="Feedback", bg="ORANGE", fg="BLACK", width=35, height=6, command=lambda: menuToFeedback())
                feedBackWidget2MenuBtn.place(x=580, y=90)
                removefeedBackWidget2 = tk.Button(mainMainMenuFrame, text="Remove Widget", bg="ORANGE", fg="BLACK", width=10, height=3, command=lambda: removeFeedBackWidget2func())
                removefeedBackWidget2.place(x=700, y=200)

                def removeFeedBackWidget2func():#define function to remove the widget
                    feedBackWidget2MenuBtn.place_forget()
                    removefeedBackWidget2.place_forget()
                    widget2MainMenu()

        else:
            inventoryAddWidget = tk.Button(addWidgetTop2, text="Inventory", bg="ORANGE", fg="BLACK", width=20, height=3, command=lambda: addInventoryWidget21())
            inventoryAddWidget.place(x=190, y=100)

            addProductAddWidget = tk.Button(addWidgetTop2, text="Add Product", bg="ORANGE", fg="BLACK", width=20, height=3, command=lambda: addAddProductWidget2())
            addProductAddWidget.place(x=190, y=200)

            orderProductAddWidget = tk.Button(addWidgetTop2, text="Order Product", bg="ORANGE", fg="BLACK", width=20, height=3, command=lambda: addOrderProductWidget2())
            orderProductAddWidget.place(x=190, y=300)

            reportAddWidget = tk.Button(addWidgetTop2, text="Report", bg="ORANGE", fg="BLACK", width=20, height=3, command=lambda: addReportWidget2())
            reportAddWidget.place(x=190, y=400)

            feedBackAddWidget = tk.Button(addWidgetTop2, text="FeedBack", bg="ORANGE", fg="BLACK", width=20, height=3, command=lambda: addFeedBackWidget21())
            feedBackAddWidget.place(x=190, y=500)

            def addInventoryWidget21():#define function to add the widget
                widget2MenuBtn.place_forget()
                addWidgetTop2.withdraw()
                inventoryWidget21MenuBtn = tk.Button(mainMainMenuFrame, text="Inventory", bg="ORANGE", fg="BLACK", width=35, height=6, command=lambda: menuToInventory())
                inventoryWidget21MenuBtn.place(x=580, y=90)
                removeInventoryWidget21 = tk.Button(mainMainMenuFrame, text="Remove Widget", bg="ORANGE", fg="BLACK", width=10, height=3, command=lambda: removeInventoryWidget21func())
                removeInventoryWidget21.place(x=700, y=200)

                def removeInventoryWidget21func():#define function to remove the widget
                    inventoryWidget21MenuBtn.place_forget()
                    removeInventoryWidget21.place_forget()
                    widget2MainMenu()

            def addAddProductWidget2():#define function to add the widget
                widget2MenuBtn.place_forget()
                addWidgetTop2.withdraw()
                addProductWidget2MenuBtn = tk.Button(mainMainMenuFrame, text="Add Product", bg="ORANGE", fg="BLACK", width=35, height=6, command=lambda: menuToAddProduct())
                addProductWidget2MenuBtn.place(x=580, y=90)
                removeAddProductWidget2 = tk.Button(mainMainMenuFrame, text="Remove Widget", bg="ORANGE", fg="BLACK", width=10, height=3, command=lambda: removeAddProductWidget2func())
                removeAddProductWidget2.place(x=700, y=200)

                def removeAddProductWidget2func():#define function to remove the widget
                    addProductWidget2MenuBtn.place_forget()
                    removeAddProductWidget2.place_forget()
                    widget2MainMenu()

            def addOrderProductWidget2():#define function to add the widget
                widget2MenuBtn.place_forget()
                addWidgetTop2.withdraw()
                orderProductWidget2MenuBtn = tk.Button(mainMainMenuFrame, text="Order Product", bg="ORANGE", fg="BLACK", width=35, height=6, command=lambda: menuToOrderProduct())
                orderProductWidget2MenuBtn.place(x=580, y=90)
                removeOrderProductWidget2 = tk.Button(mainMainMenuFrame, text="Remove Widget", bg="ORANGE", fg="BLACK", width=10, height=3, command=lambda: removeOrderProductWidget2func())
                removeOrderProductWidget2.place(x=700, y=200)

                def removeOrderProductWidget2func():#define function to remove the widget
                    orderProductWidget2MenuBtn.place_forget()
                    removeOrderProductWidget2.place_forget()
                    widget2MainMenu()

            def addReportWidget2():#define function to add the widget
                widget2MenuBtn.place_forget()
                addWidgetTop2.withdraw()
                reportWidget2MenuBtn = tk.Button(mainMainMenuFrame, text="Report", bg="ORANGE", fg="BLACK", width=35, height=6, command=lambda: menuToReport())
                reportWidget2MenuBtn.place(x=580, y=90)
                removeReportWidget2 = tk.Button(mainMainMenuFrame, text="Remove Widget", bg="ORANGE", fg="BLACK", width=10, height=3, command=lambda: removeReportWidget2func())
                removeReportWidget2.place(x=700, y=200)

                def removeReportWidget2func():#define function to remove the widget
                    reportWidget2MenuBtn.place_forget()
                    removeReportWidget2.place_forget()
                    widget2MainMenu()

            def addFeedBackWidget21():#define function to add the widget
                widget2MenuBtn.place_forget()
                addWidgetTop2.withdraw()
                feedBackWidget21MenuBtn = tk.Button(mainMainMenuFrame, text="Feedback", bg="ORANGE", fg="BLACK", width=35, height=6, command=lambda: menuToFeedback())
                feedBackWidget21MenuBtn.place(x=580, y=90)
                removefeedBackWidget21 = tk.Button(mainMainMenuFrame, text="Remove Widget", bg="ORANGE", fg="BLACK", width=10, height=3, command=lambda: removeFeedBackWidget21func())
                removefeedBackWidget21.place(x=700, y=200)

                def removeFeedBackWidget21func():#define function to remove the widget
                    feedBackWidget21MenuBtn.place_forget()
                    removefeedBackWidget21.place_forget()
                    widget2MainMenu()

    salesMenuLabel = tk.Label(mainMainMenuFrame, text="SALES", bg = "ORANGE", fg="WHITE", font=('helvetica bold', 16), width=30, height=2)
    salesMenuLabel.place(x=360, y=280)

    chart_Image = Image.open('/Users/aqibmiah/Downloads/Products MM Data.png').resize((400, 330))  # load image and resize
    chartImageMM = ImageTk.PhotoImage(chart_Image)  # use correct library for the use of an image

    chartMM_panel = tk.Label(mainMainMenuFrame, image=chartImageMM)  # create a label where the picture goes
    chartMM_panel.image = chartImageMM  # use correct library to properly display image
    chartMM_panel.place(x=300, y=340)  # place the picture


    bpExpress_label = tk.Label(mainMenuTop, text="BP Express", bg="WHITE", fg="BLACK")
    bpExpress_label.config(font=('Helvetica bold', 16))
    bpExpress_label.place(anchor="nw")  # anchor to the top left side of the screen

    bplogo_image = Image.open("BP logo.png").resize((28, 24))  # load image and resize
    bplogo_image_login = ImageTk.PhotoImage(bplogo_image)  # use correct library for the use of an image

    bplogo_panel = tk.Label(mainMenuTop, image=bplogo_image_login)  # create a label where the picture goes
    bplogo_panel.image = bplogo_image_login  # use correct library to properly display image
    bplogo_panel.place(x=1415, y=920)  # place the picture


def feedBack(): # define function to send feedback
    feedbackTop = tk.Toplevel(bg="WHITE")
    feedbackTop.geometry("1000x800")

    feedbackLabel = tk.Label(feedbackTop, text="Feedback", bg = "WHITE", fg="BLACK", font=('helvetica bold', 50))
    feedbackLabel.pack(side="top")

    feedbackText = tk.Text(feedbackTop, bg="ORANGE", fg="WHITE", width=80, height=25)
    feedbackText.place(x=230, y=120)

    cancelFeedbackBtn = tk.Button(feedbackTop, text="Cancel", bg="ORANGE", fg="BLACK", width=10, height=3, command=lambda: feedbackToMenu(feedbackTop))
    cancelFeedbackBtn.place(x=350, y=500)

    sendFeedbackBtn = tk.Button(feedbackTop, text="Send", bg="ORANGE", fg="BLACK", width=10, height=3, command=lambda: sendFeedback())
    sendFeedbackBtn.place(x=550, y=500)

    def sendFeedback(): #define function to send the feedback on email
        senderEmail = 'aqibmiah2005@gmail.com' #set a sender email
        recieverEmail = 'aqibmiah2005@gmail.com'#set a recieve email
        feedbackSubject = 'Feedback about BP Express'#add a subject to email
        feedbackMessage = feedbackText.get("1.0", "end")#get all the data from the text box


        emailFeedbackSend = smtplib.SMTP('smtp.gmail.com', 587)#connect tp smtp server  with correct port
        emailFeedbackSend.starttls()#establish secure connection
        emailFeedbackSend.login('aqibmiah2005@gmail.com', 'smtp password required')#login to smtp server
        emailFeedbackSend.sendmail(senderEmail, recieverEmail, f'Subject: {feedbackSubject}\n\n{feedbackMessage}')#send email
        emailFeedbackSend.quit()#quit
        tk.messagebox.showerror('email sent', 'Email was sent!')


    bpExpress_label = tk.Label(feedbackTop, text="BP Express", bg="WHITE", fg="BLACK")
    bpExpress_label.config(font=('Helvetica bold', 16))
    bpExpress_label.place(anchor="nw")  # anchor to the top left side of the screen

    bplogo_image = Image.open("BP logo.png").resize((28, 24))  # load image and resize
    bplogo_image_login = ImageTk.PhotoImage(bplogo_image)  # use correct library for the use of an image

    bplogo_panel = tk.Label(feedbackTop, image=bplogo_image_login)  # create a label where the picture goes
    bplogo_panel.image = bplogo_image_login  # use correct library to properly display image
    bplogo_panel.place(x=968, y=772)  # place the picture




window.eval('tk::PlaceWindow . center')
window.mainloop()


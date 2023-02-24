# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pymongo import MongoClient
import pymongo
from bson import Binary
from random import randint
from tkinter import *
from tkinter import messagebox
import gridfs
from tkinter import Button
import sys
from PIL import Image, ImageTk
from tkinter import filedialog
import tkinter as tk
from io import BytesIO
import base64
import io
from tkinter.filedialog import askopenfilename

try:
	client = MongoClient(port=27017)
	db=client.Assignment08
	print("Connected to MongoDB")
except :
	print("Database connection Error ")
	print("No connection could be made because the target machine actively refused it ")
	messagebox.showerror("Error", "Connection Error")
	sys.exit(1)
	


root=tk.Tk()
root.geometry('400x400')
root.title("ITM Student Management System")

def add_STUDENTS(root,db): 
    def add_query():
        global root
        regno = E1.get()
        name = E2.get()
        email = E3.get()
        batch = E4.get()
        mobile = E5.get()
        
        REGNO = [regno]
        NAME = [name]
        EMAIL = [email]
        BATCH = [batch]
        MOBILE = [mobile]

        # check if an image file was selected
        if img_file_path != '':
            # read the contents of the image file
            with open(img_file_path, 'rb') as f:
                img_data = f.read()
        
        Assignment08 = {
        'REGNO' : REGNO[randint(0, (len(REGNO)-1))] ,
        'NAME' : NAME[randint(0, (len(NAME)-1))],
        'EMAIL' : EMAIL[randint(0, (len(EMAIL)-1))],
        'BATCH' : BATCH[randint(0, (len(BATCH)-1))],
        'MOBILE' : MOBILE[randint(0, (len(MOBILE)-1))],
        'IMAGE' : Binary(img_data)}
        
        if len(regno) == 0 or len(name) == 0 or len(email) == 0 or len(batch) == 0:
            messagebox.showwarning("WARNING", "All fields are compulsory (except mobile number)")
            return

        if db.students.count_documents({'REGNO': regno}, limit=1) > 0:
            messagebox.showwarning("ERROR", "Student already exists")
            return

        result = db.students.insert_one(Assignment08)

        newwin.destroy()
        messagebox.showinfo("Add Student", "Student added successfully")

    def browse_img_file():
        global img_file_path
        img_file_path = askopenfilename()
        img_file_label.config(text=img_file_path)

    newwin = Toplevel(root)
    newwin.geometry('400x500')
    newwin.title("Add Students")

    L1 = Label(newwin, text="REGNO")
    L1.place(x=10, y=50)
    E1 = Entry(newwin, bd=7)
    E1.place(x=100, y=50)

    L2 = Label(newwin, text="NAME")
    L2.place(x=10, y=100)
    E2 = Entry(newwin, bd=7)
    E2.place(x=100, y=100)

    L3 = Label(newwin, text="EMAIL")
    L3.place(x=10, y=150)
    E3 = Entry(newwin, bd=7)
    E3.place(x=100, y=150)

    L4 = Label(newwin, text="BATCH")
    L4.place(x=10, y=200)
    E4 = Entry(newwin, bd=7)
    E4.place(x=100, y=200)

    L5 = Label(newwin, text="MOBILE")
    L5.place(x=10, y=250)
    E5 = Entry(newwin, bd=7)
    E5.place(x=100, y=250)

    # add a label and button for browsing image files
    img_file_label = Label(newwin, text="No image file selected")
    img_file_label.place(x=10, y=300)
    browse_button = Button(newwin, text="Browse", command=browse_img_file)
    browse_button.place(x=10, y=330)
    
    sub=Button(newwin,text="Submit",command=add_query)
    sub.place(x=120,y=350)

def del_data(root,db):
    def delete():
        global root
        regno = E1.get()
        if(len(regno)==0):
            messagebox.showwarning("WARNING", "Enter a Valid REG.NO")
            return
        if db.students.count_documents({ 'REGNO': regno }, limit = 1)==0:
            messagebox.showwarning("ERROR", "STUDENT Does Not Exist")
            return
        else:
            db.students.delete_one({'REGNO':regno})
        newwin.destroy()
        messagebox.showinfo("Delete Student", "Student Deleted")
    newwin=Toplevel(root)
    newwin.geometry('400x350')
    newwin.title("Delete STUDENT")
    L1 = Label(newwin, text="REGNO")
    L1.place(x=10, y=50)
    E1 = Entry(newwin,bd=5)
    E1.place(x=100, y=50)
    sub = Button(newwin, text="Delete Entry", command=delete)
    sub.place(x=120, y=200)

def update_data(root,db):
    def UPDD():
        global root
        regno = E6.get()
        name = E7.get()
        email = E8.get()
        batch = E9.get()
        mobile = E10.get()
        if(len(regno)==0):
            messagebox.showwarning("WARNING", "Enter a Valid REG.NO")
            return

        if db.students.count_documents({ 'REGNO': regno }, limit = 1)==0:
            messagebox.showwarning("ERROR", "STUDENT Does Not Exist")
            return
        if(len(name)!=0):
            db.students.update_one({"REGNO":regno},{"$set": {'NAME' : name}})
        if(len(email)!=0):
            db.students.update_one({"REGNO":regno},{"$set": {'EMAIL' : email}})
        if(len(batch)!=0):
            db.students.update_one({"REGNO":regno},{"$set": {'BATCH' : batch}})
        if(len(mobile)!=0):
            db.students.update_one({"REGNO":regno},{"$set": {'MOBILE' : mobile}})
        
        # check if an image file was selected
        if img_file_path != '':
            # read the contents of the image file
            with open(img_file_path, 'rb') as f:
                img_data = f.read()
            # update the image field for the student with the new image data
            db.students.update_one({"REGNO":regno},{"$set": {'IMAGE' : Binary(img_data)}})
        
        newwin.destroy()
        messagebox.showinfo("Update Student", "Student Updated")

    def browse_img_file():
        global img_file_path
        img_file_path = askopenfilename()
        img_file_label.config(text=img_file_path)

    newwin = Toplevel(root)
    newwin.geometry('400x500')
    newwin.title("Update STUDENTS")
    
    L6 = Label(newwin, text="REGNO")
    L6.place(x=10,y=50)
    E6 = Entry(newwin, bd=7)
    E6.place(x=100,y=50)
    L7 = Label(newwin, text="NAME")
    L7.place(x=10,y=100)
    E7 = Entry(newwin, bd=7)
    E7.place(x=100,y=100)
    L8 = Label(newwin, text="EMAIL")
    L8.place(x=10,y=150)
    E8 = Entry(newwin, bd=7)
    E8.place(x=100,y=150)
    L9 = Label(newwin, text="BATCH")
    L9.place(x=10,y=200)
    E9 = Entry(newwin, bd=7)
    E9.place(x=100,y=200)
    L10 = Label(newwin, text="MOBILE")
    L10.place(x=10,y=250)
    E10 = Entry(newwin, bd=7)
    E10.place(x=100,y=250)
    
    # add a label and button for browsing image files
    img_file_label = Label(newwin, text="No image file selected")
    img_file_label.place(x=10, y=300)
    browse_button = Button(newwin, text="Browse", command=browse_img_file)
    browse_button.place(x=10, y=330)
    sub=Button(newwin,text="Submit",command=UPDD)
    sub.place(x=120,y=350)


def display(root,db):
    newwin=Toplevel(root)
    newwin.geometry('600x600')
    newwin.title("STUDENT Details")
    L1=Label(newwin,text="REGNO")
    L1.grid(row=0,column=0)
    L2 = Label(newwin, text="NAME")
    L2.grid(row=0, column=2)
    L3=Label(newwin,text="EMAIL")
    L3.grid(row=0,column=4)
    L4=Label(newwin,text="BATCH")
    L4.grid(row=0,column=6)
    L5=Label(newwin,text="PHOTO")
    L5.grid(row=0,column=8)
    L6=Label(newwin,text="MOBILE")
    L6.grid(row=0,column=10)
    i=1
    students=db.students.find().sort("regno", pymongo.ASCENDING)
    for x in students:
        photo_path = x['IMAGE']
        photo=Image.open(io.BytesIO(photo_path))
        photo = photo.resize((50, 50), resample=Image.LANCZOS)
        photo = ImageTk.PhotoImage(photo)
        L1 = Label(newwin, text=x['REGNO'])
        L1.grid(row=i, column=0)
        L2 = Label(newwin, text=x['NAME'])
        L2.grid(row=i, column=2)
        L3 = Label(newwin, text=x['EMAIL'])
        L3.grid(row=i, column=4)
        L4 = Label(newwin, text=x['BATCH'])
        L4.grid(row=i, column=6)
        L5 = Label(newwin, image=photo)
        L5.image = photo
        L5.grid(row=i, column=8)
        if 'MOBILE' in x:
            L6 = Label(newwin, text=x['MOBILE'])
            L6.grid(row=i, column=10)
        i+=1


add= Button(root,text='Add New STUDENTS',command=lambda:add_STUDENTS(root,db))
delete= Button(root,text='Delete STUDENTS Entry',command=lambda:del_data(root,db))
update= Button(root,text='Update STUDENTS Info',command=lambda:update_data(root,db))
show= Button(root,text='Show STUDENTS Details',command=lambda:display(root,db))
add.place(x=100,y=100)
delete.place(x=100,y=150)
update.place(x=100,y=200)
show.place(x=100,y=250)
root.mainloop()



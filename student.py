import sqlite3

class student:

    def __init__(self,Fname,Lname,sid,email,age,gender):
        self.first_name = Fname
        self.last_name = Lname
        self.sid = sid
        self.email = email
        self.age = age 
        self.gender = gender 
    

    def toDictionary(self):
        print(self.gender)
        return  {
            'first_name' : self.first_name,
            'last_name' : self.last_name,
            'sid': self.sid ,
            'email' : self.email,
            'age' : self.age,
            'gender' :self.gender
        }
        
from students_editor import students_editor as editor

class student_info:
    
    def __init__(self,student_1,student_2,location,date,time):
        self.student_1 = student_1 
        self.student_2 = student_2 
        self.location  = location  
        self.date      = date 
        self.time      = time
    
    def found(self):
        fieldnames = ['student_1','student_2','location','date','time']
        csv_file = editor('finds.csv',fieldnames)
        data = {
            'student_1' : self.student_1,
            'student_2' : self.student_2,
            'location'  : self.location,
            'date'      : self.date,
            'time'      : self.time
         }
        csv_file.append_file(data)

    
    def getData(sid):
        conn = sqlite3.connect('student.db')
        print("Opened database successfully")
        cursor = conn.execute("SELECT first_name,last_name,sid,email,age,gender From student WHERE first_name = " + '"' + sid + '"')
        for row in cursor:
            print("first_name " + row[0])
            print("last_name " + row[1])
            print("sid " + row[2])
            print("email " + row[3])
            print("age  " + row[4])
            print("gender  " + row[5])
        print("Operation done successfully")
        conn.close()
        return {
            'first_name' :  row[0] ,
            'last_name' :   row[1],
            'sid':  row[2],
            'email' :   row[3],
            'age' :     row[4],
            'gender' :  row[5]
        }
import pickle
import os
from face_encoder import face_encoder
import math
from students_editor import students_editor
from student import student
from student import student_info as info
from datetime import datetime

import numpy as np 
from numpy.core.numeric import count_nonzero

from cam import Capturing
from webcam import RecordingThread, WebCamera
from camera import VideoCamera

from flask import Flask, render_template, request, redirect, url_for, flash ,jsonify
from flask.wrappers import Response
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)

vcam       = None
cam_frame = None
video_camera = None
global_frame = None
g_frame = None
prev_time = ""
prev_name = ""
current_name = ""
count = 0

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "student.db"))

app = Flask(__name__)
app.secret_key = "Secret Key"

app.config["SQLALCHEMY_DATABASE_URI"] = database_file

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

data = pickle.loads(open("encodings_All.pickle", "rb").read())

class Student(db.Model):
    sid = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    first_name = db.Column(db.String(80),nullable=False)
    last_name = db.Column(db.String(80),nullable=False)
    email = db.Column(db.String(80),nullable=False)
    gender = db.Column(db.String(80),nullable=False)
    age = db.Column(db.String(80),nullable=False)
    
    def __init__(self,sid,first_name,last_name,email,gender,age): 
        self.sid =  sid
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.gender = gender
        self.age = age
    
#This is the index route where we are going to
#query on all our employee data
@app.route('/', methods = ['GET', 'POST'])
def Index():
    all_data = Student.query.all()

    return render_template("index.html", employees = all_data)


@app.route('/surv', methods = ['GET', 'POST'])
def surv():
    all_data = Student.query.all()
    return render_template("surv.html", employees = all_data)


#this route is for inserting data to mysql database via html forms
@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == 'POST':

        sid = request.form["sid"]              
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        gender = request.form["gender"]
        age = request.form["age"]

        try:
            my_data = Student(sid,first_name,last_name,email,gender,age)
            db.session.add(my_data)
            db.session.commit()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            flash(error)
        
        

        return redirect(url_for('Index'))


#this is our update route where we are going to update our employee
@app.route('/update', methods = ['GET','POST'])
def update():
    if request.method == 'POST':
        my_data = Student.query.get(request.form.get('oldSid'))
        my_data.sid = request.form["oldSid"]              
        my_data.first_name = request.form["first_name"]
        my_data.last_name = request.form["last_name"]
        my_data.email = request.form["email"]
        my_data.gender = request.form["gender"]
        my_data.age = request.form["age"]

        db.session.commit()
        flash("Student Updated Successfully")

        return redirect(url_for('Index'))


#This route is for deleting our employee
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Student.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Student Deleted Successfully")

    return redirect(url_for('Index'))

counter = 0
f=None
@app.route('/trainer', methods = ['GET','POST'])
def trainer():
    global counter
    global f
    if f is None:
        f = face_encoder('encodings_Allolf.pickle','dataset','hog')
        f.start()
    if request.method == 'POST':
        json = request.get_json()
        status = json['status']
        print("status "+ status)
        if status == "true" and f._running:
            print(f.imgLen())
            print(f.imageNumber())
            counter = (f.imageNumber()/f.imgLen())*100
            print(math.trunc(counter))
            # if counter == 0.0:
            #     print('stoposaafssaaaaa')
            #     return jsonify(value="-1")
            if counter > 100:
                return jsonify(value="100")
            else:
                return jsonify(value = math.trunc(counter))
        else:
            return jsonify(value="-1")
    
    
    # f.run()
    return render_template("trainer.html",student ='Saadain')

@app.route('/record_status', methods=['POST'])
def record_status():
    global video_camera 
    if video_camera == None:
        video_camera = VideoCamera()

    json = request.get_json()

    status = json['status']
    print(json)
    

    if status == "true":
        folderName = json['name']
        video_camera.start_record(folderName)
        return jsonify(result="started")
    else:
        video_camera.stop_record()
        return jsonify(result="stopped")


def video_stream():
    global video_camera 
    global global_frame
    global current_name
    global count

    if video_camera == None:
        video_camera = VideoCamera()
        
    while True:
        frame = video_camera.get_frame()
        # current_name = "bane"+ str(count)
        # count = count +  1
        if frame != None:
            global_frame = frame
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
                            b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n\r\n')
    

def cam_stream():
    global vcam
    global cam_frame
    global current_name
    global prev_name
    global prev_time
    print('loadings')
    camName = 'Corridor1'
    if vcam == None:
        vcam = Capturing(0,data)
        
    while True:
        name , frame = vcam.get_frame()
        current_name = name
        print("the name is : ")
        print(current_name)

        if current_name != prev_name and len(current_name)>0:
            add_info(current_name,camName)
            prev_name = current_name
            # You could also pass datetime.time object in this part and convert it to string.
            prev_time = str(datetime.now().strftime("%H:%M:%S")) 
        else:            
            time_now = str(datetime.now().strftime("%H:%M:%S"))
            diff = datetime.strptime(time_now, "%H:%M:%S") - datetime.strptime(prev_time, "%H:%M:%S")            
            # Get the time in hours i.e. 9.60, 8.5
            result = diff.seconds
            print(result)
            if result >= 10:
                prev_name=[]
                prev_time = ""
                print("resetting time")
            
            

        current_name = []
        if frame != None:
            cam_frame = frame
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
                            b'Content-Type: image/jpeg\r\n\r\n' + cam_frame + b'\r\n\r\n')

@app.route('/webcam')
def webcam():
    return Response(cam_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def webcam_stream():
    # global video_camera 
    global g_frame
    
    # if video_camera == None:
    # video = cv2.VideoCapture(0)
    recordingThread = RecordingThread("Video Recording Thread")
    recordingThread.start()
        # video_camera = WebCamera()
        
    while True:
        # frame = video_camera.get_frame()
        frame = recordingThread.get_frame()

        if frame != None:
            g_frame = frame
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
                            b'Content-Type: image/jpeg\r\n\r\n' + g_frame + b'\r\n\r\n')


@app.route('/video_viewer')
def video_viewer():
    return Response(video_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/getName',methods=['POST'])
def getName():
    # global video_camera 
    # if video_camera == None:
    #     video_camera = VideoCamera()

    json = request.get_json()

    status = json['status']
    print("status "+ status)
    if status == "true":
        print(prev_name)
        return jsonify(name = prev_name)
    else:
        return jsonify(name="")


def add_info(stdn_list , loc):
    if(len(stdn_list)==1 and "Unknown" in stdn_list):
        return 0
    x = np.array(stdn_list)
    students = np.unique(x)
    time = datetime.now().strftime("%H:%M:%S")
    day = datetime.now().strftime("%d-%m-%Y")
    if len(students) > 1 :
        for i in students:
            for j in students:
                if i != j:
                    std_info = info(i,j,loc,day,time )
                    std_info.found()
    else:
        std_info = info(students[0],"",loc,day,time )
        std_info.found()
    return 1 

if __name__ == "__main__":
    app.run(debug=True)
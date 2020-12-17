import cv2
import threading
import os

class RecordingThread (threading.Thread):
    def __init__(self, name, camera,folderName):
        threading.Thread.__init__(self)
        self.name = name
        self.isRunning = True
        self.folderName = folderName
        print("folder name = " + folderName)
        
        # how to make image data set from webcam
        self.path = os.getcwd() #to get current directory
        print ("The current working directory is %s" % self.path)
        self.path = self.path + "/dataset/" + folderName

        access_rights = 0o755 #giving writing permissions

        try:
            os.mkdir(self.path)  #making directory
        except OSError:
            print("Creation of the directory %s failed" % self.path)
            return None
        else:
            print("Successfully created the directory %s " % self.path)
        


        self.cap = camera
        # fourcc = cv2.VideoWriter_fourcc(*'MP4V')
        # self.out = cv2.VideoWriter('./static/video.mp4',fourcc, 20.0, (640,480))
        self.cascadePath = "haarcascade_frontalface_default.xml"
        self.faceCascade = cv2.CascadeClassifier(self.cascadePath)
    
    def run(self):
        self.count = 0
        while self.isRunning:
            ret, frame = self.cap.read()
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.faceCascade.detectMultiScale(
                    gray,
                    scaleFactor=1.2,
                    minNeighbors=5
                )
                for (x,y,w,h) in faces:
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                    roi_gray = gray[y:y+h, x:x+w]
                    print('saving images')
                    roi_color = frame[y:y+h, x:x+w]
                    cv2.imwrite(self.path + "/frame%d.jpg" %self.count,roi_color)
                    cv2.imwrite(self.path + "/gray%d.jpg" % self.count,roi_gray) 
                    self.count = self.count + 1
                # self.out.write(frame)
                    # self.out.write(roi_color)
            if self.count == 300 :
                self.stop()
                break
        self.cap.release()

    def stop(self):
        print("counted %d frames",self.count*2)
        self.isRunning = False

    def __del__(self):
        # self.out.release()
        self.cap.release()

class VideoCamera(object):
    def __init__(self):
        # Open a camera
        self.cap = cv2.VideoCapture(1)
      
        # Initialize video recording environment
        self.is_record = False
        # self.out = None

        # Thread for recording
        self.recordingThread = None
    
    def __del__(self):
        self.cap.release()
    
    def get_frame(self):
        ret, frame = self.cap.read()

        if ret:
            ret, jpeg = cv2.imencode('.jpg', frame)

            # Record video
            # if self.is_record:
            #     if self.out == None:
            #         fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            #         self.out = cv2.VideoWriter('./static/video.avi',fourcc, 20.0, (640,480))
                
            #     ret, frame = self.cap.read()
            #     if ret:
            #         self.out.write(frame)
            # else:
            #     if self.out != None:
            #         self.out.release()
            #         self.out = None  

            return jpeg.tobytes()
      
        else:
            return None

    def start_record(self,folderName):
        self.is_record = True
        self.recordingThread = RecordingThread("Video Recording Thread", self.cap,folderName)
        self.recordingThread.start()

    def stop_record(self):
        self.is_record = False

        if self.recordingThread != None:
            self.recordingThread.stop()

            
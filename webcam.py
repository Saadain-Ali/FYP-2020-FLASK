import threading
import cv2
import face_recognition
import argparse
import imutils
import pickle
import time
import numpy as np
import cv2
import os



class RecordingThread (threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        
        
        self.name = name
        self.isRunning = True

        self.counter = 0
        self.classNames = []

        # load the known faces and embeddings
        print("[INFO] loading encodings...")

        # Loading Encodings from pickel file
        self.data = pickle.loads(open("encodings_All.pickle", "rb").read())
        self.encodeListKnown = self.data['encodings']

        # testing pickel file data not necessary
        print(len(self.encodeListKnown))
        self.classNames = self.data['names']

        # face recognition with HaarCascade 
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read('trainer/trainer.yml')
        self.cascadePath = "haarcascade_frontalface_default.xml"
        self.faceCascade = cv2.CascadeClassifier(self.cascadePath)


        self.cap =  cv2.VideoCapture("arbaz.mp4")

    def run(self):
        # while self.isRunning:
        #     ret, img = self.cap.read()
        #     if ret:
        print("imrubbds")
        
        # self.out.release()

    def haarReco(self,img):
        # cv2.imshow('camera',img) 
        name = "unknown"
        names =	{
            62445: "saadain",
            62647: "arbaz",
            12345: "ghayaas"
        }
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
        faces = self.faceCascade.detectMultiScale( 
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            #minSize = (int(minW), int(minH)),
        )
        
        for(x,y,w,h) in faces:
            
            
            #cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
        
            id, confidence = self.recognizer.predict(gray[y:y+h,x:x+w])
            # print("id is " + names[id])
            # Check if confidence is less them 100 ==> "0" is perfect match 
            if (confidence <  100):
                name = names[id]
                #confidence = "  {0}%".format(round(100 - confidence))
                
                #print(confidence)
                #print(int(float(confidence.split('%')[0])))
                
                #if(int(float(confidence.split('%')[0])) > 30):
                #    print("Haar reco")
                #    name = names[id]
                    
            else:
                name = "unknown"
                confidence = "  {0}%".format(round(100 - confidence))
        
        return name.lower()

    def get_frame(self):
        # success, image = self.video.read()
        self.current_name  = ""
        success, img = self.cap.read()
        # means 1/4th of orignal image
        imgSmall = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgSmall = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # imgSmall = imutils.resize(img, width=750)
        r = img.shape[1] / float(imgSmall.shape[1])

        # Findig face location and encodes them
        facesCurFrame = face_recognition.face_locations(imgSmall)
        # print(facesCurFrame)
        encodeCurFrame = face_recognition.face_encodings(imgSmall, facesCurFrame)
        # 

        names = []

        # Matching face encodings with the DB
        for encoding,faceLoc in zip(encodeCurFrame,facesCurFrame):
            # attempt to match each face in the input image to our known

            # encodings
            matches = face_recognition.compare_faces(self.data["encodings"], encoding,tolerance= 0.5)

            # print(matches)
            name = "Unknown"
        # 

        # Applying 3 different algorithms to correctly match the encodings with the Database

        # Algo 1 
            if True in matches:

                name1 = "unknown"
                faceDis = face_recognition.face_distance(self.encodeListKnown,encoding)
                # #lowest distance will be our best match
                #print(faceDis)
                minDis = np.min(faceDis)
                matcheIndex = np.argmin(faceDis)
                name1 = self.classNames[matcheIndex]
                # print("name 1 " + name1)
        # Algo 1 ends

        # Algo 2
                name2 = "unknown"
    			# find the indexes of all matched faces then initialize a
    			# dictionary to count the total number of times each face
    			# was matched
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}

    			# loop over the matched indexes and maintain a count for
    			# each recognized face face
                for i in matchedIdxs:
                    name2 = self.classNames[i]
                    counts[name2] = counts.get(name2, 0) + 1
    			# determine the recognized face with the largest number
    			# of votes (note: in the event of an unlikely tie Python
    			# will select first entry in the dictionary)
                name2 = max(counts, key=counts.get)
                # print("name 2 " +name2)
        # Algo 2 ends

        # Algo 3 Haar Cascade
                haarName = self.haarReco(img)
                # print("haarName = " + haarName )
        # Algo 3 ends 

        #Compairing 
        # if all three name , name2 and name3 has the same name than its a perfect match
                if name1.lower() == name2.lower() or haarName == name1.lower():
                    print("all match match")
                    name = name1
            names.append(name)
        #======================End Compare==============================================================#

        # loop over the recognized faces
        for ((top, right, bottom, left), name) in zip(facesCurFrame, names):
    		# rescale the face coordinates
            top = int(top * r)
            right = int(right * r)
            bottom = int(bottom * r)
            left = int(left * r)
            # draw the predicted face name on the image
            cv2.rectangle(img, (left, top), (right, bottom),(0, 255, 0), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(img, name.upper(), (left, y), cv2.FONT_HERSHEY_SIMPLEX,0.75, (0, 255, 0), 2)
        #================================================================================================ #

        # for orignal
        # ret, jpeg = cv2.imencode('.jpg', image)
        ret, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()



    def stop(self):
        self.isRunning = False

    def __del__(self):
        self.recordingThread.stop()
        self.cap.release()








class WebCamera(object):
    def __init__(self):
        
        


        # self.video = cv2.VideoCapture(0)
        self.recordingThread = RecordingThread("Video Recording Thread")
        re = self.recordingThread.start()
    

    # def haarReco(self,img):
    #     # cv2.imshow('camera',img) 
    #     name = "unknown"
    #     names =	{
    #         62445: "saadain",
    #         62647: "arbaz",
    #         12345: "ghayaas"
    #     }
    #     gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    #     faces = self.faceCascade.detectMultiScale( 
    #         gray,
    #         scaleFactor = 1.2,
    #         minNeighbors = 5,
    #         #minSize = (int(minW), int(minH)),
    #     )
        
    #     for(x,y,w,h) in faces:
            
            
    #         #cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
        
    #         id, confidence = self.recognizer.predict(gray[y:y+h,x:x+w])
    #         # print("id is " + names[id])
    #         # Check if confidence is less them 100 ==> "0" is perfect match 
    #         if (confidence <  100):
    #             name = names[id]
    #             #confidence = "  {0}%".format(round(100 - confidence))
                
    #             #print(confidence)
    #             #print(int(float(confidence.split('%')[0])))
                
    #             #if(int(float(confidence.split('%')[0])) > 30):
    #             #    print("Haar reco")
    #             #    name = names[id]
                    
    #         else:
    #             name = "unknown"
    #             confidence = "  {0}%".format(round(100 - confidence))
        
    #     return name.lower()





    def __del__(self):
        self.recordingThread.stop()
        self.video.release()


    def get_frame(self):
        return self.recordingThread.frame.tobytes()
        # self.recordingThread = RecordingThread("Video Recording Thread", self.video)
        # self.recordingThread.start()
    # def get_frame(self):
    #     # success, image = self.video.read()
    #     self.current_name  = ""
    #     success, img = self.video.read()
    #     # means 1/4th of orignal image
    #     imgSmall = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    #     imgSmall = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #     # imgSmall = imutils.resize(img, width=750)
    #     r = img.shape[1] / float(imgSmall.shape[1])

    #     # Findig face location and encodes them
    #     facesCurFrame = face_recognition.face_locations(imgSmall)
    #     # print(facesCurFrame)
    #     encodeCurFrame = face_recognition.face_encodings(imgSmall, facesCurFrame)
    #     # 

    #     names = []

    #     # Matching face encodings with the DB
    #     for encoding,faceLoc in zip(encodeCurFrame,facesCurFrame):
    #         # attempt to match each face in the input image to our known

    #         # encodings
    #         matches = face_recognition.compare_faces(self.data["encodings"], encoding,tolerance= 0.5)

    #         # print(matches)
    #         name = "Unknown"
    #     # 

    #     # Applying 3 different algorithms to correctly match the encodings with the Database

    #     # Algo 1 
    #         if True in matches:

    #             name1 = "unknown"
    #             faceDis = face_recognition.face_distance(self.encodeListKnown,encoding)
    #             # #lowest distance will be our best match
    #             #print(faceDis)
    #             minDis = np.min(faceDis)
    #             matcheIndex = np.argmin(faceDis)
    #             name1 = self.classNames[matcheIndex]
    #             # print("name 1 " + name1)
    #     # Algo 1 ends

    #     # Algo 2
    #             name2 = "unknown"
    # 			# find the indexes of all matched faces then initialize a
    # 			# dictionary to count the total number of times each face
    # 			# was matched
    #             matchedIdxs = [i for (i, b) in enumerate(matches) if b]
    #             counts = {}

    # 			# loop over the matched indexes and maintain a count for
    # 			# each recognized face face
    #             for i in matchedIdxs:
    #                 name2 = self.classNames[i]
    #                 counts[name2] = counts.get(name2, 0) + 1
    # 			# determine the recognized face with the largest number
    # 			# of votes (note: in the event of an unlikely tie Python
    # 			# will select first entry in the dictionary)
    #             name2 = max(counts, key=counts.get)
    #             # print("name 2 " +name2)
    #     # Algo 2 ends

    #     # Algo 3 Haar Cascade
    #             haarName = self.haarReco(img)
    #             # print("haarName = " + haarName )
    #     # Algo 3 ends 

    #     #Compairing 
    #     # if all three name , name2 and name3 has the same name than its a perfect match
    #             if name1.lower() == name2.lower() or haarName == name1.lower():
    #                 print("all match match")
    #                 name = name1
    #         names.append(name)
    #     #======================End Compare==============================================================#

    #     # loop over the recognized faces
    #     for ((top, right, bottom, left), name) in zip(facesCurFrame, names):
    # 		# rescale the face coordinates
    #         top = int(top * r)
    #         right = int(right * r)
    #         bottom = int(bottom * r)
    #         left = int(left * r)
    #         # draw the predicted face name on the image
    #         cv2.rectangle(img, (left, top), (right, bottom),(0, 255, 0), 2)
    #         y = top - 15 if top - 15 > 15 else top + 15
    #         cv2.putText(img, name.upper(), (left, y), cv2.FONT_HERSHEY_SIMPLEX,0.75, (0, 255, 0), 2)
    #     #================================================================================================ #

    #     # for orignal
    #     # ret, jpeg = cv2.imencode('.jpg', image)
    #     ret, jpeg = cv2.imencode('.jpg', img)
    #     return jpeg.tobytes()
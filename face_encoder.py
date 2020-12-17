from imutils import paths
import face_recognition
import pickle
import cv2
import ctypes 
import os
import threading

class face_encoder(threading.Thread):
    imgNum = 0
    def __init__(self,encodings,dataset,detection_method):
        threading.Thread.__init__(self)
        self._running = True
        self.args = {
            'encodings' : encodings,
            'dataset'   : dataset,
            'detection-method' : detection_method
        }
    def imgLen(self):
        imagePaths = list(paths.list_images(self.args["dataset"]))
        return len(imagePaths)
    
    def imageNumber(self):
        return self.imgNum
    
    def get_id(self): 
        # returns id of the respective thread 
        if hasattr(self, '_thread_id'): 
            return self._thread_id 
        for id, thread in threading._active.items(): 
            if thread is self: 
                return id

    def raise_exception(self): 
        thread_id = self.get_id() 
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 
              ctypes.py_object(SystemExit)) 
        if res < 1: 
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0) 
            print('Exception raise failure')
    
    def stop(self):
        print('zfop')
        self._running = False
        # self.raise_exception()
        
    def run(self):
        while self._running:
            global imgNum
            if os.path.exists(self.args["dataset"] or os.path.exists(self.args["encodings"])):
                print("[INFO] quantifying faces...")
                imagePaths = list(paths.list_images(self.args["dataset"]))

                # to save known encodings and names
                knownEncodings = []
                knownNames = []
                data = []
                with open(self.args["encodings"],'rb') as rfp: 
                    data = pickle.load(rfp)
                    knownEncodings = data["encodings"]
                    knownNames = data["names"]
                
                namelist = []
                for (i, imagePath) in enumerate(imagePaths):
                    # extract the person name from the image path
                    print("[INFO] processing image {}/{}".format(i + 1,len(imagePaths)))
                    namelist.append(imagePath.split(os.path.sep)[-2])
                
                # finding difference between folder names and KnownNames from encodings
                toBeTrain= list((set(namelist)).difference(set(knownNames)))
                print('names tobe trained are :',end='')
                print(set(toBeTrain))
                if len(toBeTrain) <= 0:
                    print('nothings here')
                    self.stop()
                # input('jesl')
                for (i, imagePath) in enumerate(imagePaths):
                    # extract the person name from the image path
                    # print ('[INFO] processing image {}/{}'.format(i + 1, len(imagePaths)))
                    name = imagePath.split(os.path.sep)[-2]
                    # print ('name is ' + name)
                    if name not in toBeTrain:
                        print (name + ' already exists skippping in ')
                    else:
                        # load the input image and convert it from RGB (OpenCV ordering)
                        # to dlib ordering (RGB)
                        self.imgNum = i+1
                        print ('Now encoding ' + name + '-' + str(self.imgNum))
                        
                        image = cv2.imread(imagePath)
                        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                        # detect the (x, y)-coordinates of the bounding boxes
                        # corresponding to each face in the input image
                        boxes = face_recognition.face_locations(rgb, model=self.args['detection-method'])
                        # compute the facial embedding for the face
                        encodings = face_recognition.face_encodings(rgb, boxes)
                        # loop over the encodings
                        for encoding in encodings:
                            # add each encoding + name to our set of known names and
                            # encodings
                            knownEncodings.append(encoding)
                            knownNames.append(name)
                # dump the facial encodings + names to disk
                print("[INFO] serializing encodings...")
                data = {"encodings": knownEncodings, "names": knownNames}
                # data.append(newData)
                # Now we "sync" our database
                with open(self.args["encodings"],'wb') as wfp:
                    pickle.dump(data, wfp)
                # Re-load our database
                with open(self.args["encodings"],'rb') as rfp:
                    temp = pickle.load(rfp)
                print(set(temp["names"]))
                self.stop()
            else:
                print('dataset or encodings does not exist')
                self.stop()
    
    def __del__(self):
        # self.out.release()
        self.stop()
# from face_encoder import face_encoder
# import time
# f = face_encoder('encodings_Allolf.pickle','dataset/60838','hog')
# f.start()
# # f.join()
# # f.run()
# while(f._running):
#     print(f.imgLen())
#     print(f.imageNumber())
#     time.sleep(2)



# from student import student_info

# std_info = student_info.getData(sid="Saadain")

# print(std_info['sid'])

import numpy as np
import cv2

cap = cv2.VideoCapture(-1)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
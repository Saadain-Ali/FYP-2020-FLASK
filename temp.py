from face_encoder import face_encoder
import time
f = face_encoder('encodings_Allolf.pickle','dataset/60838','hog')
f.start()
# f.join()
# f.run()
while(f._running):
    print(f.imgLen())
    print(f.imageNumber())
    time.sleep(2)
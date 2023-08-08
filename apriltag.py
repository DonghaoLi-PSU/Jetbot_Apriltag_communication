from dt_apriltags import Detector
import cv2
import numpy as np
import os
import math
import time
import sys
from jetbot import Camera

# Setup Camera
# Full reset of the camera
os.system("echo 'jetbot' | sudo -S systemctl restart nvargus-daemon && printf '\n'")
# Check device number
os.system("ls -ltrh /dev/video*")

print("Argv len: "+str(len(sys.argv)))
print(sys.argv)
if len(sys.argv) != 11:
    print('Wrong Input')
    exit()

cameraMatrix = np.asarray(sys.argv[1:10],dtype=float).reshape(3,3)

#print(cameraMatrix.shape)
#print(cameraMatrix)

apt_id = int(sys.argv[-1])
# CSI Camera (Raspberry Pi Camera Module V2)

camera = Camera(width=1024, height=768)
camera.running = True

at_detector = Detector(searchpath=['apriltags'],
                               families='tag36h11',
                               nthreads=1,
                               quad_decimate=1.0,
                               quad_sigma=0.0,
                               refine_edges=1,
                               decode_sharpening=0.25,
                               debug=0)

#cameraMatrix = np.array([[1.95644364e+03, 0.00000000e+00, 5.61397293e+02],[0.00000000e+00, 2.27889551e+03, 4.05640820e+02],[0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
        #camera_params = ( cameraMatrix[0,0], cameraMatrix[1,1], cameraMatrix[0,2], cameraMatrix[1,2] )
        #camera_params = ([fx, fy, cx, cy])
camera_params = ( cameraMatrix[0,0], cameraMatrix[1,1], cameraMatrix[0,2], cameraMatrix[1,2] )


start_time = time.time()
print("Start AprilTag")
sig_time = time.time()
while time.time()-start_time < 60:
    if time.time()-sig_time>1:
        #print(time.time()-sig_time)
        sig_time = time.time()
        
        instant_image=camera.value
        img = cv2.cvtColor(instant_image, cv2.COLOR_BGR2GRAY)
        
        tags = at_detector.detect(img, True, camera_params, tag_size=0.075)

        for i in range(len(tags)):
            if tags[i].tag_id == apt_id:
                print("TAG_ID"+str(apt_id))
                Current_heading_angle=(1.5707+math.asin(tags[i].pose_R.item(1)))
                currentlocation = [round(tags[i].center[i]),round(img.shape[i]-tags[i].center[1]), round(Current_heading_angle*180/np.pi)]
                print(currentlocation)
                #print(time.time())

print("End AprilTag")
camera.stop()
#del camera
exit()
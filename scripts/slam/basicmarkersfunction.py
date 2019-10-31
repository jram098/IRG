import cv2
from cv2 import aruco
import numpy as np


NUM_MARKERS = 10

def main_write():
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    imgs = [aruco.drawMarker(aruco_dict,i,200) for i in range(NUM_MARKERS)]
    for i in range(NUM_MARKERS):
        imname = "assets/" + str(i) + "_marker.jpg"
        cv2.imwrite(imname, imgs[i])
    print (len(imgs), "markers done!")

def main_detect():
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(cv2.COLOR_BGR2GRAY)
        parameters = aruco.DetectorParameters_create()
        parameters.adaptiveThreshConstant = 10
        corners, ids, rej = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        font = cv2.FONT_HERSHEY_SIMPLEX
        if np.all(ids!= None):
            rvec, tvec ,_ = aruco.estimatePoseSingleMarkers(corners, 0.05, mtx, dist)
            
        cv2.imshow()
        cv2.waitKey(5)



if __name__ == '__main__':
    main_detect()

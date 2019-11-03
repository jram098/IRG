import cv2
from cv2 import aruco
import numpy as np
import glob


NUM_MARKERS = 10

def main_write():
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    imgs = [aruco.drawMarker(aruco_dict,i,200) for i in range(NUM_MARKERS)]
    for i in range(NUM_MARKERS):
        imname = "assets/" + str(i) + "_marker.jpg"
        cv2.imwrite(imname, imgs[i])
    print (len(imgs), "markers done!")

def main_detect(dist_constant=None):

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    # checkerboard of size (7 x 6) is used
    objp = np.zeros((6*7,3), np.float32)
    objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

    # arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.

    # iterating through all calibration images
    # in the folder
    images = glob.glob('calib_images/*.jpg')

    ovr = None
    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        ovr = gray
        # find the chess board (calibration pattern) corners
        ret, corners = cv2.findChessboardCorners(gray, (7,6),None)

        # if calibration pattern is found, add object points,
        # image points (after refining them)
        if ret == True:
            objpoints.append(objp)

            # Refine the corners of the detected corners
            corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
            imgpoints.append(corners2)

            # Draw and display the corners
            img = cv2.drawChessboardCorners(img, (7,6), corners2,ret)
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, ovr.shape[::-1],None,None)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    print("Calibrated Camera")
    if (dist_constant):
        print("Using distance constant:", dist_constant)
    else:
        distance = float(input("Input Calibration Real Life Distance: "))
        #width = input("Input Calibration Real Life Height: ")
        input("press key and enter to start distance calibration")
        cap = cv2.VideoCapture(0)
        while True:
            
            
            ret, frame = None, None
            for i in range(10):
                ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            parameters = aruco.DetectorParameters_create()
            parameters.adaptiveThreshConstant = 10
            corners, ids, rej = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
            if corners != []:
                break

        pix_height = abs(corners[0][0][0][1] - corners[0][0][2][1])
        print(pix_height)
        dist_constant = distance*pix_height
        cap.release()
        print("Your NEW dist_constant is:", dist_constant)
    
    input("press key and enter if ready to start videocapture")

    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        parameters = aruco.DetectorParameters_create()
        parameters.adaptiveThreshConstant = 10
        corners, ids, rej = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        font = cv2.FONT_HERSHEY_SIMPLEX
        if np.all(ids!= None):
            rvec, tvec ,_ = aruco.estimatePoseSingleMarkers(corners, 0.05, mtx, dist)

            for i in range(0, ids.size):
                # draw axis for the aruco markers
                aruco.drawAxis(frame, mtx, dist, rvec[i], tvec[i], 0.1)

            # draw a square around the markers
            aruco.drawDetectedMarkers(frame, corners)


            for i in range(len(ids)):
                sample_id = ids[i]
                sample_corners = corners[i][0]
                print(sample_corners)

                sample_real_dist = dist_constant/(abs(sample_corners[0][1] - sample_corners[2][1]))
                print("Id", sample_id, "Distance is :", sample_real_dist)

            # code to show ids of the marker found
            strg = ''
            for i in range(0, ids.size):
                strg += str(ids[i][0])+', '

            cv2.putText(frame, "Id: " + strg, (0,64), font, 1, (0,255,0),2,cv2.LINE_AA)

        cv2.imshow("frame", frame)
        cv2.waitKey(100)

if __name__ == '__main__':
    main_detect(1950.2) #1950.2 is a dummmy value that works reasonably well on a MacBook Pro 2018



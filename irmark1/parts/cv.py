import time
import cv2
import numpy as np
from irmark1.utils import compute_normal_map
from collections import namedtuple

class ImgGreyscale():

    def run(self, img_arr):
        img_arr = cv2.cvtColor(img_arr, cv2.COLOR_RGB2GRAY)
        return img_arr

    def shutdown(self):
        pass

class ImgWriter():

    def __init__(self, filename):
        self.filename = filename

    def run(self, img_arr):
        cv2.imwrite(self.filename, img_arr)

    def shutdown(self):
        pass

class ImgBGR2RGB():

    def run(self, img_arr):
        if img_arr is None:
            return None
        try:
            img_arr = cv2.cvtColor(img_arr, cv2.COLOR_BGR2RGB)
            return img_arr
        except:
            return None

    def shutdown(self):
        pass

class ImgRGB2BGR():

    def run(self, img_arr):
        if img_arr is None:
            return None
        img_arr = cv2.cvtColor(img_arr, cv2.COLOR_RGB2BGR)
        return img_arr

    def shutdown(self):
        pass

class ImageScale():

    def __init__(self, scale):
        self.scale = scale

    def run(self, img_arr):
        if img_arr is None:
            return None
        try:
            return cv2.resize(img_arr, (0,0), fx=self.scale, fy=self.scale)
        except:
            return None

    def shutdown(self):
        pass

class ImageRotateBound():
    '''
    credit:
    https://www.pyimagesearch.com/2017/01/02/rotate-images-correctly-with-opencv-and-python/
    '''

    def __init__(self, rot_deg):
        self.rot_deg = rot_deg

    def run(self, image):
        if image is None:
            return None

        # grab the dimensions of the image and then determine the
        # center
        (h, w) = image.shape[:2]
        (cX, cY) = (w // 2, h // 2)
    
        # grab the rotation matrix (applying the negative of the
        # angle to rotate clockwise), then grab the sine and cosine
        # (i.e., the rotation components of the matrix)
        M = cv2.getRotationMatrix2D((cX, cY), -self.rot_deg, 1.0)
        cos = np.abs(M[0, 0])
        sin = np.abs(M[0, 1])
    
        # compute the new bounding dimensions of the image
        nW = int((h * sin) + (w * cos))
        nH = int((h * cos) + (w * sin))
    
        # adjust the rotation matrix to take into account translation
        M[0, 2] += (nW / 2) - cX
        M[1, 2] += (nH / 2) - cY
    
        # perform the actual rotation and return the image
        return cv2.warpAffine(image, M, (nW, nH))

    def shutdown(self):
        pass

class ImgCanny():

    def __init__(self, low_threshold=60, high_threshold=110):
        self.low_threshold = low_threshold
        self.high_threshold = high_threshold
        
        
    def run(self, img_arr):
        return cv2.Canny(img_arr, 
                         self.low_threshold, 
                         self.high_threshold)

    def shutdown(self):
        pass
    

class ImgGaussianBlur():

    def __init__(self, kernal_size=5):
        self.kernal_size = kernal_size
        
    def run(self, img_arr):
        return cv2.GaussianBlur(img_arr, 
                                (self.kernel_size, self.kernel_size), 0)

    def shutdown(self):
        pass


class ArrowKeyboardControls:
    '''
    kind of sucky control, only one press active at a time. 
    good enough for a little testing.
    requires that you have an CvImageView open and it has focus.
    '''
    def __init__(self):
        self.left = 2424832
        self.right = 2555904
        self.up = 2490368
        self.down = 2621440
        self.codes = [self.left, self.right, self.down, self.up]
        self.vec = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def run(self):
        code = cv2.waitKeyEx(delay=100)
        for iCode, keyCode in enumerate(self.codes):
            if keyCode == code:
                return self.vec[iCode]
        return (0., 0.)
        
        
        
class Pipeline():
    def __init__(self, steps):
        self.steps = steps
    
    def run(self, val):
        for step in self.steps:
            f = step['f']
            args = step['args']
            kwargs = step['kwargs']
            
            val = f(val, *args, **kwargs)
        return val
    
class CvCam(object):
    def __init__(self, image_w=160, image_h=120, image_d=3, iCam=0):

        self.frame = None
        self.cap = cv2.VideoCapture(iCam)
        self.running = True
        self.cap.set(3, image_w)
        self.cap.set(4, image_h)

    def poll(self):
        if self.cap.isOpened():
            ret, self.frame = self.cap.read()

    def update(self):
        '''
        poll the camera for a frame
        '''
        while(self.running):
            self.poll()

    def run_threaded(self):
        return self.frame

    def run(self):
        self.poll()
        return self.frame

    def shutdown(self):
        self.running = False
        time.sleep(0.2)
        self.cap.release()


class CvImageView(object):

    def run(self, image):
        if image is None:
            return
        try:
            cv2.imshow('frame', image)
            cv2.waitKey(1)
        except:
            pass

    def shutdown(self):
        cv2.destroyAllWindows()

class PlaneDetect():

    def __init__(self, params='not_defined', debug=False):
        self.planes = []
        self.normal_map = None
        if params == 'not_defined':
            Param = namedtuple('Param', ['normalResolution', 'planeMinArea'])
            self.params = Param(3, 0.0120)

        self.debug = debug
    def get_normal_map(self):
        return self.normal_map

    def detect_plane_helper(self, xyz_map, normal_map):
        R, C = xyz_map.rows, xyz_map.cols
        N = R * C
        flood_fill_map = cv2.CreateMat(R, C, cv2.CV_8U)
        for r in range(R):
            for c in range(C):
                z = flood_fill_map[r, c][2]
                flood_fill_map[r, c][2] = 255 if z > 0 else 0
            visPtr = flood_fill_map
        
        compId = -1
        
        allIndices = []
        planePointsIJ = []
        planePointsXYZ = []
        planeEquation = []

        subplane_min_points = self.params.subplaneMinPoints * N /  (self.params.normalResolution ** 2)
        plane_min_points = self.params.planeMinPoints * N /  (self.params.normalResolution ** 2)
        subplane_min_inliers = self.params.planeEquationMinInliers * N /  (self.params.normalResolution ** 2)

        return output_equations, output_points, output_points_xyz

    def detect(self, image):
        self.planes = []
        equations, points, pointsXYZ = [], [], []

        compute_normal_map(image, self.normal_map, 8, self.params.normalResolution, False)
        equations, points, pointsXYZ = self.detect_plane_helper(image, self.normal_map)

        for i in range(len(equations)):
            plane = FramePlane(equations[i], points[i], pointsXYZ[i], image, self.params)

            if (plane.getSurfArea() > self.params.planeMinArea) {
                planes.append(plane)
            }
        }
        self.planes.sort(key=lambda x: x.getPoints().size(), reverse = False)

    def run(self, img_arr):
        return cv2.Canny(img_arr, 
                         self.low_threshold, 
                         self.high_threshold)

    def shutdown(self):
        pass

class FramePlane():

    def __init__(self):

'''
Author: Tawn Kramer
File: realsense2.py
Date: April 14 2019
Notes: Parts to input data from Intel Realsense 2 cameras
'''
import time
import logging

import numpy as np
import pyrealsense2 as rs

class RS_T265(object):
    '''
    The Intel Realsense T265 camera is a device which uses an imu, twin fisheye cameras,
    and an Movidius chip to do sensor fusion and emit a world space coordinate frame that 
    is remarkably consistent.
    '''

    def __init__(self, image_output=False):
        #Using the image_output will grab two image streams from the fisheye cameras but return only one.
        #This can be a bit much for USB2, but you can try it. Docs recommend USB3 connection for this.
        self.image_output = image_output

        # Declare RealSense pipeline, encapsulating the actual device and sensors
        self.pipe = rs.pipeline()
        cfg = rs.config()
        cfg.enable_stream(rs.stream.pose)

        if self.image_output:
            #right now it's required for both streams to be enabled
            cfg.enable_stream(rs.stream.fisheye, 1) # Left camera
            cfg.enable_stream(rs.stream.fisheye, 2) # Right camera

        # Start streaming with requested config
        self.pipe.start(cfg)
        self.running = True
        
        zero_vec = (0.0, 0.0, 0.0)
        self.pos = zero_vec
        self.vel = zero_vec
        self.acc = zero_vec
        self.img = None

    def poll(self):
        try:
            frames = self.pipe.wait_for_frames()
        except Exception as e:
            logging.error(e)
            return

        if self.image_output:
            #We will just get one image for now.
            # Left fisheye camera frame
            left = frames.get_fisheye_frame(1)
            self.img = np.asanyarray(left.get_data())


        # Fetch pose frame
        pose = frames.get_pose_frame()

        if pose:
            data = pose.get_pose_data()
            self.pos = data.translation
            self.vel = data.velocity
            self.acc = data.acceleration
            logging.debug('realsense pos(%f, %f, %f)' % (self.pos.x, self.pos.y, self.pos.z))

    def update(self):
        while self.running:
            self.poll()

    def run_threaded(self):
        return self.pos, self.vel, self.acc, self.img

    def run(self):
        self.poll()
        return self.run_threaded()

    def shutdown(self):
        self.running = False
        time.sleep(0.1)
        self.pipe.stop()

class RS_D435i(object):
    '''
    Intel RealSense depth camera D435i combines the robust depth sensing capabilities of the D435 with the addition of an inertial measurement unit (IMU).
    ref: https://www.intelrealsense.com/depth-camera-d435i/
    '''

    def __init__(self, image_w=640, image_h=480, image_d=3, image_output=True, framerate=30):
        #Using the image_output will grab two image streams from the fisheye cameras but return only one.
        #This can be a bit much for USB2, but you can try it. Docs recommend USB3 connection for this.
        self.image_output = image_output

        # Declare RealSense pipeline, encapsulating the actual device and sensors
        self.pipe = rs.pipeline()
        cfg = rs.config()
        cfg.enable_stream(rs.stream.gyro)
        cfg.enable_stream(rs.stream.accel)

        if self.image_output:
            cfg.enable_stream(rs.stream.color, image_w, image_h, rs.format.rgb8, framerate) # color camera
            cfg.enable_stream(rs.stream.depth, image_w, image_h, rs.format.z16, framerate) # depth camera

        # Start streaming with requested config
        self.pipe.start(cfg)
        self.running = True

        zero_vec = (0.0, 0.0, 0.0)
        self.gyro = zero_vec
        self.acc = zero_vec
        self.img = None
        self.dimg = None

    def poll(self):
        try:
            frames = self.pipe.wait_for_frames()
        except Exception as e:
            logging.error(e)
            return

        if self.image_output:
            color_frame = frames.get_color_frame()
            depth_frame = frames.get_depth_frame()
            self.img = np.asanyarray(color_frame.get_data())
            self.dimg = np.asanyarray(depth_frame.get_data())

        # Fetch IMU frame
        accel = frames.first_or_default(rs.stream.accel)
        gyro = frames.first_or_default(rs.stream.gyro)
        if accel and gyro:
            self.acc = accel.as_motion_frame().get_motion_data()
            self.gyro = gyro.as_motion_frame().get_motion_data()
            # print('realsense accel(%f, %f, %f)' % (self.acc.x, self.acc.y, self.acc.z))
            # print('realsense gyro(%f, %f, %f)' % (self.gyro.x, self.gyro.y, self.gyro.z))

    def update(self):
        while self.running:
            self.poll()

    def run_threaded(self):
        return self.img, self.dimg, (self.acc, self.gyro)

    def run(self):
        self.poll()
        return self.run_threaded()

    def shutdown(self):
        self.running = False
        time.sleep(0.1)
        self.pipe.stop()

if __name__ == "__main__":
    c = RS_T265()
    while True:
        pos, vel, acc = c.run()
        print(pos)
        time.sleep(0.1)
    c.shutdown()

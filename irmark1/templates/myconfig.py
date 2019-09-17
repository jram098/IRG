# """ 
# My CAR CONFIG 

# This file is read by your car application's manage.py script to change the car
# performance

# If desired, all config overrides can be specified here. 
# The update operation will not touch this file.
# """

# CAMERA
CAMERA_TYPE = "D435i"
IMAGE_W = 640
IMAGE_H = 480
IMAGE_DEPTH = 3         # default RGB=3, make 1 for mono
CAMERA_FRAMERATE = 30
# CSIC camera
PCA9685_I2C_BUSNUM = 1   #None will auto detect, which is fine on the pi. But other platforms should specify the bus num.

# REAR_CAMERA
REAR_CAMERA_TYPE = "CSIC"
REAR_IMAGE_W = 960
REAR_IMAGE_H = 616
REAR_IMAGE_DEPTH = 3
REAR_CAMERA_FRAMERATE = 60

#STEERING parameters for Traxxas 4-Tec chassis
STEERING_CHANNEL = 1            #channel on the 9685 pwm board 0-15
STEERING_LEFT_PWM = 260         #pwm value for full left steering
STEERING_RIGHT_PWM = 500        #pwm value for full right steering


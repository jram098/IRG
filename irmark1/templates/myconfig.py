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

#STEERING parameters for Traxxas 4-Tec chassis
STEERING_CHANNEL = 1            #channel on the 9685 pwm board 0-15
STEERING_LEFT_PWM = 260         #pwm value for full left steering
STEERING_RIGHT_PWM = 500        #pwm value for full right steering

#THROTTLE
THROTTLE_CHANNEL = 0            #channel on the 9685 pwm board 0-15
THROTTLE_FORWARD_PWM = 500      #pwm value for max forward throttle
THROTTLE_STOPPED_PWM = 370      #pwm value for no movement
THROTTLE_REVERSE_PWM = 220      #pwm value for max reverse throttle

import rospy
import cv2 as cv
import numpy as np
import time
from threading import Thread
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from std_msgs.msg import String

rospy.init_node('color')
pub = rospy.Publisher('COLOR', String, queue_size=10)
bridge = CvBridge()

hsv_min_red = np.array((0, 162, 181), np.uint8)
hsv_max_red = np.array((9, 200, 255), np.uint8)

hsv_min_green = np.array((39, 229, 95), np.uint8)
hsv_max_green = np.array((58, 255, 188), np.uint8)

hsv_min_blue = np.array((95, 255, 127), np.uint8)
hsv_max_blue = np.array((109, 255, 253), np.uint8)

def color_red(thresh_red):
        moments_red = cv.moments(thresh_red, 1)
        dM01_r = moments_red['m01']
        dM10_r = moments_red['m10']
        dArea_r = moments_red['m00']

        if dArea_r > 100:
                x = int(dM10_r / dArea_r)
                y = int(dM01_r / dArea_r)
                pub.publish('RED')

def color_green(thresh_green):
        moments_green = cv.moments(thresh_green, 1)
        dM01_g = moments_green['m01']
        dM10_g = moments_green['m10']
        dArea_g = moments_green['m00']

        if dArea_g > 100:
                x = int(dM10_g / dArea_g)
                y = int(dM01_g / dArea_g)
                pub.publish('GREEN')

def color_blue(thresh_blue):
        moments_b = cv.moments(thresh_blue, 1)
        dM01_b = moments_b['m01']
        dM10_b = moments_b['m10']
        dArea_b = moments_b['m00']

        if dArea_b > 100:
                x = int(dM10_b / dArea_b)
                y = int(dM01_b / dArea_b)
                pub.publish('BLUE')

def image_callback(data):

        cv_image = bridge.imgmsg_to_cv2(data, 'bgr8')
        hsv = cv.cvtColor(cv_image, cv.COLOR_BGR2HSV)

        thresh_red = cv.inRange(hsv, hsv_min_red, hsv_max_red)
        thresh_green = cv.inRange(hsv, hsv_min_green, hsv_max_green)
        thresh_blue = cv.inRange(hsv, hsv_min_blue, hsv_max_blue)

        color_red(thresh_red)
        color_green(thresh_green)
        color_blue(thresh_blue)

image_sub = rospy.Subscriber('main_camera/image_raw', Image, image_callback)

rospy.spin()

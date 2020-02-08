import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2 as cv
import numpy as np
import sys
import time
import pyzbar.pyzbar as pyzbar
from std_msgs.msg import String

rospy.init_node('qr')
pub = rospy.Publisher('QR', String, queue_size=10)
bridge = CvBridge()

def image_callback(data):
    cv_image = bridge.imgmsg_to_cv2(data, 'bgr8')
    time.sleep(1)
    resultQR = False
    inputImage = cv_image
    decodedObjects = pyzbar.decode(inputImage)
    if len(decodedObjects):
        zbarData = decodedObjects[0].data
    else:
        zbarData = ''
    if zbarData:
        resultQR = zbarData

    if resultQR == False:
        return False
    else:
        pub.publish(resultQR.decode("utf-8"))
        return resultQR.decode("utf-8")

image_sub = rospy.Subscriber('main_camera/image_raw', Image, image_callback)

rospy.spin()

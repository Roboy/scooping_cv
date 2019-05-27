#!/usr/bin/env python

import rospy
import math
import cv2
import numpy as np
from std_msgs.msg import String, Float32
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

# This script listens /zed/zed_node/depth/depth_registered
# and calculates the average distance of the closest objects.
# Then, publishes average distance to shy_roboy/nearest_distance.

class ImageConverter:
    def __init__(self):
        # Initialize depth image listener and average distance publisher.
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/zed/zed_node/depth/depth_registered", Image, self.callback)
        self.rgb_sub = rospy.Subscriber("/zed/zed_node/rgb/image_raw_color", Image, self.callback_rgb)
        self.cv_image = []
        self.cv_image_rgb = []
        self.callback_received = False

    def callback(self, data):
        try:
            # Read depth image.
            self.cv_image = self.bridge.imgmsg_to_cv2(data, "32FC1")
            self.callback_received = True
        except CvBridgeError as e:
            print(e)

    def callback(self, data):
        try:
            # Read rgb image.
            self.cv_image_rgb = self.bridge.imgmsg_to_cv2(data, "bgr8")
            self.callback_received = True
        except CvBridgeError as e:
            print(e)


    def get_depth(self):
        height, width = self.cv_image.shape

        h_new = height * 0.3
        w_new = width * 0.3

        # Resize image to process faster.
        resized = cv2.resize(self.cv_image, (int(w_new), int(h_new)), interpolation=cv2.INTER_AREA)

        # Show images.
        cv2.imshow('Resized Image', resized)
        cv2.imshow('Thresholded Image', th)
        cv2.waitKey(1)


def main():
    ic = ImageConverter()

    rospy.init_node('image_converter', anonymous=True)
    rospy.loginfo("Node running.")

    # 30 FPS = 60 Hz
    rate = rospy.Rate(60)

    try:
        while not rospy.is_shutdown():

            if ic.callback_received:
                ic.get_depth()

            rate.sleep()
    except KeyboardInterrupt:
        print "Shutting down"
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()

import numpy as np
import cv2
print("start")
cap = cv2.VideoCapture(0)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
cap.set(cv2.cv.CV_CAP_PROP_FPS, 2)

def get_image():
	retval, im = cap.read()
	return im
	

for i in range (0,100):	
	print "Taking image %d ..." % (i)
	camera_capture = cv2.imwrite("acquire_%d.jpg" % (i), get_image())

import cv2
import numpy as np

def process_image( img, debugname, showwindows ):

    # Convert BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_blue = np.array([20,100,100])
    upper_blue = np.array([30,255,255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(img,img, mask= mask)

    if showwindows:
    	cv2.imshow('img',img)
    	cv2.imshow('mask',mask)
    	cv2.imshow('res',res) 
    return
  
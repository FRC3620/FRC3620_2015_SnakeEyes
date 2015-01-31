import cv2
import numpy as np

print"some"
def process_image( img, debugname, showwindows ):
    print"start"
    # Convert BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_blue = np.array([20,100,100])
    upper_blue = np.array([30,255,255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(img,img, mask= mask)
    
    kernel5 = np.ones((5,5),np.uint8)
    kernel20 = np.ones((20,20),np.uint8)
    
    open =cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel5)
    
    dilation = cv2.dilate(open,kernel5,iterations = 3)
    
    close =cv2.morphologyEx(open,cv2.MORPH_CLOSE,kernel20)

    # pick which image you want to do contours on (final, close, whatever)
    final = close
    
    # contours morphs source image so we need to use a copy of the image that we are using to get the countour from before using contours
    contour_image = final.copy()
    
    contours, hierarchy = cv2.findContours(contour_image,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	
    c = contours[0]
    print len(c)
    area = cv2.contourArea(c)

    moments = cv2.moments(c)

    yc = moments['m01'] /moments ['m00']
    xc = moments['m10'] /moments ['m00']

    print "Area = ", area
    print "Center of Mass = (",xc, "," , yc,")"
    
    if showwindows:
        cv2.circle(img, (int(xc),int(yc)),10,(0,255,0))
    	cv2.imshow('img',img)
    	cv2.imshow('res',res) 
    	cv2.imshow('open',open)
    	cv2.imshow('close',close)
    	cv2.imshow('dilation',dilation)
    	final = cv2.cvtColor(final, cv2.COLOR_GRAY2BGR)
        cv2.circle(final, (int(xc),int(yc)),10,(0,255,0))
    	cv2.imshow('final',final)

    print "bye"
    return
  
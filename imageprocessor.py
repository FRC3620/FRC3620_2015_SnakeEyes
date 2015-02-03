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
    
    kernel5 = np.ones((5,5),np.uint8)
    kernel20 = np.ones((20,20),np.uint8)
    
    open =cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel5)
    
    # we aren't sure which is better, doing a close or a dilation, so we try both
    # so we can display them both later
    dilation = cv2.dilate(open,kernel5,iterations = 3)
    close =cv2.morphologyEx(open,cv2.MORPH_CLOSE,kernel20)

    # pick which image you want to do contours on (the dilation or the close)
    final = close
    
    # contours morphs source image so we need to use a copy of the image that we are using to get the countour from before using contours
    contour_image = final.copy()
    contours, hierarchy = cv2.findContours (contour_image,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    if(len(contours) != 0):
         c = contours[0]
         #print "Contour length = %d" % (len(c))
         area = cv2.contourArea(c)
         hnum = len(hierarchy[0]-1)
         moments = cv2.moments(c)

         yc = moments['m01'] /moments ['m00']
         xc = moments['m10'] /moments ['m00']

         #print "Area = %d" % (area)
         #print "Center of Mass = %d,%d" % (xc, yc)
    
         #the thin side (the one with fedEx on it) 
         fedEx = 1.35744680851
         #the long side
         team = 2.06593406593
         #the diagonal
         corner = 1.83068783069
    
         for i in range(0, len(contours)):
             cnt = contours[i]
             x,y,w,h = cv2.boundingRect(cnt)
             ratio = float(w)/h
             cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),i+2)
             if ratio >= fedEx - .062 and ratio <= fedEx + .062:
                 print "fedEx, ",i
                 cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),i+2)
             elif ratio >= team - .2 and ratio <= team + .2:
                 print "team, ",i
                 cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),i+2)
             elif ratio >= corner - .9 and ratio <= corner + .9:
                 print "corner, ",i
                 cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),i+2)
             else:
                 cv2.rectangle(img,(x,y), (x+w,y+h),(255,255,255),9)
                 print ratio, " ", i
        

    
    if showwindows:
    	cv2.imshow('img',img)
    	#cv2.imshow('res',res) 
    	#cv2.imshow('open',open)
    	#cv2.imshow('close',close)
        final = cv2.cvtColor(final, cv2.COLOR_GRAY2BGR)
        if len(contours)!=0:
            cv2.circle(final, (int(xc),int(yc)),10,(0,255,0))
            cv2.drawContours (final, contours, -1, (255, 0, 0), 3)
            cv2.imshow('final',final)
        #print hierarchy[0][1]
        #print hierarchy
        #print moments

    return
 
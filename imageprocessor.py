import cv2
import numpy as np


def process_image( img, debugname, showwindows ):
    bestScore = -1
    bestblob = -1
    current = 0
    bestxc = 0
    bestyc = 0
    seen = False
    x= None
    y= None
    w= None
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
         #the thin side (the one with fedEx on it) 
         fedEx = 1.35744680851
         #the long side
         team = 2.06593406593
         #the diagonal
         corner = 1.83068783069
         
         
         
         for i in range(0, len(contours)-1):

             c = contours[i]

             
             area = cv2.contourArea(c)
             moments = cv2.moments(c)

             yc = moments['m01'] /moments ['m00']
             xc = moments['m10'] /moments ['m00']
             if area < 11000:
                 continue
             print i
             print "Contour length = %d" % (len(c))
             print "Area = %d" % (area)
             print "Center of Mass = %d,%d" % (xc, yc)
             
             x,y,w,h = cv2.boundingRect(c)
             ratio = float(w)/h
             
             if ratio >= fedEx - .062 and ratio <= fedEx + .062:
                 print "fedEx, ",i
                 cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),i+2)
                 cv2.putText(img,str(i),(x+w/2,y+h/2),cv2.FONT_HERSHEY_SIMPLEX,.5, (0,0,0),2)
                 current = 2*ratio + int(area/1000)
                 
             elif ratio >= team - .2 and ratio <= team + .2:
                 print "team, ",i
                 cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),i+2)
                 
                 cv2.putText(img,str(i),(x+w/2,y+h/2),cv2.FONT_HERSHEY_SIMPLEX,.5, (0,0,0),2)
                 current = 2*ratio + int(area/1000)
             elif ratio >= corner - .9 and ratio <= corner + .9:
                 print "corner, ",i
                 cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),i+2) 
                 cv2.putText(img,str(i),(x+w/2,y+h/2),cv2.FONT_HERSHEY_SIMPLEX,.5, (0,0,0),2)
                 current = 1.5*ratio + int(area/1000)
             else:
                 cv2.rectangle(img,(x,y), (x+w,y+h),(255,255,255),9)
                 print ratio, " ", i
                 cv2.putText(img,str(i),(x+w/2,y+h/2),cv2.FONT_HERSHEY_SIMPLEX,.5, (0,0,0),2)
                 current = ratio + int(area/1000)

             if current > bestScore:
                 bestScore = current
                 bestblob = i
                 seen = True
                 bestxc = xc
                 bestyc = yc
             print "blob ",i," is scored ",current
             print "the best score is ", bestScore," on blob ", bestblob
             

        

    
    if showwindows:
        cv2.putText(img,str(bestblob),(int(bestxc),int(bestyc)),cv2.FONT_HERSHEY_SIMPLEX,.5, (0,255,255),2)
    	cv2.imshow('img',img)
    	#cv2.imshow('res',res) 
    	#cv2.imshow('open',open)
    	#cv2.imshow('close',close)
        final = cv2.cvtColor(final, cv2.COLOR_GRAY2BGR)
        if len(contours)!=0:
            cv2.circle(final, (int(bestxc),int(bestyc)),10,(0,255,0))
            cv2.drawContours (final, contours, -1, (255, 0, 0), 3)
            cv2.drawContours (final, [contours[bestblob]], -1, (255, 255, 0), 3)
            cv2.imshow('final',final)
        #print hierarchy[0][1]
        #print hierarchy
        #print moments
        
    height, width, depth = img.shape
    if seen:
        return { 'ImageX': width, 'ImageY':height, 'X':bestxc, 'Y':bestyc , 'Seen':seen}
    return {'Seen':False}
 
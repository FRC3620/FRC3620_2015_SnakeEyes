import cv2
import numpy as np
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

def process_image( img, hsvDict , markup=0 ):
    global logger

    bestScore = -1
    bestContour = -1
    bestxc = 0
    bestyc = 0
    seen = False
    height, width, depth = img.shape

    images = { }

    if markup:
	marked = img.copy()
        images['marked'] = marked

    # Convert BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # define range of colors in HSV
    lower_limits = np.array([hsvDict.get('hLo'), hsvDict.get('sLo'), hsvDict.get('vLo')])
    upper_limits = np.array([hsvDict.get('hHi'), hsvDict.get('sHi'), hsvDict.get('vHi')])

    # Threshold the HSV image to get what fits in the limits
    mask = cv2.inRange(hsv, lower_limits, upper_limits)
    images['mask'] = mask

    kernel5 = np.ones((5,5),np.uint8)
    kernel20 = np.ones((20,20),np.uint8)
    
    open = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel5)
    close = cv2.morphologyEx(open,cv2.MORPH_CLOSE,kernel20)

    # pick which image you want to do contours on (the dilation or the close)
    final = close
    images['final'] = final
    
    # contours morphs source image so we need to use a copy of the image that we are using to get the countour from before using contours
    contour_image = final.copy()
    contours, hierarchy = cv2.findContours (contour_image,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    #the thin side (the one with fedEx on it) 
    fedEx = 1.35744680851
    #the long side
    team = 2.06593406593
    #the diagonal
    corner = 1.83068783069

    minArea = int(width*height*0.03)

    for i in range(0, len(contours)):
        c = contours[i]
             
        area = cv2.contourArea(c)

        if area >= minArea:

            moments = cv2.moments(c)
            if moments['m00']==0:
                yc = -1
                xc = -1
            else:
                yc = moments['m01'] /moments ['m00']
                xc = moments['m10'] /moments ['m00']

	    if (logger.isEnabledFor(logging.DEBUG)):
		logger.debug ("Contour %d, length = %d, area = %d, center of mass = %d,%d",
		    i, len(c), area, xc, yc)
             
            x,y,w,h = cv2.boundingRect(c)
            ratio = float(w)/h

	    currentScore = 0
             
            if ratio >= fedEx - .062 and ratio <= fedEx + .062:
                currentScore = 2.25*ratio + int(area/1000)

	        if markup:	
		    cv2.rectangle(marked,(x,y),(x+w,y+h),(255,0,0),i+2)
		    cv2.putText(marked,str(i),(x+w/2,y+h/2),cv2.FONT_HERSHEY_SIMPLEX,.5, (0,0,0),2)
                 
            elif ratio >= team - .2 and ratio <= team + .2:
                currentScore = 2*ratio + int(area/1000)

	        if markup:	
                    cv2.rectangle(marked,(x,y),(x+w,y+h),(0,255,0),i+2)
                    cv2.putText(marked,str(i),(x+w/2,y+h/2),cv2.FONT_HERSHEY_SIMPLEX,.5, (0,0,0),2)

	    elif ratio >= corner - .9 and ratio <= corner + .9:
                currentScore = 1.5*ratio + int(area/1000)

		if markup:
		    cv2.rectangle(marked,(x,y),(x+w,y+h),(0,0,255),i+2) 
                    cv2.putText(marked,str(i),(x+w/2,y+h/2),cv2.FONT_HERSHEY_SIMPLEX,.5, (0,0,0),2)

            else:
                currentScore = ratio + int(area/1000)

		if markup:
                    cv2.rectangle(marked,(x,y), (x+w,y+h),(255,255,255),9)
                    cv2.putText(marked,str(i),(x+w/2,y+h/2),cv2.FONT_HERSHEY_SIMPLEX,.5, (0,0,0),2)

            logger.debug ("contour %d is scored %f", i, currentScore)

            if currentScore > bestScore:
                bestScore = currentScore
                bestContour = i
                seen = True
                bestxc = xc
                bestyc = yc

    logger.debug ("the best score is %f on contour %d", bestScore, bestContour)
    
    if markup:
        cv2.putText(marked,str(bestContour),(int(bestxc),int(bestyc)),cv2.FONT_HERSHEY_SIMPLEX,.5, (0,255,255),2)
        if len(contours)!=0:
            finalMarked = cv2.cvtColor(final, cv2.COLOR_GRAY2BGR)
            images['finalMarked'] = finalMarked
            cv2.circle(finalMarked, (int(bestxc),int(bestyc)),10,(0,255,0))
            cv2.drawContours (finalMarked, contours, -1, (255, 0, 0), 3)
            cv2.drawContours (finalMarked, [contours[bestContour]], -1, (255, 255, 0), 3)
    
    if seen:
        r = { 'imageWidth': width, 'imageHeight':height, 'x':bestxc, 'y':bestyc , 'seen':seen, 'dataType':"visionData", 'nContours':len(contours)}
    else:
        r = {'seen':False, 'dataType':"visionData", 'nContours':len(contours)}
    
    return (r, images)

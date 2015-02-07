#!/usr/bin/python
import cv2
import imageprocessor
import socket
import json

UDP_IP = "roborio-3620.local"
UDP_PORT = 3620

sock = None

try:
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
except Exception as foo:
    print type(foo)
    print "Huh, had trouble making the socket"

cap = cv2.VideoCapture(0)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
#cap.set(cv2.cv.CV_CAP_PROP_FPS, 2)

start = open('videoSettings.json','r')
sread = start.read()
initialHSV=json.loads(sread)
start.close()

while(1):

    # Take each frame
    _, frame = cap.read()
    
    cv2.imshow('frame',frame)
    
    #get information aboot the image
    output, images=imageprocessor.process_image (frame,initialHSV, markup=0 )
    
    #convert to JSON
    jsontote = json.dumps(output)
    print jsontote
    
    if sock is not None:
        #send to network
        try:
            pass
            #sock.sendto(jsontote, (UDP_IP, UDP_PORT))
        except Exception as foo:
    	    print type(foo)
	    print "Huh, had trouble making the socket"
    
    k = cv2.waitKey(5) & 0xFF

#clean up
cv2.destroyAllWindows() 

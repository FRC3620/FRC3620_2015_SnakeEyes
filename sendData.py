import numpy as np
import cv2
import socket
import time as t
import json

start = t.time()
print start

UDP_IP = "localhost"
UDP_PORT = 3620

filename = 'test.avi'
robotmode = 'teleop'
time = '10:42'

joystickx = 0
joysticky = 0
position = 'Red 3'
voltage = '12.42'

sock = None

try:
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
except Exception as foo:
    print type(foo)
    print "Huh, had trouble making the socket"


while True:
    timeinmatch = str(int(t.time()-start))
    data = json.dumps({'filename':filename,'robotmode':robotmode,'time':time,'timeinmatch':timeinmatch,'joystickx':joystickx,'joysticky':joysticky,'position':position,'voltage':voltage})
    if sock is not None:
        try:
            sock.sendto(data,(UDP_IP, UDP_PORT))
            print timeinmatch
            t.sleep(.05)
        except Exception as foo:
    	    print type(foo)
	    print "Huh, had trouble making the socket"
    if int(t.time()-start) == 30:
        filename = 'testChange.avi'
        print filename
    if int(t.time()-start) == 60:
        start = t.time()
        print filename

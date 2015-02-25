import numpy as np
import cv2
import socket

UDP_IP = "localhost"
UDP_PORT = 3620

sock = None

try:
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
except Exception as foo:
    print type(foo)
    print "Huh, had trouble making the socket"


while True:
    if sock is not None:
        try:
            sock.sendto('howdy',(UDP_IP, UDP_PORT))
        except Exception as foo:
    	    print type(foo)
	    print "Huh, had trouble making the socket"
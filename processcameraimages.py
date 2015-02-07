#!/usr/bin/env python

import cv2
import imageprocessor
import socket
import json
import logging
import logging.handlers
import argparse
import sys

###############################################################################
# parse the command line
#

# Define and parse command line arguments
parser = argparse.ArgumentParser(description="My simple Python service")
parser.add_argument("-l", "--log", help="file to write log to")

args = parser.parse_args()

###############################################################################
# set up the logging
#

# Defaults
LOG_LEVEL = logging.DEBUG # Could be e.g. "DEBUG" or "WARNING"
LOG_FORMAT = '%(asctime)s %(name)s %(levelname)-8s %(message)s'

# TODO: add code to set LOG_LEVEL from command line
 
# Make a class we can use to capture stdout and sterr in the log
class MyLogger(object):
    def __init__(self, logger, level):
	"""Needs a logger and a logger level."""
	self.logger = logger
	self.level = level
 
    def write(self, message):
	# Only log if there is a message (not just a new line)
	if message.rstrip() != "":
		self.logger.log(self.level, message.rstrip())

rootLogger = logging.getLogger() 
# Set the log level to LOG_LEVEL
rootLogger.setLevel(LOG_LEVEL)

# Give the logger for this module a unique name (good practice)
logger = logging.getLogger(__name__)

# If the log file is specified on the command line, log to file, and
# redirect stdout and stderr to the log file
if args.log:
    print "logging to " + args.log

    logging.basicConfig(filename=args.log,level=LOG_LEVEL,format=LOG_FORMAT)
    # Replace stdout with logging to file at INFO level
    sys.stdout = MyLogger(logger, logging.INFO)
    # Replace stderr with logging to file at ERROR level
    sys.stderr = MyLogger(logger, logging.ERROR)

else:
    logging.basicConfig(stream=sys.stderr,level=LOG_LEVEL,format=LOG_FORMAT)

rootLogger.info ("message to root")
logger.info ("message to named logger")


###############################################################################
# set up socket
#

UDP_IP = "roborio-3620.local"
UDP_PORT = 3620

sock = None

try:
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
except Exception as foo:
    print type(foo)
    print "Huh, had trouble making the socket"

###############################################################################
# get the vision settings
#
start = open('videoSettings.json','r')
sread = start.read()
videoSettings=json.loads(sread)
start.close()

###############################################################################
# set up the camera
#

cap = cv2.VideoCapture(0)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
#cap.set(cv2.cv.CV_CAP_PROP_FPS, 2)

###############################################################################
# process frame from camera
#

while(1):

    # Take each frame
    _, frame = cap.read()
    
    #cv2.imshow('frame',frame)
    
    #get information aboot the image
    output, images=imageprocessor.process_image (frame,videoSettings, markup=0 )
    
    #convert to JSON
    jsontote = json.dumps(output)
    logger.debug ("JSON: %s", jsontote)
    
    if sock is not None:
        #send to network
        try:
            pass
            #sock.sendto(jsontote, (UDP_IP, UDP_PORT))
        except Exception as foo:
    	    print type(foo)
	    print "Huh, had trouble making the socket"
    
    #k = cv2.waitKey(5) & 0xFF

#clean up
#cv2.destroyAllWindows() 

#!/usr/bin/env python

import numpy as np
import cv2
import time
import socket
import errno
import json
import argparse
import logging
import sys
import math

##DEBUG VARIABLES##
count = 0
startFrame = time.time()
###################
start = time.time()
UDP_IP = "0.0.0.0"
UDP_PORT = 3620
fail = 0
sock = None
y_offset = 0
x_offset = 0
oldfile = None
filename = None
tFromLast = 0
out = None

margin = 20
imgWidth = 320
imgHeight = 240
bgHeight = imgHeight + margin
bgWidth = imgWidth



###############################################################################
# parse the command line
#

# Define and parse command line arguments
parser = argparse.ArgumentParser(description="My simple Python service")
parser.add_argument("-l", "--log", help="file to write log to")
parser.add_argument("-s", "--screen", help="see screen", action = 'store_true')
parser.add_argument("-f", "--framerate", help="run line to find frame rate", action = 'store_true')
parser.add_argument("-o", "--output", help="Toggles the data display off", action = 'store_true')

args = parser.parse_args()
###############################################################################
# set up the logging
#

# Defaults
LOG_LEVEL = logging.INFO # Could be e.g. "DEBUG" or "WARNING"
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

#rootLogger.info ("message to root")
#logger.info ("message to named logger")
############################################################################

logger.info('making socket connection')
try:
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT))
    sock.setblocking(False)
except Exception as foo:
    logger.info(type(foo))
    logger.info("Huh, had trouble making the socket")
logger.info ('done making socket connection')
##############################################################################
if args.output:
    bsHeight = imgHeight
    logger.info("{},{}".format(bsHeight,imgHeight))
##############################################################################
#When can we get a compotent text editor
cap = cv2.VideoCapture(0)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, imgWidth)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, imgHeight)
fourcc = cv2.cv.CV_FOURCC(*'XVID')
##############################################################################
try:
    while(cap.isOpened()):
        msg = None
        data = None
        #Reading Data
        while True:
            try:
                msg, addr = sock.recvfrom(512) # buffer size is 1024
                tFromLast = time.time()
                if args.log:
                   logger.debug(msg)
            except socket.error, e:
                #DEBUG logger.info("found socket error %s"%e)
                err = e.args[0]
                if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                    if time.time()-tFromLast > 10:
                        stringToPrint="Been a long time sense home called..."
                        #DEBUG print stringToPrint
                        msg = None
                        if filename is not None:
                            logger.info(stringToPrint)
                        
                        filename = None
                else:
                    logger.info(e)
                break
        #DEBUG print msg
        if msg is not None:
            data= json.loads(msg)
            stringToPrintTime = "{time:.1f}, {tim} sec,".format(tim= int(time.time()-start),time=data['timeinmatch'])
            stringToPrint2 ="team {team}, {volt:.1f} volts, {mode}".format(team=data['position'],volt=(data['voltage']), mode = data['robotmode'])
            try:
                filename = data['filename']
            except KeyError:
                filename = None
            try:
                pt2 = (int(30*data['joystickx']+(bgWidth-40)),int(30*data['joysticky']+(bgHeight-50)))
            except KeyError:
                pt2 = (bgWidth-40,bgHeight-50)
           
        #Changing files 
        #DEBUG logger.info("filename {}, oldfile {}, out {}".format(filename,oldfile,out))
        if filename != oldfile:
            if out is not None:
                out.release()
                logger.info ('file %s is closing'%filename)
            out = None
            
        oldfile = filename
        
        #We don't have a file open but we want one
        if filename is not None and out is None:
            out = cv2.VideoWriter(filename,fourcc,20,(bgWidth,bgHeight))
            logger.info("file changed to {}".format(filename))
            start = time.time()
    
        
        
        if out is not None:
            ret, frame = cap.read()
            
            if ret == True: 
                if args.output:
                    img1 = frame
                else:
                    img1 = np.zeros((bgHeight,bgWidth, 3), np.uint8)
                    img2 = frame
                    h,w,d = img2.shape
                    img1[y_offset:y_offset+h, x_offset:x_offset+w] = img2
                    cv2.putText(img1,stringToPrintTime,(3,bgHeight-14),2,.35,(255,255,255))
                    cv2.putText(img1,stringToPrint2,(3,bgHeight-2),2,.35,(255,255,255))
                    cv2.rectangle(img1,(bgWidth - 70, bgHeight-20),(bgWidth-10,bgHeight-80),(0,0,0))
                    cv2.line(img1,(bgWidth-40,bgHeight-50),pt2,(255,255,0))
                if args.screen:
                    cv2.imshow('res', img1)
                out.write(img1)
        if cv2.waitKey(1)& 0xFF == ord('q'):
            break
        
        if args.framerate:
            count += 1
            if time.time()-startFrame >= 10:
                startFrame = time.time()
                logger.info(count)
                count = 0
            logger.info(time.time()-startFrame)
except KeyboardInterrupt:
    pass
#cleanup
cap.release()
if out is not None:
    out.release()

###################################################################################
if args.screen:
    cv2.destroyAllWindows()

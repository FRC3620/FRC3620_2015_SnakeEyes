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


###############################################################################
# parse the command line
#

# Define and parse command line arguments
parser = argparse.ArgumentParser(description="My simple Python service")
parser.add_argument("-l", "--log", help="file to write log to")
parser.add_argument("-s", "--screen", help="see screen")

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
#When can we get a compotent text editor
cap = cv2.VideoCapture(0)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
fourcc = cv2.cv.CV_FOURCC(*'XVID')
##############################################################################
try:
    while(cap.isOpened()):

        #Reading Data
        try:
            data, addr = sock.recvfrom(1024) # buffer size is 1024
            data= json.loads(data)
            stringToPrint = "{time} match, {tim} sec,\n team {team}, {volt} volts".format(time=data['time'],tim=data['timeinmatch'],team=data['position'],volt=data['voltage'])
            tFromLast = time.time()
            try:
                filename = data['filename']
            except KeyError:
                filename = None
            try:
                pt2 = (int(30*data['joystickx']+280),int(30*data['joysticky']+210))
            except KeyError:
                pt2 = (280,210)
        except socket.error, e:
            err = e.args[0]
            if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                if time.time()-tFromLast > 10:
                    stringToPrint="Been a long time sense home called..."
                    if filename is not None:
                        logger.info(stringToPrint)
                    filename = None
            else:
                logger.info(e)
        
           
        #Changing files 
        #DEBUG logger.info("filename {}, oldfile {}, out {}".format(filename,oldfile,out))
        if filename != oldfile:
            if out is not None:
                out.release()
                logger.info ('file closing')
            out = None
            
        oldfile = filename
        
        #We don't have a file open but we want one
        if filename is not None and out is None:
            out = cv2.VideoWriter(filename,fourcc,17,(320,260))
            logger.info("file changed to {}".format(filename))
            start = time.time()
    
        
        
        if out is not None:
            ret, frame = cap.read()
            
            if ret == True: 
                img1 = np.zeros((260,320, 3), np.uint8)
                img2 = frame
                h,w,d = img2.shape
                img1[y_offset:y_offset+h, x_offset:x_offset+w] = img2
                cv2.putText(img1,stringToPrint,(3,245),2,.35,(255,255,255))
                cv2.putText(img1,str(int(time.time()-start)),(0,12),2,.5,(0,0,0))
                cv2.rectangle(img1,(250,240),(310,180),(0,0,0))
                cv2.line(img1,(280,210),pt2,(0,0,0))
                if args.screen:
                    cv2.imshow('res', img1)
                out.write(img1)
        if cv2.waitKey(1)& 0xFF == ord('q'):
           break
except KeyboardInterrupt:
    pass
#cleanup
cap.release()
if out is not None:
    out.release()

###################################################################################
if args.screen:
    cv2.destroyAllWindows()

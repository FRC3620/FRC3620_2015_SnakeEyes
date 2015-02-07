#!/usr/bin/env python2

import cv2
import imageprocessor
import numpy as np
import argparse
import json
import time
import logging
import sys

parser = argparse.ArgumentParser()
parser.add_argument("file")
args = parser.parse_args()

###############################################################################
# set up logging
LOG_LEVEL = logging.DEBUG
LOG_FORMAT = '%(levelname)-8s %(message)s'

# Give the logger a unique name (good practice)
logger = logging.getLogger(__name__)
# Set the log level to LOG_LEVEL
logger.setLevel(LOG_LEVEL)

logging.basicConfig(stream=sys.stderr,level=LOG_LEVEL,format=LOG_FORMAT)

###############################################################################
# read file
#

logger.info ("Processing file %s", args.file)
im = cv2.imread(args.file)

currentHSV={}


###############################################################################
# a 'do nothing' onChange handler
#

def nothing(x):
    pass

###############################################################################
# the onChange handler for the 'save' slider
#

def writeFile(s):
    if s == 1:
        print 'Saving...'
        
        with open('videoSettings.json','w') as outfile:
            print currentHSV
            json.dump(currentHSV, outfile)
        print "...Done"
    cv2.setTrackbarPos('Save','image',0)
    
###############################################################################
# the onChange handler for the 'reset' slider
#

def reset(r):
    if r==1:
        cv2.setTrackbarPos('hLo','image',initialHSV.get('hLo'))
        cv2.setTrackbarPos('hHi','image',initialHSV.get('hHi'))
        cv2.setTrackbarPos('sLo','image',initialHSV.get('sLo'))
        cv2.setTrackbarPos('sHi','image',initialHSV.get('sHi'))
        cv2.setTrackbarPos('vLo','image',initialHSV.get('vLo'))
        cv2.setTrackbarPos('vHi','image',initialHSV.get('vHi'))
        writeFile(1)
    cv2.setTrackbarPos('Reset and Save','image',0)

###############################################################################
# the onChange handler for the settings sliders
#

def process(o):

    # get current positions of six trackbars
    hLo = cv2.getTrackbarPos('hLo','image')
    hHi = cv2.getTrackbarPos('hHi','image')
    sLo = cv2.getTrackbarPos('sLo','image')
    sHi = cv2.getTrackbarPos('sHi','image')
    vLo = cv2.getTrackbarPos('vLo','image')
    vHi = cv2.getTrackbarPos('vHi','image')
    global currentHSV
    currentHSV = {'hLo': hLo, 'hHi': hHi, 'sLo': sLo, 'sHi': sHi, 'vLo': vLo, 'vHi': vHi}
    
    # get imformation about the image
    output, images = imageprocessor.process_image( im, currentHSV, markup=1 )
    logger.info("output = %s", output)
    cv2.imshow('image',im)

    for n, img in images.iteritems():
	cv2.imshow(n, img)

###############################################################################
# read processing here

# Create a black image, a window
cv2.namedWindow('image')

# get the settings
start = open('videoSettings.json','r')
sread = start.read()
initialHSV=json.loads(sread)
currentHSV= initialHSV.copy()
start.close()

# create trackbars for color change
cv2.createTrackbar('hLo','image',initialHSV.get('hLo'),255,process)
cv2.createTrackbar('hHi','image',initialHSV.get('hHi'),255,process)
cv2.createTrackbar('sLo','image',initialHSV.get('sLo'),255,process)
cv2.createTrackbar('sHi','image',initialHSV.get('sHi'),255,process)
cv2.createTrackbar('vLo','image',initialHSV.get('vLo'),255,process)
cv2.createTrackbar('vHi','image',initialHSV.get('vHi'),255,process)
cv2.createTrackbar('Save','image',0,1,writeFile)
cv2.createTrackbar('Reset and Save','image',0,1,reset)

# process 
process(0)

while(1):

    k = cv2.waitKey(200) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()

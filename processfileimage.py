#!/usr/bin/env python2

import cv2
import imageprocessor
import json
import argparse
import logging
import sys

parser = argparse.ArgumentParser()
parser.add_argument("file")
args = parser.parse_args()

###############################################################################
# set up logging
LOG_LEVEL = logging.DEBUG
LOG_FORMAT = '%(asctime)s %(levelname)-8s %(message)s'

# Give the logger a unique name (good practice)
logger = logging.getLogger(__name__)
# Set the log level to LOG_LEVEL
logger.setLevel(LOG_LEVEL)

logging.basicConfig(stream=sys.stderr,level=LOG_LEVEL,format=LOG_FORMAT)

###############################################################################
# get the vision settings
#

start = open('videoSettings.json','r')
sread = start.read()
videoSettings=json.loads(sread)
start.close()

###############################################################################
# read the file
#

print "Processing file %s", args.file
im = cv2.imread(args.file)

# process the image
output, images = imageprocessor.process_image( im, videoSettings, markup=1 )
print output

for n, img in images.iteritems():
	cv2.imshow(n, img)

# wait for a key
k = cv2.waitKey()

# clean up
cv2.destroyAllWindows()

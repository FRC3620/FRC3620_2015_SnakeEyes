#!/usr/bin/env python2

import cv2
import imageprocessor

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file")
args = parser.parse_args()

print "Processing file %s", args.file

im = cv2.imread(args.file)
#im = cv2.imread('tote.jpg')
#im = cv2.imread('3620s.jpg')
#im = cv2.imread('corner.jpg')

# get imformation about the image
output, images = imageprocessor.process_image( im, hLo=20, hHi=50, sLo=100, sHi=255, vLo=100, vHi=255, markup=1 )
print output

for n, img in images.iteritems():
	cv2.imshow(n, img)

# wait for a key
k = cv2.waitKey()

# clean up
cv2.destroyAllWindows()

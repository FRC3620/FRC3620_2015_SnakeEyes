import cv2
import imageprocessor

im = cv2.imread('acquire_14.jpg')
#im = cv2.imread('tote.jpg')
#im = cv2.imread('3620s.jpg')
#im = cv2.imread('corner.jpg')
output=imageprocessor.process_image( im, 'dummy', 1 )
print output
k = cv2.waitKey()

cv2.destroyAllWindows()
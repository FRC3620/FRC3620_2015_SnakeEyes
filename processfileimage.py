import cv2
import imageprocessor

im = cv2.imread('tote.jpg')
imageprocessor.process_image( im, 'dummy', 1 )

k = cv2.waitKey()

cv2.destroyAllWindows()
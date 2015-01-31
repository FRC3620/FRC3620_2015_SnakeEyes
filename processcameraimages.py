import cv2
import imageprocessor
    
# here is our main program

cap = cv2.VideoCapture(0)

while(1):

    # Take each frame
    _, frame = cap.read()
    imageprocessor.process_image (frame, 'dummy', 1)
    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows() 
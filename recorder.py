import numpy as np
import cv2
import time

cap = cv2.VideoCapture(0)
fourcc = cv2.cv.CV_FOURCC(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 10, (640,500))

#img1 = cv2.imread('blank.png')
img1 = np.zeros((500,640, 3), np.uint8)
y_offset = 0
x_offset = 0
count = 0
start = time.time()
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
         img2 = frame
         h,w,d = img2.shape
        
         img1[y_offset:y_offset+h, x_offset:x_offset+w] = img2
         #rows,cols,channels = img2.shape
         #roi = img1[0:rows, 0:cols ]
         
         #img1gray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
	 #ret, mask = cv2.threshold(img1gray,10,255, cv2.THRESH_BINARY)
	 #mask_inv = cv2.bitwise_not(mask)

         #img1_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)
         #img2_fg = cv2.bitwise_and(img2,img2,mask = mask)
         
         #dst = cv2.add(img2_fg,img1_bg)
         #img1[0:rows, 0:cols ] = dst
         
         #cv2.imshow('res', img1)
             
         out.write(img1)

         if cv2.waitKey(1)& 0xFF == ord('q'):
              break
         if count == 250:
              break
              
         count = count +1
    else:
         break

cap.release()
out.release()
print time.time() - start
cv2.destroyAllWindows()
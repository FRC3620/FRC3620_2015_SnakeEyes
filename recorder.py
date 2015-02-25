import numpy as np
import cv2
import time
import socket
import errno

start = time.time()
UDP_IP = "0.0.0.0"
UDP_PORT = 3620
fail = 0
sock = None
print 'making socket connection'
try:
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT))
    sock.setblocking(False)
except Exception as foo:
    print type(foo)
    print "Huh, had trouble making the socket"
print 'done making socket connection'
cap = cv2.VideoCapture(0)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
fourcc = cv2.cv.CV_FOURCC(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 17, (320,260))


y_offset = 0
x_offset = 0
count = 0

while(cap.isOpened()):
    
    img1 = np.zeros((260,320, 3), np.uint8)
    ret, frame = cap.read()
    if sock is not None:
        #send to network
        try:
            
            data, addr = sock.recvfrom(256) # buffer size is 256 bytes
        except socket.error, e:
            err = e.args[0]
            if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                data="No socket @ t=", time.time()-start
                print data
            else:
                print e
        else:
            print data
    if ret == True:
        img2 = frame
        h,w,d = img2.shape
        img1[y_offset:y_offset+h, x_offset:x_offset+w] = img2
        cv2.putText(img1,(str(data) +' '+str(time.time()-start)),(0+3,250),2,.35,(255,255,255))
        cv2.imshow('res', img1)
         
        out.write(img1)
        
        if cv2.waitKey(1)& 0xFF == ord('q'):
             break
        #if time.time()-start > 1:
             #break
        #count = count +1
    else:
        break

cap.release()
out.release()
#print time.time() - start
#print count
cv2.destroyAllWindows()
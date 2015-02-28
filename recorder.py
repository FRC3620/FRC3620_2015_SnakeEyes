import numpy as np
import cv2
import time
import socket
import errno
import json

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
##############################################################################
#When can we get a compotent text editor
cap = cv2.VideoCapture(0)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
fourcc = cv2.cv.CV_FOURCC(*'XVID')
##############################################################################
while(cap.isOpened()):

    #Reading Data
    try:
        data, addr = sock.recvfrom(256) # buffer size is 256 by
        data= json.loads(data)
        stringToPrint = "{time} match, {tim} sec, team {team}, {volt} volts".format(time=data['time'],tim=data['timeinmatch'],team=data['position'],volt=data['voltage'])
        tFromLast = time.time()
        filename = data['filename']
    except socket.error, e:
        err = e.args[0]
        if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
            if time.time()-tFromLast > 10:
                stringToPrint="Been a long time sense home called..."
                if filename is not None:
                    print stringToPrint
                filename = None
        else:
            print e
            
    #Changing files 
    #DEBUG print "filename {}, oldfile {}, out {}".format(filename,oldfile,out)    
    if filename != oldfile:
        if out is not None:
            out.release()
            print 'file closing'
        out = None
        
    oldfile = filename
    
    #We don't have a file open but we want one
    if filename is not None and out is None:
        out = cv2.VideoWriter(filename,fourcc,17,(320,260))
        print "file changed to {}".format(filename)

        
    if out is not None:
        ret, frame = cap.read()
        
        if ret == True: 
            img1 = np.zeros((260,320, 3), np.uint8)
            img2 = frame
            h,w,d = img2.shape
            img1[y_offset:y_offset+h, x_offset:x_offset+w] = img2
            cv2.putText(img1,stringToPrint,(0+3,250),2,.35,(255,255,255))
            cv2.imshow('res', img1)
            out.write(img1)
    if cv2.waitKey(1)& 0xFF == ord('q'):
       break
            
cap.release()
if out is not None:
    out.release()

###################################################################################

cv2.destroyAllWindows()
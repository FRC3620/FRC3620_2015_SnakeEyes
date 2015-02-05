import cv2
import imageprocessor
import socket
import json
    
UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP

cap = cv2.VideoCapture(0)

while(1):

    # Take each frame
    _, frame = cap.read()
    #get information aboot the image
    output=imageprocessor.process_image (frame, 'dummy', 1)
   
    #convert to JSON
    jsontote = json.dumps(output)
    print jsontote
    
    #send to network
    sock.sendto(jsontote, (UDP_IP, UDP_PORT))
    
    k = cv2.waitKey(5) & 0xFF

#clean up
cv2.destroyAllWindows() 

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
    
print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
print "message:", MESSAGE
print output
print jsontote
  



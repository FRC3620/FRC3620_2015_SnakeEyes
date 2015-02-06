import cv2
import imageprocessor
import json
import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP

im = cv2.imread('acquire_14.jpg')
#im = cv2.imread('tote.jpg')
#im = cv2.imread('3620s.jpg')
#im = cv2.imread('corner.jpg')

# get imformation about the image
output=imageprocessor.process_image( im, 'dummy', 1 )
print output

# convert to JSON
jsontote = json.dumps(output)
print jsontote

# send to network
sock.sendto(jsontote, (UDP_IP, UDP_PORT))

# wait for a key
k = cv2.waitKey()

# clean up
cv2.destroyAllWindows()
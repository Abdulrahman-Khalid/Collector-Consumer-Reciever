import cv2
import zmq
import _thread
import base64
import math
import config as CONFIG
import sys
import zmq

receiverSocket = CONFIG.configure_port(
    CONFIG.RECIEVER[0], sys.argv[1], zmq.PULL)
f = open(sys.argv[2], "w")
while True:
    img = receiverSocket.recv()
    f.write("Frame# {}:\nXmin =  {}, Xmax = {},Ymin =  {}, Ymax = {} \n \
            --------------------------------------------------------\n\
                ".format(img["frameNum"], img["Xmin"], img["Xmax"], img["Ymin"], img["Ymax"]))

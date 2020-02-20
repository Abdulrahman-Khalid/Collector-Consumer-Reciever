import cv2
import zmq
import _thread
import base64
import math
import config as CONFIG


def configure_port():
    context = zmq.Context()
    # recieve work
    receiverSocket = context.socket(zmq.PULL)
    receiverSocket.connect("tcp://127.0.0.1:%s" % CONFIG.CONSUMER2_SENDER_PORT)
    return receiverSocket


receiverSocket = configure_port()
f = open(CONFIG.OUTPUT_FILE, "w")
while True:
    img = receiverSocket.recv()
    f.write("Frame# {}:\nXmin =  {}, Xmax = {},Ymin =  {}, Ymax = {} \n \
            --------------------------------------------------------\n\
                ".format(img["frameNum"], img["Xmin"], img["Xmax"], img["Ymin"], img["Ymax"]))

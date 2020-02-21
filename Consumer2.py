import cv2
import zmq
import numpy as np
from skimage.filters import threshold_otsu
from skimage.measure import find_contours
from config import *
import pickle
import sys


def get_contours(frameNum, image):
    bounding_boxes = find_contours(image, 0.8)
    for box in bounding_boxes:
        Xvalues = box[:, 1]
        Yvalues = box[:, 0]
        Xmin = (np.min(Xvalues)).astype(np.uint16)
        Xmax = (np.max(Xvalues)).astype(np.uint16)
        Ymin = (np.min(Yvalues)).astype(np.uint16)
        Ymax = (np.max(Yvalues)).astype(np.uint16)
    return pickle.dumps({"frameNum": frameNum, "Xmin": Xmin, "Xmax": Xmax, "Ymin": Ymin, "Ymax": Ymax})


def msg_to_image(message):
    message = pickle.loads(message)
    frameNum = message["frameNum"]
    image = message["img"]
    return frameNum, image


senderSocket = configure_Publisher(sys.argv[2])
receiverSocket = configure_Replier(sys.argv[1])

while True:
    message = receiverSocket.recv()
    frameNum, image = msg_to_image(message)
    data = get_contours(frameNum, image)
    senderSocket.send(data)

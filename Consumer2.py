import cv2
import zmq
import numpy as np
import _thread
import base64
from skimage.filters import threshold_otsu
from skimage.measure import find_contours
import config as CONFIG
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
    return frameNum, Xmin, Xmax, Ymin, Ymax


def msg_to_image(message):
    message = pickle.loads(message)
    frameNum = message["frameNum"]
    image = message["img"]
    return frameNum, image


def data_to_msg(data):
    frameNum, Xmin, Xmax, Ymin, Ymax = data
    return {"frameNum": frameNum, "Xmin": Xmin, "Xmax": Xmax, "Ymin": Ymin, "Ymax": Ymax}


# Create N threads as follows
try:
    receiverSocket = CONFIG.configure_port(
        CONFIG.SENDER[0], sys.argv[1], zmq.PULL)
    senderSocket = CONFIG.configure_port(
        CONFIG.RECIEVER[0], sys.argv[2], zmq.PUSH)
    while True:
        message = receiverSocket.recv()
        frameNum, image = msg_to_image(message)
        data = get_contours(frameNum, image)
        senderSocket.send_json(data_to_msg(data))

except:
    print("Error: unable to start threading")

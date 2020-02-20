import cv2
import zmq
import numpy as np
import _thread
import base64
from skimage.filters import threshold_otsu
from skimage.measure import find_contours
import config as CONFIG


def configure_port():
    context = zmq.Context()
    # recieve work
    receiverSocket = context.socket(zmq.PULL)
    receiverSocket.connect("tcp://127.0.0.1:%s" % CONFIG.COLLECTOR_SENDER_PORT)
    # send work
    senderSocket = context.socket(zmq.PUSH)
    senderSocket.connect("tcp://127.0.0.1:%s" % CONFIG.CONSUMER2_SENDER_PORT)

    return senderSocket, receiverSocket


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
    frameNum = message["frameNum"]
    image = message["img"]
    image = bytearray(base64.b64decode(image))
    return frameNum, image


def data_to_msg(data):
    frameNum, Xmin, Xmax, Ymin, Ymax = data
    return {"frameNum": frameNum, "Xmin": Xmin, "Xmax": Xmax, "Ymin": Ymin, "Ymax": Ymax}


def thread_function(senderSocket, receiverSocket):
    while True:
        message = receiverSocket.recv()
        frameNum, image = msg_to_image(message)
        data = get_contours(frameNum, image)
        senderSocket.send_json(data_to_msg(data))


# Create N threads as follows
try:
    threadCount = CONFIG.N
    senderSocket, receiverSocket = configure_port()
    while threadCount:
        _thread.start_new_thread(
            thread_function, (senderSocket, receiverSocket))
        threadCount -= 1
except:
    print("Error: unable to start threading")

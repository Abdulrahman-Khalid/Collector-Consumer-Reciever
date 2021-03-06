import cv2
import zmq
import sys
import pickle
import numpy as np
from skimage.filters import threshold_otsu
from skimage.measure import find_contours
import utils


def get_contours(frameNum, image):
    bounding_boxes = find_contours(image, 0.8)
    frame_data = []
    for box in bounding_boxes:
        Xvalues = box[:, 1]
        Yvalues = box[:, 0]
        Xmin = (np.min(Xvalues)).astype(np.uint16)
        Xmax = (np.max(Xvalues)).astype(np.uint16)
        Ymin = (np.min(Yvalues)).astype(np.uint16)
        Ymax = (np.max(Yvalues)).astype(np.uint16)
        frame_data.append({"Xmin": Xmin, "Xmax": Xmax,
                           "Ymin": Ymin, "Ymax": Ymax})
    return pickle.dumps({"frameNum": frameNum, "contours": frame_data})


receiverSocket, receiverContext = utils.configure_port(sys.argv[1], zmq.PULL , "connect")
senderSocket, senderContext = utils.configure_port(sys.argv[2], zmq.PUSH , "connect")

try:
    while True:
        message = receiverSocket.recv()
        frameNum, image = utils.msg_to_image(message)
        data = get_contours(frameNum, image)
        senderSocket.send(data)
except:
    pass
finally:
    receiverSocket.close()
    senderSocket.close()  
    senderContext.destroy()                    
    receiverContext.destroy()                       
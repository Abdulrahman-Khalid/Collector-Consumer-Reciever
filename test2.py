import cv2
import zmq
import pickle
import sys
from skimage.color import rgb2gray
from skimage.filters import threshold_otsu


def configure_port():
    context = zmq.Context()
    # recieve work
    receiverSocket = context.socket(zmq.PULL)
    receiverSocket.connect("tcp://127.0.0.1:%s" % 59375)
    return receiverSocket


def apply_threshold(image):
    grayscale = rgb2gray(image)
    thresh = threshold_otsu(grayscale)
    binary = image <= thresh
    return binary


def msg_to_image(message):
    message = pickle.loads(message)
    frameNum = message["frameNum"]
    image = message["img"]
    return frameNum, image


def image_to_msg(frameNum, frame):
    msgD = {"frameNum": frameNum, "img": frame}
    msg = pickle.dumps(msgD)
    return msg



receiverSocket = configure_port()
count = 0
FramesN = [] 
while True:
    print(count)
    message = receiverSocket.recv()
    count += 1 
    print(count)
    frameNum, image = msg_to_image(message)
    FramesN.append(frameNum)
    binaryImage = apply_threshold(image)
    
    
    
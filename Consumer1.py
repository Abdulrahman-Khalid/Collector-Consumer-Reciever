import cv2
import zmq
import _thread
import base64
from skimage.color import rgb2gray
from skimage.filters import threshold_otsu
import config as CONFIG
import pickle


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


    # Create N threads as follows
try:
    receiverSocket = CONFIG.configure_port(
        CONFIG.SENDER[0], sys.argv[1], zmq.PULL)
    senderSocket = CONFIG.configure_port(
        CONFIG.SENDER[0], sys.argv[2], zmq.PUSH)
    while True:
        message = receiverSocket.recv()
        frameNum, image = msg_to_image(message)
        binaryImage = apply_threshold(image)
        senderSocket.send_json(image_to_msg(frameNum, binaryImage))

except:
    print("Error: unable to start threading")

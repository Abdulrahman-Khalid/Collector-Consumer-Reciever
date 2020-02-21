import cv2
import zmq
import sys
import utils
from skimage.color import rgb2gray
from skimage.filters import threshold_otsu


def apply_threshold(image):
    grayscale = rgb2gray(image)
    thresh = threshold_otsu(grayscale)
    binary = grayscale <= thresh
    return binary


senderSocket = utils.configure_Publisher(sys.argv[2])
receiverSocket = utils.configure_Replier(sys.argv[1])
while True:
    message = receiverSocket.recv()
    frameNum, image = utils.msg_to_image(message)
    binaryImage = apply_threshold(image)
    senderSocket.send(utils.image_to_msg(frameNum, binaryImage))

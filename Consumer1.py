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


receiverSocket, receiverContext = utils.configure_port(sys.argv[1], zmq.PULL, "connect")
senderSocket, senderContext = utils.configure_port(sys.argv[2], zmq.PUSH, "connect")

try:
    while True:
        message = receiverSocket.recv()
        frameNum, image = utils.msg_to_image(message)
        binaryImage = apply_threshold(image)
        senderSocket.send(utils.image_to_msg(frameNum, binaryImage))
except:
    pass
finally:
    receiverSocket.close()
    senderSocket.close()  
    senderContext.destroy()                    
    receiverContext.destroy()                       
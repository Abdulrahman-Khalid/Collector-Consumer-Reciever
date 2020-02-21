import cv2
import zmq
import _thread
import base64
import math
import config as CONFIG
import sys

try:
    receiverSocket = CONFIG.configure_port(
        CONFIG.SENDER[0], sys.argv[1], zmq.PULL)
    senderSocket = CONFIG.configure_port(
        CONFIG.SENDER[0], sys.argv[2], zmq.PUSH)
    while True:
        message = receiverSocket.recv()
        senderSocket.send_json(message)
except:
    print("Error: unable to start threading")

while True:
    pass

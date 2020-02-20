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
    receiverSocket.connect("tcp://127.0.0.1:%s" % CONFIG.CONSUMER1_SENDER_PORT)
    # send work
    senderSocket = context.socket(zmq.PUSH)
    senderSocket.connect("tcp://127.0.0.1:%s" % CONFIG.COLLECTOR_SENDER_PORT)

    return senderSocket, receiverSocket


# Define a function for the thread
def thread_function(senderSocket, receiverSocket):
    while True:
        message = receiverSocket.recv()
        senderSocket.send_json(message)


# Create N threads as follows
try:
    threadCount = math.ceil(N / 2)
    senderSocket, receiverSocket = configure_port()
    while threadCount:
        _thread.start_new_thread(
            thread_function, (senderSocket, receiverSocket))
        threadCount -= 1
except:
    print("Error: unable to start threading")

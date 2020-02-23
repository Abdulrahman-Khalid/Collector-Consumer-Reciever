import socket
from contextlib import closing
from math import ceil
import pickle
import zmq


# Functions


def configure_Subscriber(publishers_data):
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    for publisher in publishers_data:
        socket.connect("tcp://" + publisher)
    return socket


def configure_Publisher(publisher):
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    socket.bind("tcp://{}".format(publisher))
    return socket


def configure_Requester(Repliers_data):
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    for Replier in Repliers_data:
        socket.connect("tcp://" + Replier)
    return socket


def configure_Replier(Replier):
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.bind("tcp://" + Replier)
    return socket


def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


def get_ip():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as s:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]


def msg_to_image(message):
    message = pickle.loads(message)
    frameNum = message["frameNum"]
    image = message["img"]
    return frameNum, image


def image_to_msg(frameNum, frame):
    msgD = {"frameNum": frameNum, "img": frame}
    msg = pickle.dumps(msgD)
    return msg


# Constants
N = 4
SENDER = get_ip()
RECIEVER = get_ip()
CONNECTION_PORT = "60175"

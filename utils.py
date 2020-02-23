import socket
from contextlib import closing
from math import ceil
import pickle
import zmq


# Functions

def configure_port(ipPort, portType, connectionType):
    context = zmq.Context()
    socket = context.socket(portType)
    socket.setsockopt( zmq.LINGER,      0 )  # ____POLICY: set upon instantiations
    socket.setsockopt( zmq.AFFINITY,    1 )  # ____POLICY: map upon IO-type thread
    socket.setsockopt( zmq.RCVTIMEO, 2000 )
    if(connectionType == "connect"):
        socket.connect("tcp://" + ipPort)
    else:
        socket.bind("tcp://" + ipPort)
    return socket, context

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
SENDER = "25.94.80.145"
RECIEVER = "25.94.85.0"
CONNECTION_PORT = "60175"

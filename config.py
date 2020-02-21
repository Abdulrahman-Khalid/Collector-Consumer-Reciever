
import socket
from contextlib import closing
from math import ceil
import zmq


def get_ip():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as s:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]


SENDER = ("192.168.1.6", "50041")
RECIEVER = ("192.168.1.6", "36865")


def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


def configure_port(ip, portNum, portType):
    context = zmq.Context()
    socket = context.socket(portType)
    socket.connect("tcp://{}:{}".format(ip, portNum))
    return socket


class ConfigSender:
    def __init__(self, numOfConsumers, videoPath):
        self.N = numOfConsumers
        self.PRODUCER_SENDER_PORT = find_free_port()
        self.CONSUMER1_SENDER_PORT_VEC = []
        self.COLLECTOR_SENDER_PORT_VEC = []
        self.VIDEO_PATH = videoPath
        for _ in range(numOfConsumers):
            self.CONSUMER1_SENDER_PORT_VEC.append(find_free_port())
        for _ in range(ceil(numOfConsumers/2)):
            self.COLLECTOR_SENDER_PORT_VEC.append(find_free_port())


class ConfigReciever:
    def __init__(self, numOfConsumers, outputFilePath):
        self.OUTPUT_FILE = outputFilePath
        self.CONSUMER2_SENDER_PORT_VEC = []
        for _ in range(numOfConsumers):
            self.CONSUMER2_SENDER_PORT_VEC.append(find_free_port())


print("MY IP IS: ", get_ip())
print("Free Port Num: ", find_free_port())

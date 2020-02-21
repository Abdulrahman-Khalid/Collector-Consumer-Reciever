
import socket
from contextlib import closing
from math import ceil
import zmq

PRODUCER_SENDER_PORT = CONSUMER1_RECEIVER_PORT = 59375
CONSUMER1_SENDER_PORT = COLLECTOR_RECEIVER_PORT = 50042
COLLECTOR_SENDER_PORT = CONSUMER2_RECEIVER_PORT = 50043
CONSUMER2_SENDER_PORT = FINAL_COLLECTOR_RECEIVER_PORT = 50044


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
    socket.bind("tcp://"+ Replier)
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

#SENDER = ("192.168.1.6", "50041")
#RECIEVER = ("192.168.1.6", "36865")

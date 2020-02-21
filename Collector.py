import zmq
import sys
from config import *


Publishers = []
for Publisher in sys.argv[1:3]:
    Publishers.append(Publisher)

Repliers = []
for Replier in sys.argv[3:5]:
    Repliers.append(Replier)


receiverSocket = configure_Subscriber(Publishers)
senderSocket = configure_Requester(Repliers)

while True:
    message = receiverSocket.recv()
    senderSocket.send(message)



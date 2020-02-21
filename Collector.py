import zmq
import sys
import utils


Publishers = []
for Publisher in sys.argv[1:3]:
    Publishers.append(Publisher)

Repliers = []
for Replier in sys.argv[3:5]:
    Repliers.append(Replier)


receiverSocket = utils.configure_Subscriber(Publishers)
senderSocket = utils.configure_Requester(Repliers)

while True:
    message = receiverSocket.recv()
    senderSocket.send(message)

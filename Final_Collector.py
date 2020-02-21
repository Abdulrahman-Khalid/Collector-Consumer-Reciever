import zmq
import sys
import pickle
from common_function import *

Publishers = []
for Publisher in sys.argv[2:]:
    Publishers.append(Publisher)

receiverSocket = configure_Subscriber(Publishers)
f = open(sys.argv[1], "w")

while True:
    img = pickle.loads(receiverSocket.recv())
    f.write("Frame# {}:\nXmin =  {}, Xmax = {},Ymin =  {}, Ymax = {} \n".format(
        img["frameNum"], img["Xmin"], img["Xmax"], img["Ymin"], img["Ymax"]))
    f.write("--------------------------------------------------------\n")

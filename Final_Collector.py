import zmq
import sys
import pickle
from common_function import *

Publishers = []
for Publisher in sys.argv[2:]:
    Publishers.append(Publisher)

receiverSocket = configure_Subscriber(Publishers)
f = open(sys.argv[1], "w")

orderNum = 1
dictionaryFrames = {}
while True:
    img = pickle.loads(receiverSocket.recv())
    # To print inorder
    dictionaryFrames[img["frameNum"]] = img
    if(img["frameNum"] == orderNum):
        imgToOut = dictionaryFrames[img["frameNum"]]
        f.write("Frame# {}:\nXmin =  {}, Xmax = {},Ymin =  {}, Ymax = {} \n".format(
            imgToOut["frameNum"], imgToOut["Xmin"], imgToOut["Xmax"], imgToOut["Ymin"], imgToOut["Ymax"]))
        f.write("--------------------------------------------------------\n")
        orderNum += 1

import zmq
import sys
import pickle
import utils
Publishers = []
for Publisher in sys.argv[2:]:
    Publishers.append(Publisher)

receiverSocket = utils.configure_Subscriber(Publishers)

f = open(str(sys.argv[1]), "w")
orderNum = 0
dictionaryFrames = {}
while True:
    frame_data = pickle.loads(receiverSocket.recv())
    # save in dictionary to print in order
    dictionaryFrames[frame_data["frameNum"]] = frame_data
    # print("Frame #{} Recieved".format(frame_data["frameNum"]))
    # To print in order
    if(frame_data["frameNum"] == orderNum):
        imgToOut = dictionaryFrames[orderNum]
        # To print this frame info
        f.write("Frame# {}:\n".format(imgToOut["frameNum"]))
        for idx, contour in enumerate(imgToOut["contours"]):
            f.write("Contour# {}: Xmin =  {}, Xmax = {},Ymin =  {}, Ymax = {} \n".format(
                idx, contour["Xmin"], contour["Xmax"], contour["Ymin"], contour["Ymax"]))
        f.write("--------------------------------------------------------\n")
        orderNum += 1
        # To print existing frames' info that already have been recieved
        while orderNum in dictionaryFrames.keys():
            imgToOut = dictionaryFrames[orderNum]
            f.write("Frame# {}:\n".format(imgToOut["frameNum"]))
            for idx, contour in enumerate(imgToOut["contours"]):
                f.write("Contour# {}: Xmin =  {}, Xmax = {},Ymin =  {}, Ymax = {} \n".format(
                    idx, contour["Xmin"], contour["Xmax"], contour["Ymin"], contour["Ymax"]))
            f.write("--------------------------------------------------------\n")
            orderNum += 1

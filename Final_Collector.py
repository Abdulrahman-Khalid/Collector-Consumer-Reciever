import zmq
import sys
import pickle
import utils


receiverSocket, receiverContext = utils.configure_port(
    str(sys.argv[2]), zmq.PULL, "bind")
frames = {}


def log_contours(frames):
    f = open(str(sys.argv[1]), "w")
    for i in range(len(frames)):
        f.write("Frame#{}: \n".format(i + 1))
        for idx, contour in enumerate(frames[i]):
            f.write("Contour#{}:    Xmin= {}    Xmax= {}    Ymin= {}    Ymax= {}\n".format(
                idx, contour["Xmin"], contour["Xmax"], contour["Ymin"], contour["Ymax"]))
        f.write("--------------------------------------------------------\n")
    f.close()


try:
    while True:
        frame_data = pickle.loads(receiverSocket.recv())
        frames[frame_data["frameNum"]] = frame_data["contours"]
except:
    pass
finally:
    receiverSocket.close()
    receiverContext.destroy()
    log_contours(frames)

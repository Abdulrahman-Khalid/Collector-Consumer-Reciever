import cv2
import zmq
import numpy
import sys
import utils
import pickle
import sys


def video_to_frames(video):
    frames = []
    while(True):
        ret, frame = video.read()
        if ret:
            frames.append(frame)
        else:
            return frames


def read_video_frames(video_path):
    video = cv2.VideoCapture(video_path)   # Read the video
    frames = video_to_frames(video)  # convert it to frames
    video.release()    # Release all space and windows once done
    return frames


def send_images(frames, socket):
    for idx, frame in enumerate(frames):
        socket.send(utils.image_to_msg(idx, frame))

senderSocket, senderContext = utils.configure_port(str(sys.argv[2]), zmq.PUSH, "bind")
frames = read_video_frames(str(sys.argv[1]))
send_images(frames, senderSocket)

senderSocket.close()
senderContext.destroy()

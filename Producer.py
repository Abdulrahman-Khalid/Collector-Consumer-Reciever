import cv2
import zmq
import numpy
import base64
import config as CONFIG
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


def image_to_msg(frameNum, frame):
    msgD = {"frameNum": frameNum, "img": frame}
    msg = pickle.dumps(msgD)
    return msg


def send_images(frames, socket):
    for idx, frame in enumerate(frames):
        socket.send(image_to_msg(idx, frame))


socket = CONFIG.configure_port(CONFIG.SENDER[0], sys.argv[1], zmq.PUSH)
frames = read_video_frames(sys.argv[2])
send_images(frames, socket)

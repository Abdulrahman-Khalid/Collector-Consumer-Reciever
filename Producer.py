import cv2
import zmq
import numpy
import base64
import config as CONFIG
import pickle



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


def configure_port():
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    socket.bind("tcp://127.0.0.1:%s" % CONFIG.PRODUCER_SENDER_PORT)
    return socket


def image_to_msg(frameNum, frame):
    imgToString = base64.b64encode(frame)
    msgD = {"frameNum": frameNum, "img": imgToString}
    msg = pickle.dumps(msgD)
    return msg


def send_images(frames, socket):
    for idx, frame in enumerate(frames):
        socket.send(image_to_msg(idx, frame))


socket = configure_port()
frames = read_video_frames(CONFIG.VIDEO_PATH)
send_images(frames, socket)

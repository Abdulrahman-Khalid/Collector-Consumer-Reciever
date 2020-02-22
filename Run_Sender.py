import sys
import json
from subprocess import Popen
import utils
import pickle
import zmq


def main():
    videoPath = str(sys.argv[1])
    print("Your ip is: {}".format(utils.get_ip()))
    print("Your free port is: {}".format(utils.find_free_port()))
    commands = []
    Consumers1_Receiving_Ports = []
    Consumers1_Sending_Ports = []
    Consumers2_Receiving_Ports = []
    # Recieve from second computer
    try:
        context = zmq.Context()
        socket = context.socket(zmq.PAIR)
        socket.connect(
            "tcp://{}:{}".format(utils.RECIEVER, utils.CONNECTION_PORT))
        Consumers2_Receiving_Ports = pickle.loads(socket.recv())
        print("Port list has been recieved")
    except:
        print("Machine 1 (Sender) ERROR IN Recieving CONNECTION DATA, Try Chaning the CONNECTION_PORT in utils.py file")

    for i in range(utils.N):
        Consumers1_Receiving_Ports.append(
            utils.SENDER + ":" + str(utils.find_free_port()))
        Consumers1_Sending_Ports.append(
            utils.SENDER + ":" + str(utils.find_free_port()))

    #######################################################################################
    Consumers1_Receiving_Ports_string = " ".join(Consumers1_Receiving_Ports)
    commands.append('python Producer.py {} {}'.format(videoPath,
                                                      Consumers1_Receiving_Ports_string))
    #######################################################################################
    for i in range(utils.N):
        commands.append('python Consumer1.py {} {}'.format(
            Consumers1_Receiving_Ports[i], Consumers1_Sending_Ports[i]))
    #######################################################################################
    for i in range(0, utils.N, 2):
        Two_Receiving_Ports = " ".join(Consumers1_Sending_Ports[i: i+2])
        Two_Sending_Ports = " ".join(Consumers2_Receiving_Ports[i: i+2])
        commands.append('python Collector.py {} {}'.format(
            Two_Receiving_Ports, Two_Sending_Ports))
    #######################################################################################
    # run in parallel
    processes = [Popen(cmd, shell=True) for cmd in commands]
    for p in processes:
        p.wait()


if __name__ == '__main__':
    main()

from subprocess import Popen
import utils
import sys
import json
import pickle
import zmq


def main():
    outputPath = str(sys.argv[1])
    print("Your ip is: {}".format(utils.get_ip()))
    print("Your free port is: {}".format(utils.find_free_port()))
    commands = []
    Consumers2_Receiving_Ports = []
    Consumers2_Sending_Ports = []
    for i in range(utils.N):
        Consumers2_Receiving_Ports.append(
            "{}:{}".format(utils.RECIEVER, utils.find_free_port()))
        Consumers2_Sending_Ports.append(
            "{}:{}".format(utils.RECIEVER, utils.find_free_port()))
    ################################################################
    # connect to the SENDER COMPUTER and sends
    try:
        context = zmq.Context()
        socket = context.socket(zmq.PAIR)
        socket.bind("tcp://{}:{}".format(utils.RECIEVER, utils.CONNECTION_PORT))
        data = pickle.dumps(Consumers2_Receiving_Ports)
        socket.send(data)
        print("Port list has been sent")
    except:
        print("Machine 2 (Reciever) ERROR IN SENDING CONNECTION DATA, Try Chaning the CONNECTION_PORT in utils.py file")
    ################################################################
    for i in range(utils.N):
        commands.append('python Consumer2.py {} {}'.format(
            Consumers2_Receiving_Ports[i], Consumers2_Sending_Ports[i]))
    ################################################################
    Consumers2_Sending_Ports_string = " ".join(Consumers2_Sending_Ports)
    commands.append('python Final_Collector.py {} {}'.format(
        outputPath, Consumers2_Sending_Ports_string))
    ################################################################
    # run in parallel
    processes = [Popen(cmd, shell=True) for cmd in commands]
    for p in processes:
        p.wait()


if __name__ == '__main__':
    main()

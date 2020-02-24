from subprocess import Popen
import utils
import sys
import json
import pickle
import zmq
import math


def main():
    outputPath = str(sys.argv[1])
    print("Your ip is: {}".format(utils.get_ip()))

    commands = []
    Collector_Sending_Ports = []

    # Generate needed random free ports
    finalCollectorPort = str(utils.get_ip()) + ":" + \
        str(utils.find_free_port())

    # Recieve Collector Ports from frst computer
    # try:
    ipPortConnecton = str(utils.SENDER) + ":" + utils.CONNECTION_PORT
    recieverSocket, recieverContext = utils.configure_port(
        ipPortConnecton, zmq.PULL, "connect")
    Collector_Sending_Ports = pickle.loads(recieverSocket.recv())
    print("Port has been recieved from the sender's collector")
    # except:
    #     print("Machine 2 (Reciever) ERROR IN RECIVING CONNECTION DATA," +
    #           "Try Chaning the CONNECTION_PORT in utils.py file")

    # Generate needed Processes
    # Generate N Consumers2
    for i in range(utils.N):
        commands.append('python Consumer2.py {} {}'.format(
            Collector_Sending_Ports[int(math.floor(i/2))], finalCollectorPort))

    # Generate Final Collector
    commands.append('python Final_Collector.py {} {}'.format(
        outputPath, finalCollectorPort))

    # Run in parallel
    processes = [Popen(cmd, shell=True) for cmd in commands]
    for p in processes:
        p.wait()

    recieverSocket.close()
    recieverContext.destroy()


if __name__ == '__main__':
    main()

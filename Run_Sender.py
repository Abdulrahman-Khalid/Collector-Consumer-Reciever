import sys
import json
from subprocess import Popen
import utils
import pickle
import zmq
import math


def main():
    videoPath = str(sys.argv[1])
    print("Your ip is: {}".format(utils.get_ip()))
  
    commands = []
    Collector_Receiving_Ports = []
    Collector_Sending_Ports = []

    # Generate needed random free ports
    producerPort = str(utils.get_ip()) + ":" + str(utils.find_free_port())
    for i in range(math.ceil(utils.N / 2)):
        Collector_Receiving_Ports.append(
            str(utils.get_ip()) + ":" + str(utils.find_free_port()))
        Collector_Sending_Ports.append(
            str(utils.get_ip()) + ":" + str(utils.find_free_port()))

    
    # Send Collector Ports to second computer
    try:
        ipPortConnecton = str(utils.RECIEVER) + ":" + utils.CONNECTION_PORT
        senderSocket, senderContext = utils.configure_port(ipPortConnecton, zmq.PUSH, "bind")
        data = pickle.dumps(Collector_Sending_Ports)
        senderSocket.send(data)
    except:
        print("Machine 1 (Sender) ERROR IN SENDING CONNECTION DATA, " +
            "Try Chaning the CONNECTION_PORT in utils.py file")


    # Generate needed Processes
     # Generate Producer
    commands.append('python Producer.py {} {}'.format(videoPath, producerPort))

    # Generate N Consumers1
    for i in range(utils.N):
        commands.append('python Consumer1.py {} {}'.format(producerPort, Collector_Receiving_Ports[math.floor(i/2)]))
    
    # Generate N / 2 Collector
    for i in range(math.ceil(utils.N / 2)):
        commands.append('python Collector.py {} {}'.format(
            Collector_Receiving_Ports[i], Collector_Sending_Ports[i]))
    
    
    # Run in parallel
    processes = [Popen(cmd, shell=True) for cmd in commands]
    for p in processes:
        p.wait()

    senderSocket.close()
    senderContext.destroy()


if __name__ == '__main__':
    main()

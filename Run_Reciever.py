from subprocess import Popen
from common_function import *
import sys
import json


# Arguments #
<<<<<<< HEAD
N = 15
outputFilePath = "./Frames_Data_Output.txt"
#########################
config = CONFIG.ConfigReciever(N, outputFilePath)
#########################
#########################
# TODO: RECIEVE COLLECTOR PORT FROM CONFIG.SENDER
########################
# Set Ports #
CONFIG.SENDER[0], CONFIG.RECIEVER[0]
for port in config.CONSUMER2_SENDER_PORT_VEC:
    # change 24512 to recieved port
    commands.append('python Consumer2.py {} {};'.format(24512, port))
# change 50023 CONSUMER2 SENDER PORT
commands.append('python Final_Collector.py {} {};'.format(
    50023, outputFilePath))
=======
N = int(sys.argv[1])
outputPath = "./" + str(sys.argv[2])

commands = []
Consumers2_Receiving_Ports = []
Consumers2_Sending_Ports = []

for i in range(N):
    Consumers2_Receiving_Ports.append(get_ip() + ":" + str(find_free_port()))
    Consumers2_Sending_Ports.append(get_ip() + ":" + str(find_free_port()))

for i in range(N):
    commands.append('python Consumer2.py {} {}'.format(Consumers2_Receiving_Ports[i], Consumers2_Sending_Ports[i]))

Consumers2_Sending_Ports_string = " ".join(Consumers2_Sending_Ports)
commands.append('python Final_Collector.py {} {}'.format (outputPath ,Consumers2_Sending_Ports_string))

>>>>>>> 6ea478a314ba7055b27365e7edd8e3dcb2643523

# run in parallel
processes = [Popen(cmd, shell=True) for cmd in commands]
for p in processes:
    p.wait()

import sys
import json
from subprocess import Popen
from common_function import *


# Arguments #
N = int(sys.argv[1])
videoPath = "./" + str(sys.argv[2])
outputPath = "./" + str(sys.argv[3])

commands = []
Consumers1_Receiving_Ports = []
Consumers1_Sending_Ports = []

Consumers2_Receiving_Ports = []
Consumers2_Sending_Ports = []

for i in range(N):
    Consumers1_Receiving_Ports.append(get_ip() + ":" + str(find_free_port()))
    Consumers1_Sending_Ports.append(get_ip() + ":" + str(find_free_port()))
    Consumers2_Receiving_Ports.append(get_ip() + ":" + str(find_free_port()))
    Consumers2_Sending_Ports.append(get_ip() + ":" + str(find_free_port()))

#######################################################################################
Consumers1_Receiving_Ports_string = " ".join(Consumers1_Receiving_Ports)
commands.append('python Producer.py {} {}'.format (videoPath ,Consumers1_Receiving_Ports_string))
#######################################################################################
for i in range(N):
    commands.append('python Consumer1.py {} {}'.format(Consumers1_Receiving_Ports[i], Consumers1_Sending_Ports[i]))
#######################################################################################
for i in range(0,N, 2):
    Two_Receiving_Ports = " ".join(Consumers1_Sending_Ports[i: i+2])
    Two_Sending_Ports = " ".join(Consumers2_Receiving_Ports[i: i+2])
    commands.append('python Collector.py {} {}'.format(Two_Receiving_Ports , Two_Sending_Ports))
#######################################################################################
for i in range(N):
    commands.append('python Consumer2.py {} {}'.format(Consumers2_Receiving_Ports[i], Consumers2_Sending_Ports[i]))
#######################################################################################
Consumers2_Sending_Ports_string = " ".join(Consumers2_Sending_Ports)
commands.append('python Final_Collector.py {} {}'.format (outputPath ,Consumers2_Sending_Ports_string))
#######################################################################################

# run in parallel
processes = [Popen(cmd, shell=True) for cmd in commands]
for p in processes:
    p.wait()

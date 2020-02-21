from subprocess import Popen
from common_function import *
import sys
import json


# Arguments #
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


# run in parallel
processes = [Popen(cmd, shell=True) for cmd in commands]
for p in processes:
    p.wait()

from subprocess import Popen
import config as CONFIG
commands = []
# Arguments #
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

# run in parallel
processes = [Popen(cmd, shell=True) for cmd in commands]
# do other things here..
# wait for completion
for p in processes:
    p.wait()

#    'python Consumer2.py;',
#  'python Final_Collector.py;',

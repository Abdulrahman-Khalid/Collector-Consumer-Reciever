from subprocess import Popen
import config as CONFIG
commands = []
# Arguments #
N = 15
videoPath = "./small.mp4"
#########################
config = CONFIG.ConfigSender(N, videoPath)
#########################
# TODO: SEND COLLECTOR PORT TO CONFIG.RECIEVER
########################
# Set Ports #
commands.append('python Producer.py ' + config.PRODUCER_SENDER_PORT + ';')
for port in config.CONSUMER1_SENDER_PORT_VEC:
    commands.append('python Consumer1.py ' +
                    config.PRODUCER_SENDER_PORT + ' ' + port + ';')
for port in config.COLLECTOR_SENDER_PORT_VEC:
    commands.append('python Collector.py ' +
                    "50024" + ' ' + port + ';')  # change 50024 with CONSUMER1 SENDER PORT

# run in parallel
processes = [Popen(cmd, shell=True) for cmd in commands]
# do other things here..
# wait for completion
for p in processes:
    p.wait()

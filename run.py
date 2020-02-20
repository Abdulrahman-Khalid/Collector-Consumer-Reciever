from subprocess import Popen

commands = [
    'python Producer.py;',
    'python Consumer1.py;',
    'python Collector.py;',
    'python Consumer2.py;',
    'python Final_Collector.py;',
]
# run in parallel
processes = [Popen(cmd, shell=True) for cmd in commands]
# do other things here..
# wait for completion
for p in processes:
    p.wait()

from subprocess import Popen

commands = []
commands.append('python test.py')
commands.append('python test2.py 1')
commands.append('python test2.py 2')

processes = [Popen(cmd, shell=True) for cmd in commands]

for p in processes:
    p.wait()

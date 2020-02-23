from subprocess import Popen

commands = ["python Run_Sender.py ./small.mp4;",
            "python Run_Reciever.py Test2.txt"]
            
# run in parallel
processes = [Popen(cmd, shell=True) for cmd in commands]
for p in processes:
    p.wait()

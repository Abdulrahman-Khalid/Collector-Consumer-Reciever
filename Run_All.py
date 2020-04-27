from subprocess import Popen


def main():
    commands = ["python Run_Reciever.py ./output.txt",
                "python Run_Sender.py ./small.mp4"]
    # Run in parallel
    processes = [Popen(cmd, shell=True) for cmd in commands]
    for p in processes:
        p.wait()


if __name__ == '__main__':
    main()

import zmq
import sys
import utils

receiverSocket, receiverContext = utils.configure_port(str(sys.argv[1]), zmq.PULL, "bind")
senderSocket, senderContext = utils.configure_port(str(sys.argv[2]), zmq.PUSH, "bind")

try:
    while True:
        message = receiverSocket.recv()
        senderSocket.send(message)
except:
    pass
finally:
    receiverSocket.close()
    senderSocket.close()  
    senderContext.destroy()                    
    receiverContext.destroy()  
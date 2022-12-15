# Receiver. Block on input from provided serial port, upon recieving an ACK
# notify the sender. Upon receiving printer state, update GUI thread with newly
# read state

class Recver:

    def __init__(self, port, sender_obj):
        self.port = port
        self.sender_obj = sender_obj
        self.killed = 0

    def kill(self):
        self.killed = 1

    def thread(self):
        while not self.killed:
            serial_input = self.port.read()

            if self.killed == 1:
                break
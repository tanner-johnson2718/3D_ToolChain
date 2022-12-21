# Receiver. Block on input from provided serial port, upon recieving an ACK
# notify the sender. Upon receiving printer state, update GUI thread with newly
# read state

import re

class Recver:

    def __init__(self, port, ds):
        self.port = port
        self.killed = 0
        self.ds = ds

    def kill(self):
        self.killed = 1

    def thread(self):
        print("Recver Thread Started")
        while not self.killed:
            serial_input = self.port.readline().decode('ascii')
            if serial_input != "":
                self.ds.push_reponse_line(serial_input)

        print("Recver Thread Killed")
                    
                        
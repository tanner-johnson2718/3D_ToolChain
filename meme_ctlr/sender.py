# Sender thread. Maintains a Q of commands to be sent over a port that provides
# a send function. Provide a file for optional logging of all commands sent.
# Commands to be sent shall be in ascii, text format

import time
import threading

class Sender:

###############################################################################
# Job class holds commands and meta data of a command to be sent.
###############################################################################

    class SendJob:
        def __init__(self, command):
            self.command = command
            self.time_enQed = -1
            self.time_sent = -1
            self.time_ACKed = -1

        def timestamp_enQ(self):
            self.time_enQed = time.time()

        def timestamp_sent(self):
            self.time_sent = time.time()

        def timestamp_ACKed(self):
            self.time_ACKed = time.time()

        def get_csv_report(self):
            return self.command + "," + str(self.timestamp_enQ) + "," + str(self.timestamp_sent) + "," + str(self.timestamp_ACKed) + "\n"

###############################################################################
# Public functions. Called to create, enQ, and ACK commands.
###############################################################################

    def __init__(self, port, log_file):
        self.port = port
        self.log_file = log_file

        self.Q = []
        self.killed = 0
        self.timeout = .5
        self.cv = threading.Condition()
        self.Q_lock = threading.Semaphore(1)

    def enQ(self, command):

        self.Q_lock.acquire()

        self.Q.append(Sender.SendJob(command))
        self.Q[-1].timestamp_enQ()
        self.cv.notify()

        self.Q_lock.release()

    def ACK(self):

        self.Q_lock.acquire()

        if self.Q[0].time_sent < 0:
            print("ERROR in ACK, tried to ACK a command that has not ben sent")
            self.Q_lock.release()
            return

        self.Q[0].timestamp_ACKed()

        self.Q_lock.release()

    def thread(self):
        while not self.killed:

            # Wait on an enQ or an ACK
            self.cv.wait(timeout=self.timeout)
            self.Q_lock.acquire()

            if len(self.Q) == 0:
                print("ERROR in Sender, ACK recieved on empty Q")
                self.Q_lock.release()
                break

            # notified by an enQ
            if self.Q[0].time_sent < 0:
                self.port.write((self.Q[0].command+"\n").encode('ascii'))

            # notified by an ACK
            else:
                
            

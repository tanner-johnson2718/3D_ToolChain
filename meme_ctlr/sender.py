# Sender thread. Maintains a Q of commands to be sent over a port that provides
# a write function. Provide a file for optional logging of all commands sent.
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

        def timestamp_enQ(self, delta):
            self.time_enQed = time.time() - delta

        def timestamp_sent(self, delta):
            self.time_sent = time.time() - delta

        def timestamp_ACKed(self, delta):
            self.time_ACKed = time.time() - delta

        def get_csv_report(self):
            return self.command + "," + str(float(self.time_enQed)) + "," + str(float(self.time_sent)) + "," + str(float(self.time_ACKed)) + "\n"

###############################################################################
# Public functions. Called to create, enQ, and ACK commands.
###############################################################################

    def __init__(self, port, log_file=""):
        self.port = port
        self.log_file = log_file

        self.Q = []
        self.killed = 0
        self.timeout = .5
        self.cv = threading.Condition()
        self.start_time = time.time()
        
        if not log_file == "":
            try:
                self.file_handle = open(self.log_file, "w")
            except Exception as e:
                print("In Sender, failed to open " + str(self.log_file))
                self.file_handle = -1
        else:
            self.file_handle = -1

    def enQ(self, command):

        self.cv.acquire()

        self.Q.append(Sender.SendJob(command))
        self.Q[-1].timestamp_enQ(self.start_time)
        self.cv.notify_all()

        self.cv.release()

    def ACK(self):

        self.cv.acquire()

        if len(self.Q) == 0:
            print("ERROR in ACK(), ACKed empty Q")
            self.cv.release()
            return

        if self.Q[0].time_sent < 0:
            print("ERROR in ACK, tried to ACK a command that has not ben sent")
            self.cv.release()
            return

        self.Q[0].timestamp_ACKed(self.start_time)
        self.cv.notify_all()

        self.cv.release()

    def kill(self):
        self.cv.acquire()
        self.killed = 1
        self.cv.notify_all()
        self.cv.release()

    def thread(self):
        print("Sender Thread Starting")
        while not self.killed:

            # Wait on an enQ or an ACK
            self.cv.acquire()
            wait_ret = self.cv.wait(timeout=self.timeout)

            # print("Send thread awoken")

            if self.killed:
                break

            if wait_ret == False:
                continue

            if len(self.Q) == 0:
                print("ERROR in Sender, ACK recieved on empty Q")
                self.cv.release()
                break

            # notified by an enQ and its ready to be sent
            if self.Q[0].time_sent < 0:
                self.port.write((self.Q[0].command+"\n").encode('ascii'))
                # print("SENT) " + self.Q[0].command)
                self.Q[0].timestamp_sent(self.start_time)

            # notified by an enQ but not ready to be sent
            elif self.Q[0].time_ACKed < 0:
                self.cv.release()
                continue

            # notified by an ACK
            elif (self.Q[0].time_enQed > 0) and (self.Q[0].time_sent > 0) and (self.Q[0].time_ACKed > 0):
                if not self.file_handle == -1:
                    self.file_handle.write(self.Q[0].get_csv_report())

                self.Q.pop(0)

                if len(self.Q) > 0:
                    self.port.write((self.Q[0].command+"\n").encode('ascii'))
                    self.Q[0].timestamp_sent(self.start_time)

            else:
                print("ERROR in Sender thread, SHOULD NOT be HERE!")

            self.cv.release()
        self.file_handle.close()
        print("Sender Thread Killed")
            

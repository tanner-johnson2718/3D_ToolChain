# Holds all state across all threads:
#   -> Send Q and send history (including timestamps and accumulated responses)
#   -> Table mapping gcode commands to reponse structure and most recent parsed
#      response from printer i.e. {"M105", "Nozzle Temp", 154}

# Should also provide the following functionality)
#    -> Periodically write out to disk
#        -> When a flush to disk occurs, empty the Qs
#    -> Provide controlled multithreaded access to data
#    -> Parse responses from serial into state map

# Should be thread safe and completely synchronise. I.e. any thread should
# be able to call any function and it should not change the outcome of
# executing the function. Also no call should spawn any background thread.
# All function calls execute all computation on the thread that called it.
# NOTE) many calls are blocking and will be stuck there. Provide a kill switch
# to wake all threads waiting in functions.

import time
import threading
import re

class DataStore():

###############################################################################
# Define the state map. The state map holds a list of commands that return
# state of the printer. A dictionary maps the key
###############################################################################
    class StateMap():
        def __init__(self):
            self.state = {"nozzle temp current" : 0,
                          "nozzle temp target"  : 0,
                          "bed temp current"    : 0,
                          "bed temp target"     : 0,
                          "X Pos"               : 0,
                          "Y Pos"               : 0,
                          "Z Pos"               : 0,
                          "E Pos"               : 0,
                          "Print Accel"         : 0,
                          "Travel Accel"        : 0,
                          "Retract Accel"       : 0,
                          "SD Progress"         : 0,
                          "SD Total"            : 0}

            self.cmd2key = {"M155" : ["nozzle temp current", "nozzle temp target", "bed temp current", "bed temp target"], 
                            "M154" : ["X Pos","Y Pos","Z Pos","E Pos"],
                            "M27"  : ["SD Progress","SD Total"], 
                            "M204" : ["Print Accel","Retract Accel","Travel Accel"]}

            self.cmd2prefix = {"M155" : "T:", 
                               "M154" : "X:",
                               "M27"  : "SD printing", 
                               "M204" : "M204"}
            self.regex = r"[-+]?(?:\d*\.\d+|\d+)"

    def __init__(self):
        self.kill_switch = 0
        self.start_time = time.time()
        self.sendQ = []                             # List of send job objects
        self.sendQ_cv =  threading.Condition()      # Controls and notifies on sendQ activity
        self.current_sendQ_index = 0
        self.state = DataStore.StateMap()

    def kill(self):
        self.kill_switch = 1

        self.sendQ_cv.acquire()
        self.sendQ_cv.notify_all()
        self.sendQ_cv.release()

###############################################################################
# Send Job class holds commands and meta data of a command to be sent.
###############################################################################

    class SendJob:
        def __init__(self, command):
            self.command = command
            self.time_enQed = -1
            self.time_sent = -1
            self.time_ACKed = -1
            self.responses = []

        def timestamp_enQ(self, delta):
            self.time_enQed = time.time() - delta

        def timestamp_sent(self, delta):
            self.time_sent = time.time() - delta

        def timestamp_ACKed(self, delta):
            self.time_ACKed = time.time() - delta

        def get_csv_report(self):
            return self.command + "," + str(float(self.time_enQed)) + "," + str(float(self.time_sent)) + "," + str(float(self.time_ACKed)) + "\n"

###############################################################################
# Public sendQ access functions
###############################################################################

    def push_cmd(self, gcode):
        self.sendQ_cv.acquire()

        self.sendQ.append(DataStore.SendJob(gcode))
        self.sendQ[-1].timestamp_enQ(self.start_time)
        self.sendQ_cv.notify_all()

        self.sendQ_cv.release()

    def wait_cmd(self):
        while not self.kill_switch:
            self.sendQ_cv.acquire()
            self.sendQ_cv.wait()

            # Check if ready to send. If current job index is pointing to an empty slot or if
            # the current job has already been sent then do not break out of loop and do not return
            if self.is_ready():
                ret = self.sendQ[self.current_sendQ_index].command
                self.sendQ_cv.release()
                return ret

    def push_reponse(self, line):
        
        # Grab CV, append line to response list of current open command
        self.sendQ_cv.acquire()
        if self.is_open():
            self.sendQ[self.current_sendQ_index].responses.append(line)

        # recved an ACK, update timestamp on current send job, inc the index,
        # and notify anyone waiting on sendQ activity
        if line == "ok\n":
            self.sendQ[self.current_sendQ_index].timestamp_ACKed(self.start_time)
            self.advance_Q()     # NOTE!!! SHOULD ONLY BE CALLED HERE WHEN AN ACK IS RECIEVED
            self.sendQ_cv.notify_all()
            self.sendQ_cv.release()
            return
        self.sendQ_cv.release()

        # parse the input and see if it matches any prefixes in the state map
        for cmd_key in self.state.cmd2prefix.keys():
            if line.find(self.state.cmd2prefix[cmd_key]) > -1:
                nums = re.findall(self.state.regex, line)
                for i in range(0, len(self.state.cmd2key[cmd_key])):
                    self.state.state[self.state.cmd2key[cmd_key][i]] = nums[i]
        

###############################################################################
# Public state map access functions
###############################################################################

    def query(self, key):
        if key in self.state.state.keys():
            return self.state.state[key]
        return ""

    def get_all_state_keys(self):
        return self.state.state.keys()

###############################################################################
# Private helper functions. There are 3 important state)
#   1) Closed  -> All send commands are sent and not waiting any input
#   2) Ready   -> 1 or more commands are ready to be sent and not wainting on 
#                 reponse from previous command
#   3) Open    -> A command has been sent and are awaiting on a response
###############################################################################
    def is_open(self):
        ret = (self.current_sendQ_index < len(self.sendQ)) and\
              (self.sendQ[self.current_sendQ_index].time_sent >= 0) and\
              (self.sendQ[self.current_sendQ_index].ACKed < 0)

        return ret

    def is_closed(self):
        return self.current_sendQ_index == len(self.sendQ)

    def is_ready(self):
        ret = (self.current_sendQ_index < len(self.sendQ)) and\
              (self.sendQ[self.current_sendQ_index].time_sent < 0)

        return ret

    def advance_Q(self):
        self.current_sendQ_index += 1
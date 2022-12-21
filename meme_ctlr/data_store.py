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

class DataStore():

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
# Define the state map. Each entry's key is the gcode command that gets
# that data. The second indecies in the table are one of the following)
#    -> prefix      : unique prefix of the response from printer
#    -> description : short text description of command
#    -> regex       : regex to pull relavent data from reponse
#    -> labels      : Text labels of the values returned by command
#    -> values      : numerical values returned by command
#    -> gui         : list of gui elements to be updated 
###############################################################################
    class StateMap():
        def __init__(self):
            self.state_map = {}
            self.state_map["M155 S1"] = {}
            self.state_map["M155 S1"]["prefix"] = "T:"
            self.state_map["M155 S1"]["description"] = "Returns Nozzle and Bed Temp every second."
            self.state_map["M155 S1"]["regex"] = r"[-+]?(?:\d*\.\d+|\d+)"
            self.state_map["M155 S1"]["labels"] = ["Nozzle Current", "Nozzle Target", "Bed Current", "Bed Target"]
            self.state_map["M155 S1"]["values"] = [0,0,0,0]
            self.state_map["M155 S1"]["gui"] = []
            self.state_map["M154 S1"] = {}
            self.state_map["M154 S1"]["prefix"] = "X:"
            self.state_map["M154 S1"]["description"] = "Returns X,Y,Z,E pos every second."
            self.state_map["M154 S1"]["regex"] = r"[-+]?(?:\d*\.\d+|\d+)"
            self.state_map["M154 S1"]["labels"] = ["X Curr", "Y Curr", "Z Curr", "E Curr"]
            self.state_map["M154 S1"]["values"] = [0,0,0,0]
            self.state_map["M154 S1"]["gui"] = []
            self.state_map["M851"] = {}
            self.state_map["M851"]["prefix"] = "M851"
            self.state_map["M851"]["description"] = "Distance from probe to nozzle."
            self.state_map["M851"]["regex"] = r"[-+]?(?:\d*\.\d+|\d+)"
            self.state_map["M851"]["labels"] = ["X Probe Off", "Y Probe Off", "Z Probe Off"]
            self.state_map["M851"]["values"] = [0,0,0]
            self.state_map["M851"]["gui"] = []
            self.state_map["M92"] = {}
            self.state_map["M92"]["prefix"] = "M92"
            self.state_map["M92"]["description"] = "Steps per mm"
            self.state_map["M92"]["regex"] = r"[-+]?(?:\d*\.\d+|\d+)"
            self.state_map["M92"]["labels"] = ["X Steps per mm", "Y  Steps per mm", "Z Steps per mm", "E  Steps per mm"]
            self.state_map["M92"]["values"] = [0,0,0,0]
            self.state_map["M92"]["gui"] = []

    def __init__(self):
        self.kill_switch = 0
        self.start_time = time.time()

        self.sendQ = []                             # List of send job objects
        self.sendQ_cv =  threading.Condition()      # Controls and notifies on sendQ activity
        self.response_cv = threading.Condition()    # Notifys when a response is recved
        self.current_sendQ_index = 0
        self.most_recent_response = ""              # Holds most recent reponse

    def kill(self):
        self.kill_switch = 1

        self.sendQ_cv.acquire()
        self.sendQ_cv.notify_all()
        self.sendQ_cv.release()

        self.response_cv.acquire()
        self.response_cv.notify_all()
        self.response_cv.release()

###############################################################################
# Public sendQ access functions
###############################################################################

    def push_next_send(self, gcode):
        self.sendQ_cv.acquire()

        self.sendQ.append(DataStore.SendJob(gcode))
        self.sendQ[-1].timestamp_enQ(self.start_time)
        self.sendQ_cv.notify_all()

        self.sendQ_cv.release()

    def wait_on_next_to_send(self):
        while not self.kill_switch:
            self.sendQ_cv.acquire()
            self.sendQ_cv.wait()

            # Check if ready to send. If current job index is pointing to an empty slot or if
            # the current job has already been sent then do not break out of loop and do not return
            if self.is_ready():
                ret = self.sendQ[self.current_sendQ_index].command
                self.sendQ_cv.release()
                return ret

    def push_reponse_line(self, line):
        
        # Grab CV, append line to response list of current open command and 
        # notify anyone waiting on response input 
        self.sendQ_cv.acquire()
        if self.is_open():
            self.sendQ[self.current_sendQ_index].responses.append(line)

        self.response_cv.acquire()
        self.most_recent_response = line
        self.response_cv.notify_all()
        self.response_cv.release()

        # recved an ACK, update timestamp on current send job, inc the index,
        # and notify anyone waiting on sendQ activity
        if line == "ok\n":
            self.sendQ[self.current_sendQ_index].timestamp_ACKed(self.start_time)
            self.advance_Q()     # NOTE!!! SHOULD ONLY BE CALLED HERE WHEN AN ACK IS RECIEVED
            self.sendQ_cv.notify_all()
            self.sendQ_cv.release()
            return
        self.sendQ_cv.release()

        # TODO, parse the input and see if it matches any prefixes in the state map

    def wait_on_next_response(self):
        self.response_cv.acquire()
        self.response_cv.wait()
        ret = self.most_recent_response
        self.response_cv.release()
        return ret

    

###############################################################################
# Public state map access functions
###############################################################################

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
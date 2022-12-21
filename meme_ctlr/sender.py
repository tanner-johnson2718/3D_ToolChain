# Sender thread. Simply wait on the data store to notify us that a command
# is ready to be sent and sent it over the 

class Sender:

###############################################################################
# Public functions. Called to create, enQ, and ACK commands. These functions
# are called from another thread.
###############################################################################

    def __init__(self, port, ds):
        self.port = port
        self.killed = 0
        self.ds = ds

    def kill(self):
        self.killed = 1

    def thread(self):
        print("Sender Thread Starting")
        while not self.killed:
            cmd = self.ds.wait_on_next_to_send()
            if (not self.killed) and isinstance(cmd, str):
                self.port.write((cmd+"\n").encode('ascii'))
        print("Sender Thread Killed")
            

# Receiver. Block on input from provided serial port, upon recieving an ACK
# notify the sender. Upon receiving printer state, update GUI thread with newly
# read state

import re

class Recver:

    def __init__(self, port, sender_obj):
        self.port = port
        self.sender_obj = sender_obj
        self.killed = 0

        self.parse_table = {}
        self.parse_table['ACK'] = {}
        self.parse_table['ACK']['prefix'] = "ok"
        self.parse_table['ACK']['regex'] = "ok"
        self.parse_table['ACK']['multi'] = "ok"

    def kill(self):
        self.killed = 1

    def define_matching_entry(self, key, unique_prefix, regex, multi_line):
        self.parse_table[key] = {}
        self.parse_table[key]['prefix'] = unique_prefix
        self.parse_table[key]['regex'] = regex
        self.parse_table[key]['multi'] = multi_line
        

    def thread(self):
        print("Recver Thread Started")
        while not self.killed:
            serial_input = self.port.readline().decode('ascii')
            print("RECVED) " + serial_input)

            if self.killed == 1:
                break

            for k in self.parse_table.keys():
                prefix = self.parse_table[k]['prefix']
                index = serial_input.find(prefix)
                if index > -1:
                    if k == 'ACK':
                        self.sender_obj.ACK()
                    elif self.parse_table[k]['multi'] == 0:
                        numbers = re.findall(self.parse_table[k]['regex'], serial_input[index+len(prefix):])
                        print(numbers)
                    else:
                        while True and not self.killed:
                            serial_input = self.port.readline().decode('ascii')
                            if serial_input == "ok":
                                self.sender_obj.ACK()
                                break
                            numbers = re.findall(self.parse_table[k]['regex'], serial_input)
                            print(numbers)

        print("Recver Thread Killed")
                    
                        
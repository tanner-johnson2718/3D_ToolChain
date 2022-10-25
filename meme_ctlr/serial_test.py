# Send a single simple G-code command such as home over the console

# Scaffold for an initial console design:
# Two threads. Sender thread for sending single commands or macros over the
# port to the printer. Recver thread is an async thread that just waits for
# input and queues the responses with time stamps until its appropiate to dump
# it to the user. Semaphore used to simply control single thread access to the
# shared port

import serial.tools.list_ports

# Send a command to printer
def send(port, cmd):
    return port.write((cmd+"\n").encode('ascii'))

def recv(port):
    ret = ""
    dat = ""
    while dat != "":
        dat = port.readline()
        ret += dat
    return ret

port = serial.Serial(port = "/dev/ttyUSB0", baudrate=115200, timeout = .25)
send(port, "G28")
send(port, "M503")
print(recv(port))

print("Exiting...")
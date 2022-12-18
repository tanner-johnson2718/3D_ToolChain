import sender
import recver
import sys
import threading
import time
import serial

port_dev = "/dev/ttyACM0"
baud = 115200
serial_timeout = 1

port = serial.Serial(port = port_dev, baudrate = baud, timeout = serial_timeout)
s = sender.Sender(port, "test.txt")
r = recver.Recver(port, s)

send_thread = threading.Thread(target=s.thread, name="Send_Thread")
send_thread.start()

recv_thread = threading.Thread(target=r.thread, name="Recv_Thread")
recv_thread.start()

r.define_matching_entry("M203", "M203", r"[-+]?(?:\d*\.\d+|\d+)", 0)

s.enQ("M20")

time.sleep(10)

s.kill()
r.kill()

send_thread.join()
recv_thread.join()
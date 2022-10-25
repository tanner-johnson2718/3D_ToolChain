# Send a single simple G-code command such as home over the console

import serial.tools.list_ports
import time

serialPort = serial.Serial(port = "/dev/ttyUSB0", baudrate=115200)

serialPort.write("G28\n".encode('ascii'))

time.sleep(10)
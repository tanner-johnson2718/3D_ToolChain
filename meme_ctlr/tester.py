import sender
import recver
import gui
import threading
import time
import serial

port_dev = "/dev/ttyACM0"
baud = 115200
serial_timeout = 1

port = serial.Serial(port = port_dev, baudrate = baud, timeout = serial_timeout)
s = sender.Sender(port, "test.txt")
r = recver.Recver(port, s)
g = gui.GUI_Man(500)

send_thread = threading.Thread(target=s.thread, name="Send_Thread")
send_thread.start()

recv_thread = threading.Thread(target=r.thread, name="Recv_Thread")
recv_thread.start()

gui_thread = threading.Thread(target=g.thread, name="GUI Thread")
gui_thread.start()

g.push_serial_input("yolo")
g.push_serial_input("yolo1")
g.push_serial_input("yolo2")
g.push_serial_input("yolo3")

time.sleep(10)

s.kill()
r.kill()
g.kill()

send_thread.join()
recv_thread.join()
gui_thread.join()

port.close()
import sender
import recver
import data_store
import threading
import time
import serial

port_dev = "/dev/ttyACM0"
baud = 115200
serial_timeout = 1

ds = data_store.DataStore(0, 0)

port = serial.Serial(port = port_dev, baudrate = baud, timeout = serial_timeout)
s = sender.Sender(port, ds)
r = recver.Recver(port, ds)


send_thread = threading.Thread(target=s.thread, name="Send_Thread")
send_thread.start()

recv_thread = threading.Thread(target=r.thread, name="Recv_Thread")
recv_thread.start()

ds.push_next_send("M503")
ds.push_next_send("M503")
ds.push_next_send("M503")

time.sleep(10)

ds.kill()
s.kill()
r.kill()


send_thread.join()
recv_thread.join()

port.close()
import sender
import recver
import data_store
import threading
import time
import serial

port_dev = "/dev/ttyACM0"
baud = 115200
serial_timeout = 1
killed = 0

ds = data_store.DataStore(0, 0)
port = serial.Serial(port = port_dev, baudrate = baud, timeout = serial_timeout)

def recv_thread(self):
    print("Recver Thread Started")
    while not self.killed:
            serial_input = port.readline().decode('ascii')
            if serial_input != "":
                self.ds.push_reponse_line(serial_input)

def send_thread(self):
        print("Sender Thread Starting")
        while not self.killed:
            cmd = self.ds.wait_on_next_to_send()
            if (not self.killed) and isinstance(cmd, str):
                port.write((cmd+"\n").encode('ascii'))
        print("Sender Thread Killed")




send_thread = threading.Thread(target=s.thread, name="Send_Thread")
send_thread.start()

recv_thread = threading.Thread(target=r.thread, name="Recv_Thread")
recv_thread.start()



time.sleep(10)

ds.kill()
s.kill()
r.kill()


send_thread.join()
recv_thread.join()

port.close()


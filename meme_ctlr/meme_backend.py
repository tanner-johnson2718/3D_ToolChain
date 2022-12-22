import data_store
import threading
import serial
import os
import time

port_dev = "/dev/ttyACM0"
baud = 115200
serial_timeout = 1
killed = 0

ds = data_store.DataStore()
port = serial.Serial(port = port_dev, baudrate = baud, timeout = serial_timeout)

def recv_thread():
    print("Recv Thread Starting...")
    while not killed:
        serial_input = port.readline().decode('ascii')
        if (not killed) and (serial_input != ""):
            ds.push_reponse_line(serial_input)
    print("Recv Thread Stopping...")

def send_thread():
    print("Send Thread Starting...")
    while not killed:
        cmd = ds.wait_on_next_to_send()
        if (not killed) and isinstance(cmd, str):
            port.write((cmd+"\n").encode('ascii'))
    print("Send Thread Stopping...")


send_t = threading.Thread(target=send_thread, name="Send_Thread")
send_t.start()

recv_t = threading.Thread(target=recv_thread, name="Recv_Thread")
recv_t.start()

while not killed:
    t = input("quit? ")
    if t == "q":
        killed = 1
        break
    elif t == "":
        continue

ds.kill()
send_t.join()
recv_t.join()
port.close()
os.system("rm -rf __pycache__ ")
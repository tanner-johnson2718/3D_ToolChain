import data_store
import threading
import serial
import os
import time

import socket

HOST = "127.0.0.1"
PORT = 65432 

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
            ds.push_reponse(serial_input)
    print("Recv Thread Stopping...")

def send_thread():
    print("Send Thread Starting...")
    while not killed:
        cmd = ds.wait_cmd()
        if (not killed) and isinstance(cmd, str):
            port.write((cmd+"\n").encode('ascii'))
    print("Send Thread Stopping...")

def server_thread():
    print("Server Thread Starting...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while not killed:
                line = ds.wait_response()
                if (not killed) and (line != ""):
                    conn.sendall(line.encode('ascii'))

    print("Server Thread Stopping...")

send_t = threading.Thread(target=send_thread, name="Send_Thread")
recv_t = threading.Thread(target=recv_thread, name="Recv_Thread")
server_t = threading.Thread(target=server_thread, name="Server_Thread")
recv_t.start()
send_t.start()
server_t.start()

while not killed:
    t = input("cmd) ")
    if t == "q":
        killed = 1
        break
    elif t == "":
        continue
    else:
        ds.push_cmd(t)


ds.kill()
send_t.join()
recv_t.join()
server_t.join()
port.close()
os.system("rm -rf __pycache__ ")
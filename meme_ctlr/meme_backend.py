import data_store
import threading
import serial
import os
import select

import socket

HOST = "127.0.0.1"
PORT = 65432 

port_dev = "/dev/ttyACM0"
baud = 115200
serial_timeout = 1
killed = 0

# Create data store, open data store and connect to client
ds = data_store.DataStore()
port = serial.Serial(port = port_dev, baudrate = baud, timeout = serial_timeout)
listening_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listening_sock.bind((HOST, PORT))
listening_sock.listen()

print("Waiting for client...")
conn, addr = listening_sock.accept()
conn.setblocking(0)
print(f"Connected by {addr}")

def recv_thread():
    print("Recv Thread Starting...")
    while not killed:
        serial_input = port.readline()
        if (not killed) and (len(serial_input) > 0):
            ds.push_reponse(serial_input.decode('ascii'))
            conn.sendall(serial_input)
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
    while not killed:
        ready = select.select([conn], [], [], serial_timeout)
        if ready[0]:
            msg = conn.recv(128).decode("ascii")
            print(msg)
    print("Server Thread Stopping...")

send_t = threading.Thread(target=send_thread, name="Send_Thread")
recv_t = threading.Thread(target=recv_thread, name="Recv_Thread")
server_t = threading.Thread(target=server_thread, name="Server_Thread")
recv_t.start()
send_t.start()
server_t.start()

while not killed:
    t = input("cmd) ")
    if t == "quit":
        killed = 1
        break
    elif t == "":
        continue
    elif t.find("query ") == 0:
        print(ds.query(t[6:]))
    else:
        ds.push_cmd(t)


ds.kill()
send_t.join()
recv_t.join()
server_t.join()

port.close()
conn.close()
listening_sock.close()

os.system("rm -rf __pycache__ ")
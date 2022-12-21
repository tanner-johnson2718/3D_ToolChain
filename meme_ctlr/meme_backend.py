import data_store
import threading
import serial
import os

port_dev = "/dev/ttyACM0"
baud = 115200
serial_timeout = 1
killed = 0

ds = data_store.DataStore(0, 0)
port = serial.Serial(port = port_dev, baudrate = baud, timeout = serial_timeout)

response_pipe_name = "./response_pipe"
os.mkfifo(response_pipe_name, 0o600)
os.system("gnome-terminal -e 'bash -c \"cat " + response_pipe_name + "\"'")

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

def response_poster():
    with open(response_pipe_name, "w") as fifo:
        print("Response Thread Starting...")
        while not killed:
            r = ds.wait_on_next_response()
            fifo.write(r)
            fifo.flush()
    print("Response Thread Stopping...")


send_t = threading.Thread(target=send_thread, name="Send_Thread")
send_t.start()

recv_t = threading.Thread(target=recv_thread, name="Recv_Thread")
recv_t.start()

response_t = threading.Thread(target=response_poster, name="Respnse Thred")
response_t.start()

while not killed:
    t = input("cmd) ")
    if t == "q":
        killed = 1
        break
    elif t == "":
        continue
    else:
        ds.push_next_send(t)

ds.kill()
send_t.join()
response_t.join()
recv_t.join()
port.close()
os.system("rm -rf __pycache__ " + response_pipe_name)
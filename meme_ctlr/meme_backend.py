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

response_pipe_name = "./response_pipe"
os.mkfifo(response_pipe_name, 0o600)
os.system("gnome-terminal -e 'bash -c \"cat " + response_pipe_name + "\"'")

sub_pipe_name = "./sub_pipe"
os.mkfifo(sub_pipe_name, 0o600)
os.system("gnome-terminal -e 'bash -c \"cat " + sub_pipe_name + "\"'")

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

def subscription_poster():
    with open(sub_pipe_name, "w") as fifo1:
        print("Subscription Thread Starting...")
        while not killed:
            time.sleep(1)
            temps = ds.get_state("M155 S1")
            fifo1.write("Temp Nozzle Current) " + str(temps[0]) + "\n")
            fifo1.write("Temp Nozzle Target) " + str(temps[1]) + "\n")
            fifo1.write("Temp Bed Current) " + str(temps[2]) + "\n")
            fifo1.write("Temp Bed Target) " + str(temps[3]) + "\n\n")

            pos = ds.get_state("M154 S1")
            fifo1.write("X) " + str(pos[0]) + "\n")
            fifo1.write("Y) " + str(pos[1]) + "\n")
            fifo1.write("Z) " + str(pos[2]) + "\n")
            fifo1.write("E) " + str(pos[3]) + "\n\n")

            a = ds.get_state("M204")
            fifo1.write("Print) " + str(a[0]) + "\n")
            fifo1.write("Retract) " + str(a[1]) + "\n")
            fifo1.write("Travel) " + str(a[2]) + "\n")

            fifo1.write("\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F")
            fifo1.flush()
    print("Subscription Thread Stopping...")


send_t = threading.Thread(target=send_thread, name="Send_Thread")
send_t.start()

recv_t = threading.Thread(target=recv_thread, name="Recv_Thread")
recv_t.start()

response_t = threading.Thread(target=response_poster, name="Respnse Thread")
response_t.start()

sub_t = threading.Thread(target=subscription_poster, name="Sub Thread")
sub_t.start()

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
os.system("rm -rf __pycache__ " + response_pipe_name + " " + sub_pipe_name)
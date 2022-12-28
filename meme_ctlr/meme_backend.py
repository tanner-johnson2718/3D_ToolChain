import data_store
import threading
import serial
import os
import select
import time
import socket
import tracemalloc as tm

HOST = "127.0.0.1"
PORT = 65432
PACKET_SIZE = 64
response_verbosity = 0
poll_list = []

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

client_send_lock = threading.Semaphore(1)

def parse_packet(packet):
    if len(packet) >= 64:
        print("Warning in parse packet. Packet appears to full")
    if len(packet) < 4:
        print("ERROR in parse packet, malformed pacekt recved")
        return
    if not (packet[-1:] == b'\n'):
        print("ERROR in parse packet, packet not terminated with new line")
        return

    # strip new line
    packet = packet[:-1]

    # parse prefix
    prefix = packet[0:4].decode("ascii")

    # Push a single gcode command onto the queue. No real way to check if 
    # packet is properly formed
    if prefix == "cmdG":
        ds.push_cmd(packet[5:].decode('ascii'))

    # Change response verbosity of response. Check that packet is 6 chars long
    # and last byte is 0,1, or 2       
    elif prefix == "subR":
        if not (len(packet) == 6):
            print("ERROR in parse packet, subR request malformed")
            return

        v = int(packet[5:])
        if not (v in [0,1,2]):
            print("ERROR in parse packet, subR invalid verbosity level) " + str(v))
            return
        global response_verbosity
        response_verbosity = v

    # Subscribe to state. Check if valid key. If key has auto poll feature
    # send cmd + "S1". If key is already in poll list, remove it and if its
    # an auto poll, send cmd + S0
    elif prefix == 'subS':
        global poll_list

        key = packet[5:].decode('ascii')
        if not ds.is_state_key(key):
            print("ERROR in parse packet, invalid key sub: " + str(key))
            return
        if key in poll_list:
            poll_list.remove(key)
            if ds.is_auto_poll(key):
                ds.push_cmd(ds.state.key2cmd[key] + " S0")
            return
        
        poll_list.append(key)

        if ds.is_auto_poll(key):
            ds.push_cmd(ds.state.key2cmd[key] + " S1")

    else:
        print("ERROR in parse packet, invalid prefix: " + prefix)

def filter_and_send_response(serial_input):
    global response_verbosity
    if response_verbosity == 0:
        return
    elif response_verbosity == 2:
        client_send_lock.acquire()
        try:
            conn.sendall(b'subR ' + serial_input)
        except:
            print("Failed to send packet to client")
        client_send_lock.release()
    elif response_verbosity == 1:
        if serial_input.decode("ascii") == "ok\n":
            return
        for key in poll_list:
            prefix = ds.get_prefix(key)
            if serial_input.decode('ascii').find(prefix) > -1:
                return
        client_send_lock.acquire()
        try:
            conn.sendall(b'subR ' + serial_input)
        except:
            print("Failed to send packet to client")
        client_send_lock.release()
    else:
        print("ERROR in filter, invalid response verbosity: " + str(response_verbosity))

def recv_thread():
    print("Recv Thread Starting...")
    while not killed:
        serial_input = port.readline()
        if (not killed) and (len(serial_input) > 0):
            ds.push_reponse(serial_input.decode('ascii'))
            filter_and_send_response(serial_input)
    print("Recv Thread Stopping...")

def send_thread():
    print("Send Thread Starting...")
    while not killed:
        cmd = ds.wait_cmd()
        if (not killed) and isinstance(cmd, str):
            port.write((cmd+"\n").encode('ascii'))
    print("Send Thread Stopping...")

def server_thread():
    global killed
    print("Server Thread Starting...")
    while not killed:
        ready = select.select([conn], [], [], serial_timeout)
        if ready[0]:
            try:
                msg = conn.recv(PACKET_SIZE)
                if not msg:
                    killed = 1
                    break
                parse_packet(msg)
            except:
                continue
                
    print("Server Thread Stopping...")

def polling_thread():
    print("Polling Thread Starting...")
    while not killed:
        time.sleep(1)

        computed_poll_list = set([ds.state.key2cmd[i] for i in poll_list])

        client_send_lock.acquire()
        try:
            conn.sendall("subS \n".encode('ascii'))
        except:
            print("Failed to send packet to client")

        # Send all the commands to the printer
        for cmd in computed_poll_list:
            if not ds.state.cmd_auto_poll[cmd]:
                ds.push_cmd(cmd)
        
        # Send state to client
        for key in poll_list:
            try:
                conn.sendall( ("subS " +  key + " " + str(ds.query(key)) + '\n').encode('ascii') )
            except:
                print("Failed to send packet to client")
        client_send_lock.release()
    print("Polling Thread Stopping...")
            
send_t = threading.Thread(target=send_thread, name="Send_Thread")
recv_t = threading.Thread(target=recv_thread, name="Recv_Thread")
server_t = threading.Thread(target=server_thread, name="Server_Thread")
poll_t = threading.Thread(target=polling_thread, name="Poll Thread")

recv_t.start()
send_t.start()
server_t.start()
poll_t.start()

time.sleep(1)
for key in ds.state.cmd_auto_poll:
    if ds.state.cmd_auto_poll[key]:
        ds.push_cmd(key + "S0")

tm.start()

while not killed:
    time.sleep(1)
    snap = tm.take_snapshot()
    for s in snap.statistics('filename'):
        print(s)
    print()

tm.stop()
ds.kill()

send_t.join()
recv_t.join()
server_t.join()
poll_t.join()


port.close()
conn.close()
listening_sock.close()

os.system("rm -rf __pycache__ ")
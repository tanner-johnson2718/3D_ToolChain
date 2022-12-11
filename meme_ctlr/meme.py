# See readme for details

from fileinput import filename
from multiprocessing import Semaphore
import PySimpleGUI as sg
import serial
import re
import threading
import time

###############################################################################
# Global Consts
###############################################################################

port_dev = "/dev/ttyUSB0"
baud = 115200
serial_timeout = 1
port = 0                  # forward declaration of serial port obj
killed = 0
pause_recv_thread = 0
recv_thread_paused = 0
hide_temp_poll = 1
hide_pos_poll = 1

info_text_lines = 16
info_label_box_text = "\
Nozzle Temp Current\n\
Nozzle Temp Target\n\n\
Bed Temp Current\n\
Bed Temp Target\n\n\
Chamber Temp Current\n\
Chamber Temp Target\n\n\
De-H20 Temp Current\n\
De-H20 Temp Target\n\n\
X Current\n\
Y Current\n\
Z Current\n\
E Current\n"

info_value_box_text="\
0.0 C\n\
0.0 C\n\n\
0.0 C\n\
0.0 C\n\n\
0.0 C\n\
0.0 C\n\n\
0.0 C\n\
0.0 C\n\n\
0.0 mm\n\
0.0 mm\n\
0.0 mm\n\
0.0 mm\n"

mech_box_text_lines = 15
mech_box_text = "\
X Probe offset\n\
Y Probe offset\n\
Z Probe offset\n\n\
X Min\n\
X Max\n\
Y Min\n\
Y Max\n\
Z Min\n\
Z Max \n\n\
X steps per mm\n\
Y steps per mm\n\
Z steps per mm\n\
E steps per mm\n\
"

mech_box_value_text ="\
0.0 mm\n\
0.0 mm\n\
0.0 mm\n\n\
0.0 mm\n\
0.0 mm\n\
0.0 mm\n\
0.0 mm\n\
0.0 mm\n\
0.0 mm\n\n\
0.0 mm\n\
0.0 mm\n\
0.0 mm\n\
0.0 mm\n\
"

rates_box_line = 18
rates_box_text = "\
Max X Vel\n\
May Y Vel\n\
Max Z Vel\n\
Max E Vel\n\n\
Max X Accel\n\
Max Y Accel\n\
Max Z Accel\n\
Max E Accel\n\n\
Init Print Accel\n\
Init Travel Accel\n\
Init Retract Accel\n\n\
Junction Deviation\n\
Min Feedrate\n\
Min Travel Feedrate\n\
Min Seg Time\n\
"

rates_box_values = "\
0.0 mm/s\n\
0.0 mm/s\n\
0.0 mm/s\n\
0.0 mm/s\n\n\
0.0 mm/s2\n\
0.0 mm/s2\n\
0.0 mm/s2\n\
0.0 mm/s2\n\n\
0.0 mm/s2\n\
0.0 mm/s2\n\
0.0 mms/s2\n\n\
0.0\n\
0.0 mm/s\n\
0.0 mm/s\n\
0.0 us\n\
"

# Globals
current_nozzle_temp = 0.0
target_nozzle_temp = 0.0
current_bed_temp = 0.0
target_bed_temp = 0.0
current_chamber_temp = 0.0
target_chamber_temp = 0.0
current_dehydrator_temp = 0.0
target_dehydrator_temp = 0.0
x_curr = 0.0
y_curr = 0.0
z_curr = 0.0
e_curr = 0.0
x_min = 0.0
x_max = 0.0
y_min = 0.0
y_max = 0.0
z_min = 0.0
z_max = 0.0
x_off = 0.0
y_off = 0.0
z_off = 0.0
x_steps_per_mm = 0.0
y_steps_per_mm = 0.0
z_steps_per_mm = 0.0
e_steps_per_mm = 0.0
max_x_vel = 0.0
max_y_vel = 0.0
max_z_vel = 0.0
max_e_vel = 0.0
max_x_accel = 0.0
max_y_accel = 0.0
max_z_accel = 0.0
max_e_accel = 0.0
junction = 0.0
min_feed_rate = 0.0
min_travel_feed_rate = 0.0
min_seg_time = 0.0
init_print_accel = 0.0
init_travel_accel = 0.0
init_retract_accel = 0.0

level_table = [["Bed", 0,0,0,0, 0,0,0,0], ["Hot End", 0,0,0,0, 0,0,0,0], ["De-H20", 0,0,0,0, 0,0,0,0], ["Chamber", 0,0,0,0, 0,0,0,0]]
sd_entries = ""

globals_changed = 0

###############################################################################
# Global accessor functions. Global Values should only be updated here
###############################################################################

global_lock = Semaphore(1)

def update_global_temps(nozzle_curr, nozzle_target, bed_curr, bed_target):
    global current_nozzle_temp
    global target_nozzle_temp
    global current_bed_temp
    global target_bed_temp

    global_lock.acquire()
    current_nozzle_temp = nozzle_curr
    target_nozzle_temp = nozzle_target
    current_bed_temp = bed_curr
    target_bed_temp = bed_target
    global_lock.release()

def update_global_level_table(levels):
    global level_table

    global_lock.acquire()
    for i in range(0, 4):
        for j in range(0, 4):
            level_table[i][j+1] = levels[i][j]
    global_lock.release()

def update_global_z_offset(new_x, new_y, new_z):
    global z_off
    global x_off
    global y_off
    global_lock.acquire()
    x_off = new_x
    y_off = new_y
    z_off = new_z
    global_lock.release()

def update_global_steps_per_mm(new):
    global x_steps_per_mm
    global y_steps_per_mm
    global z_steps_per_mm
    global e_steps_per_mm
    global_lock.acquire()
    x_steps_per_mm = new[0]
    y_steps_per_mm = new[1]
    z_steps_per_mm = new[2]
    e_steps_per_mm = new[3]
    global_lock.release()

def update_globals_curr_pos(x,y,z,e):
    global x_curr
    global y_curr
    global z_curr
    global e_curr
    global_lock.acquire()
    x_curr = x
    y_curr = y
    z_curr = z
    e_curr = e
    global_lock.release()

def update_globals_max_vel(x,y,z,e):
    global max_x_vel
    global max_y_vel
    global max_z_vel
    global max_e_vel
    global_lock.acquire()
    max_x_vel = x
    max_y_vel = y
    max_z_vel = z
    max_e_vel = e
    global_lock.release()

def update_globals_acces(accels):
    global max_x_accel
    global max_y_accel
    global max_z_accel
    global max_e_accel
    global_lock.acquire()
    max_x_accel = accels[0]
    max_y_accel = accels[1]
    max_z_accel = accels[2]
    max_e_accel = accels[3]
    global_lock.release()

def update_globals_init_accels(accels):
    global init_travel_accel
    global init_print_accel
    global init_retract_accel
    global_lock.acquire()
    init_print_accel = accels[0]
    init_retract_accel = accels[1]
    init_travel_accel = accels[2]
    global_lock.release()

def update_globals_advanced(advanced):
    global junction
    global min_feed_rate
    global min_travel_feed_rate
    global min_seg_time
    global_lock.acquire()
    min_seg_time = advanced[0]
    min_feed_rate = advanced[1]
    min_travel_feed_rate = advanced[2]
    junction = advanced[3]
    global_lock.release()

def update_globals_sd_list(new):
    global sd_entries
    global_lock.acquire()
    sd_entries = new
    global_lock.release()

###############################################################################
# Set Serial port and control variables for threaded access
###############################################################################

# Send a command to printer
def send(port, cmd):
    return port.write((cmd+"\n").encode('ascii'))

# recv a single line from the printer
def recv(port):
    return port.readline().decode('ascii')

# wait for an 'ok' ACK
def wait_for_ACK(port):
    error = 0
    while True:
        response = recv(port)
        print(response)
        if response.find("Error") > -1:
            error = 1
        if response.find("ok") > -1:
            break
    return error

def cycle_serial_func():
    global port
    port.close()
    time.sleep(1)
    port = serial.Serial(port = port_dev, baudrate = baud, timeout = serial_timeout)
    time.sleep(1)


port = serial.Serial(port = port_dev, baudrate = baud, timeout = serial_timeout)

###############################################################################
# Set UP GUI
###############################################################################

# Define Window layout and Theme
sg.theme('DarkAmber')
layout = [  [sg.Text("Send GCODE) "), sg.InputText(key="cmd_box", size=(80,1))],
            [sg.Button("Home", key="home_button"), sg.Button("STOP!", key="STOP"), sg.Button("Disable Steppers", key="kill_steps"), sg.Button("Pull Stats", key="cord_button"), sg.Button("Tram", key="tram"), sg.Button("Level", key="level_button"), sg.Button("Populate SD Table", key="pop_SD"), sg.Button("Cycle Serial", key="cycle_serial_button")],
            [sg.Text("Nozzle Temp:    ", size=(14,1)), sg.InputText(key="nozzle_target", size=(8,1)), sg.Text("Bed Temp:       ", size=(14,1)), sg.InputText(key="bed_target", size=(8,1)), sg.Text("Z Offset:       ", size=(14,1)), sg.InputText(key="z_off", size=(8,1))],
            [sg.Frame("Heat and Pos", [[sg.Text(info_label_box_text, size=(20,info_text_lines), key='info_label_box'), sg.Text(info_value_box_text, size=(15,info_text_lines), key='info_value_box')]]), sg.Frame("Mechanical Params", [[sg.Text(mech_box_text, size=(20,mech_box_text_lines), key='mech_label_box'), sg.Text(mech_box_value_text, size=(15,mech_box_text_lines), key='mech_value_box')]]), sg.Frame("Rates", [[sg.Text(rates_box_text, size=(20,rates_box_line)), sg.Text(rates_box_values, size=(20, rates_box_line), key="rates_values")]])],
            [sg.Table(level_table,  ['Thermal', 'P      ','I      ','D      ', 'Index  ', 'PU Res ', 'Res 25C', 'B      ', 'C      '], num_rows=4, key="level_table_ui")],
            [sg.InputText(size=(20,1), key="input_file"), sg.Button("Send Local File to SD", key="send_file_button"), sg.InputText(size=(20,1), key="print_file"), sg.Button("Print", key="print_button")], 
            [sg.Multiline('', key="sd_explorer", size=(60,20))]
        ]

# Create the Window and define elements
window = sg.Window('MEME', layout, finalize=1)
window["cmd_box"].bind("<Return>", "enter_hit")
window["nozzle_target"].bind("<Return>", "enter_hit")
window["bed_target"].bind("<Return>", "enter_hit")
window["z_off"].bind("<Return>", "enter_hit")
cmd_box = window["cmd_box"]
info_label_box = window["info_value_box"]
nozzle_target_temp_input_box = window["nozzle_target"]
bed_target_temp_input_box = window["bed_target"]
z_off_input_box = window["z_off"]
pull_coordinates_button = window["cord_button"]
home_button = window["home_button"]
level_button = window["level_button"]
level_table_ui = window["level_table_ui"]
sd_explorer = window["sd_explorer"]
sd_table_populate = window["pop_SD"]
input_file_box = window["input_file"]
input_file_button = window["send_file_button"]
print_file_box = window["print_file"]
mech_label_box = window["mech_value_box"]
rates_box = window["rates_values"]

###############################################################################
# GUI Accessor functions. Only the main thread should try to update GUI
# elements. Following functions will enforce this. ALL UPDATES TO GUI ELEMENTS
# SHOULD GO THROUGH HERE.
############################################################################### 

# Input info labels sg object and update with current global values
def update_info_label_box():
    if __name__ != "__main__":
        print("ERROR, GUI elements accessed by non main thread")
        return

    new_text = str(current_nozzle_temp) + " C\n" +\
              str(target_nozzle_temp)  + " C\n\n" +\
              str(current_bed_temp)    + " C\n" +\
              str(target_bed_temp)     + " C\n\n" +\
              str(current_chamber_temp) + " C\n" +\
              str(target_chamber_temp)  + " C\n\n" +\
              str(current_dehydrator_temp)    + " C\n" +\
              str(target_dehydrator_temp)     + " C\n\n" +\
              str(x_curr)              + " mm\n" +\
              str(y_curr)              + " mm\n" +\
              str(z_curr)              + " mm\n" +\
              str(e_curr)              + " mm\n"

    info_label_box.update(new_text)

# Update mech info box
def update_mech_box_label():
    if __name__ != "__main__":
        print("ERROR, GUI elements accessed by non main thread")
        return

    new_text = str(x_off) + " mm\n" +\
               str(y_off) + " mm\n" +\
               str(z_off) + " mm\n\n" +\
               str(x_min) + " mm\n" +\
               str(x_max) + " mm\n" +\
               str(y_min) + " mm\n" +\
               str(y_max) + " mm\n" +\
               str(z_min) + " mm\n" +\
               str(z_max) + " mm\n\n" +\
               str(x_steps_per_mm) + " mm\n" +\
               str(y_steps_per_mm) + " mm\n" +\
               str(z_steps_per_mm) + " mm\n" +\
               str(e_steps_per_mm) + " mm\n"
    
    mech_label_box.update(new_text)
    
# Update rates box
def update_rates_box():
    if __name__ != "__main__":
        print("ERROR, GUI elements accessed by non main thread")
        return
    
    new_text = str(max_x_vel) + " mm/s\n" +\
               str(max_y_vel) + " mm/s\n" +\
               str(max_z_vel) + " mm/s\n" +\
               str(max_e_vel) + " mm/s\n\n" +\
               str(max_x_accel) + " mm/s2\n" +\
               str(max_y_accel) + " mm/s2\n" +\
               str(max_z_accel) + " mm/s2\n" +\
               str(max_e_accel) + " mm/s2\n\n" +\
               str(init_print_accel) + " mm/s2\n" +\
               str(init_travel_accel) + " mm/s2\n" +\
               str(init_retract_accel) + " mm/s2\n\n" +\
               str(junction) + "\n" +\
               str(min_feed_rate) + " mm/s\n" +\
               str(min_travel_feed_rate) + " mm/s\n" +\
               str(min_seg_time) + " us\n"

    rates_box.update(new_text)

# Update the SD explorer
def update_sd_explorer():
    if __name__ != "__main__":
        print("ERROR, GUI elements accessed by non main thread")
        return

    sd_explorer.update(sd_entries)
    sd_explorer.set_vscroll_position(1.0)

# Update level table
def update_level_table():
    if __name__ != "__main__":
        print("ERROR, GUI elements accessed by non main thread")
        return

    level_table_ui.update(level_table)

###############################################################################
# Thread functions
###############################################################################

# Thread to block on input from printer
def _recver_thread():

    global pause_recv_thread
    global recv_thread_paused

    #  == T:xxx.xx/xxx.xx == B:xxx.xx/xxx.xx
    # Takes in a line and tests if it is a temp (M155) pull response. If it is,
    # returns list of floats: current nozzle, target nozzle, current bed, target
    # bed. Else returns empty list
    def parse_temp(line):
        if line.find(" T:") == 0:
            numbers = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", line)
            return numbers
        return []

    # echo:  M851 Zx.xx
    # Takes line of input and look for a Z_offset response
    def parse_z_off(line):
        if line.find("M851") > 0:
            numbers = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", line)
            return numbers
        return []

    # M92 
    def parse_steps_per_mm(line):
        if line.find("M92") > 0:
            numbers = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", line)
            return numbers
        return []

    # look for position updates
    def parse_pos(line):
        if line.find("X:") == 0 and line.find("Count") > 0:
            numbers = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", line)
            return numbers
        return []

    # look for Feed rates
    def parse_feed_rate(line):
        if line.find("M203") > -1:
            numbers = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", line)
            return numbers
        return []

    # Loof for accel data
    def parse_accels(line):
        if line.find("M201") > -1:
            numbers = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", line)
            return numbers
        return []

    # Look for advanced movement setting
    def parse_advanced_move(line):
        if line.find("M205") > -1:
            numbers = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", line)
            return numbers
        return []

    # Look for init accels
    def parse_init_accels(line):
        if line.find("M204") > -1:
            numbers = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", line)
            return numbers
        return []

    # look for level table
    def parse_level_table(line):
        if line.find("Bilinear") == 0:
            # found the first line of the grid, read the next couple lines till
            # we fill the table. May read input from other commands i.e. temp,
            # but we will just throw those lines out
            lines_read = 0
            new_table = []
            while lines_read < 4 and not killed:
                print("Waiting for mesh level entries...")
                next_line = recv(port)
                if next_line.find(str(lines_read)) == 1:
                    numbers = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", next_line)
                    new_table.append(numbers[1:])
                    lines_read += 1
                else:
                    continue
            print("Done with mesh level reading")
            return new_table
        return []

    # look for SD card list
    def parse_sd_list(line):
        if line.find("Begin file list") == 0:
            ret = []
            while True and not killed:
                print("Waiting for more SD entries...")
                new_line = recv(port)
                if new_line.find("End file list") == 0:
                    print("Done with SD\n")
                    return ret

                if new_line.find(".GCO"):
                    ret.append(new_line)
        return []

    while True and not killed:
        serial_input = recv(port)

        if killed == 1:
            break

        if pause_recv_thread == 1:
            recv_thread_paused = 1
            print("Recv Thread Paused")
            while pause_recv_thread and not killed:
                time.sleep(1)
            print("Recv Thread Resumed")
            recv_thread_paused = 0

        # Serial input ready to be displayed
        if serial_input == "" :
            continue
        
        temps = parse_temp(serial_input)
        z_offs = parse_z_off(serial_input)
        steps = parse_steps_per_mm(serial_input)
        pos = parse_pos(serial_input)
        feeds =  parse_feed_rate(serial_input)
        accels = parse_accels(serial_input)
        init_accels = parse_init_accels(serial_input)
        advanced = parse_advanced_move(serial_input)
        levels = parse_level_table(serial_input)
        sd_list = parse_sd_list(serial_input)

        if len(temps) >= 4:
            update_global_temps(temps[0], temps[1], temps[2], temps[3])
            if hide_temp_poll:
                continue
        elif len(z_offs) == 4:
            update_global_z_offset(z_offs[1], z_offs[2], z_offs[3])
        elif len(steps) == 5:
            update_global_steps_per_mm(steps[1:])
        elif len(pos) > 6:
            update_globals_curr_pos(pos[0], pos[1], pos[2], pos[3])
            if hide_pos_poll:
                continue
        elif len(feeds) > 4:
            update_globals_max_vel(feeds[1],feeds[2],feeds[3],feeds[4])
        elif len(accels) > 4:
            update_globals_acces(accels[1:])
        elif len(init_accels) > 3:
            update_globals_init_accels(init_accels[1:])
        elif len(advanced) > 4:
            update_globals_advanced(advanced[1:])
        elif len(levels) > 0:
            update_global_level_table(levels)
        elif len(sd_list) > 0:
            new_sd = ""
            for s in sd_list:
                new_sd = new_sd + s
            update_globals_sd_list(new_sd)
        
        print(serial_input, end="")

###############################################################################
# Main
###############################################################################

if __name__ == "__main__":

    # Let the serial port boot
    time.sleep(2)

    # Start up command
    send(port, "M155 S1")
    send(port, "M154 S1")
    send(port, "M503")

    # Start threads
    recver_thread = threading.Thread(target=_recver_thread, name="Recv_Thread")
    recver_thread.start()

    while True:
        event = ""
        event, values = window.read(1000)    # block on GUI event

        if event == sg.WIN_CLOSED:       # Close button hit
            break

        # emergency stop
        elif event == "STOP":
            send(port, "M112")

        # Kill Steppers
        elif event == "kill_steps":
            send(port, "M84")

        # Enter hit while in command box
        elif event == "cmd_box" + "enter_hit":
            command = cmd_box.get()
            print("Sending) " + command + "\n")
            send(port, command)

        # nozzle temp updated
        elif event == "nozzle_target" + "enter_hit":
            temp = nozzle_target_temp_input_box.get()
            send(port, "M104 S"+temp)

        # bed temp updated
        elif event == "bed_target" + "enter_hit":
            temp = bed_target_temp_input_box.get()
            send(port, "M140 S"+temp)

        # z_off updated
        elif event == "z_off" + "enter_hit":
            val = z_off_input_box.get()
            send(port, "M851 Z" + val)
            send(port, "M500")
            send(port, "M501")
            send(port, "M503")

        # Pull Stats button pressed
        elif event == "cord_button":
            send(port, "M114")
            send(port, "M503")

        # Home printer
        elif event == "home_button":
            send(port, "G28")

        # Tram
        elif event == "tram":
            send(port, "G28")
            send(port, "G30 X30 Y50")
            send(port, "G30 X310 Y50")
            send(port, "G30 X30 Y325")
            send(port, "G30 X310 Y325")

        # Level
        elif event == "level_button":
            send(port, "G28")
            send(port, "G29 P1 V4 T0")
            send(port, "G29 S0")
            send(port, "G29 A")
            send(port, "M500")
            send(port, "G29 P5")

        # populate SD table
        elif event == "pop_SD":
            send(port, "M20")

        # Send a print
        elif event == "print_button":
            send(port, "M23 " + print_file_box.get())
            send(port, "M27 S5")   # 5s print status report
            send(port, "M24")

        # Close and reopen serial port
        elif event == "cycle_serial_button":
            pause_recv_thread = 1
            while not recv_thread_paused:
                time.sleep(1)
            cycle_serial_func()
            pause_recv_thread = 0

        # send local file to SD
        elif event == "send_file_button":
            file_name = input_file_box.get()

            # open file
            try:
                # Turn off temp polling and pause recv_thread, wait till its paused
                pause_recv_thread = 1
                while not recv_thread_paused:
                    time.sleep(1)

                # Before sending data set line number to 0
                send(port, "M110 N0")

                # Start sending data, but wait for response from M28
                print("Sending M28")
                send(port, "M28 " + file_name)
                wait_for_ACK(port)
                print("Reading " + file_name + "...")

                with open(file_name, encoding="utf-8") as my_file_handle:
                    
                    tot_sent = 0
                    line = 1

                    for chunk in my_file_handle:

                        if not (chunk.find("G") == 0 or chunk.find("M") == 0):
                            continue

                        # Add line number and strip trailing new line
                        chunk = "N" + str(line) + " " + chunk.rstrip()
                        line += 1

                        # strip comments
                        off = chunk.find(";")
                        if off > -1:
                            chunk = chunk[0:off]
                        sum = 0
                        for c in chunk:
                            sum ^= ord(c)
                        chunk = chunk + '*' + str(sum)
                        
                        while 1:
                            send(port, chunk)

                            print(chunk)
                            code = wait_for_ACK(port)
                            if not code:
                                break

                print("Sending M29")
                send(port, "M29")
                wait_for_ACK(port)
                pause_recv_thread = 0
                send(port, "M155 S1")                  # Turn on temp polling
                send(port, "M154 S1")

            except Exception as e:
                print("ERROR reading " + file_name)
                print(str(e))
                send(port, "M29")
                pause_recv_thread = 0
                send(port, "M155 S1")                  # Turn on temp polling
                send(port, "M154 S1")

        # Update values in gui elements
        update_info_label_box()
        update_mech_box_label()
        update_rates_box()
        update_sd_explorer()
        update_level_table()
    
    # Kill the recver thread
    killed = 1
    recver_thread.join()

    # Clean Up Resources
    window.close()
    port.close()
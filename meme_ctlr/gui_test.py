# TODO doc

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

info_text_lines = 16
info_label_box_text = "\
Nozzle Temp Current\n\
Nozzle Temp Target\n\
Bed Temp Current\n\
Bed Temp Target\n\n\
X Current\n\
Y Current\n\
Z Current\n\n\
Z Offset\n\
Steps per mm\n\
Max X vel\n\
Max Y vel\n\
Max Z vel\n\
Max E vel\n"

info_value_box_text="\
0.0 C\n\
0.0 C\n\
0.0 C\n\
0.0 C\n\n\
0.0 mm\n\
0.0 mm\n\
0.0 mm\n\n\
0.0 mm\n\
0.0 steps\n\
0.0 m/s\n\
0.0 m/s\n\
0.0 m/s\n\
0.0 m/s"

current_nozzle_temp = 0.0
target_nozzle_temp = 0.0
current_bed_temp = 0.0
target_bed_temp = 0.0
x_curr = 0.0
y_curr = 0.0
z_curr = 0.0
z_off = 0.0
steps_per_mm = 0.0
max_x_vel = 0.0
max_y_vel = 0.0
max_z_vel = 0.0
max_e_vel = 0.0

level_table = [["Front", 0,0,0,0], ["Mid F", 0,0,0,0], ["Mid R", 0,0,0,0], ["Rear", 0,0,0,0]]

###############################################################################
# Set Serial port and control variables for threaded access
###############################################################################

# Send a command to printer
def send(port, cmd):
    return port.write((cmd+"\n").encode('ascii'))

# recv a single line from the printer
def recv(port):
    return port.readline().decode('ascii')

port = serial.Serial(port = port_dev, baudrate = baud, timeout = serial_timeout)

###############################################################################
# Set UP GUI
###############################################################################

# Define Window layout and Theme
sg.theme('DarkAmber')
layout = [  [sg.Text("Nozzle Temp: ", size=(13,1)), sg.InputText(key="nozzle_target", size=(8,1)), sg.Text("Bed Temp: ", size=(10,1)), sg.InputText(key="bed_target", size=(8,1)), sg.Text("Z Offset: ", size=(10,1)), sg.InputText(key="z_off", size=(8,1)), sg.Text("Steps per mm: ", size=(14,1)), sg.InputText(key="steps", size=(8,1)), sg.Button("Pull Stats", key="cord_button")],
            [sg.Text(info_label_box_text, size=(20,info_text_lines), key='info_label_box'), sg.Text(info_value_box_text, size=(15,info_text_lines), key='info_value_box') , sg.Multiline('', key="console", size=(80,20), disabled=1)],
            [sg.Text(" " * 65),sg.InputText(key="cmd_box", size=(80,1))],
            [sg.Button("Home", key="home_button"), sg.Text("X", size=(1,1)), sg.InputText("0",key="x_in", size=(8,1)), sg.Text("Y", size=(1,1)), sg.InputText("0",key="y_in", size=(8,1)), sg.Text("Z", size=(1,1)), sg.InputText("0",key="z_in", size=(8,1)), sg.Button("Go", key="pos_move"), sg.Text("E", size=(1,1)), sg.InputText("0.0", size=(8,1), key="e_move"), sg.Button("Extrude", key="extrude_button"), sg.Button("Retract", key="retract_button")],
            [sg.Button("Level", key="level_button"), sg.Table(level_table,  ['        ', 'Left    ','Mid L   ','Mid R   ', 'Right   '], num_rows=4, key="level_table_ui")],
            [sg.InputText(size=(20,1), key="input_file"), sg.Button("Send Local File to SD", key="send_file_button"), sg.Button("Populate SD Table", key="pop_SD")], 
            [sg.Multiline('', key="sd_explorer", size=(60,20))]
        ]

# Create the Window and define elements
window = sg.Window('Window Title', layout, finalize=1)
window["cmd_box"].bind("<Return>", "enter_hit")
window["nozzle_target"].bind("<Return>", "enter_hit")
window["bed_target"].bind("<Return>", "enter_hit")
window["z_off"].bind("<Return>", "enter_hit")
window["steps"].bind("<Return>", "enter_hit")
console = window["console"]
cmd_box = window["cmd_box"]
info_label_box = window["info_value_box"]
nozzle_target_temp_input_box = window["nozzle_target"]
bed_target_temp_input_box = window["bed_target"]
z_off_input_box = window["z_off"]
steps_input_box = window["steps"]
pull_coordinates_button = window["cord_button"]
home_button = window["home_button"]
x_go_box = window["x_in"]
y_go_box = window["y_in"]
z_go_box = window["z_in"]
go_button = window["pos_move"]
e_go_box = window["e_move"]
extrude_botton = window["extrude_button"]
retract_botton = window["retract_button"]
level_button = window["level_button"]
level_table_ui = window["level_table_ui"]
sd_explorer = window["sd_explorer"]
sd_table_populate = window["pop_SD"]
input_file_box = window["input_file"]
input_file_button = window["send_file_button"]

# Helper to append multiline (console). Input multiline sg obj and add line at
# end of lines. Scroll to last line upon update.
def update_console(multi_line_obj, text):
    multi_line_obj.update(multi_line_obj.get() + "\n" + text)
    multi_line_obj.set_vscroll_position(1.0)

# Input info labels sg object, the line indexes to update, and values to update too 
def update_info_label_box(text_obj):
    new_text = str(current_nozzle_temp) + " C\n" +\
              str(target_nozzle_temp)  + " C\n" +\
              str(current_bed_temp)    + " C\n" +\
              str(target_bed_temp)     + " C\n\n" +\
              str(x_curr)              + " mm\n" +\
              str(y_curr)              + " mm\n" +\
              str(z_curr)              + " mm\n\n" +\
              str(z_off)               + " mm\n" +\
              str(steps_per_mm)        + " mm\n" +\
              str(max_x_vel)           + " mm/s\n" +\
              str(max_y_vel)           + " mm/s\n" +\
              str(max_z_vel)           + " mm/s\n" +\
              str(max_e_vel)           + " mm/s" 

    text_obj.update(new_text)

###############################################################################
# Thread functions
###############################################################################

# Thread to block on input from printer
def _recver_thread():

    global current_nozzle_temp
    global target_nozzle_temp
    global current_bed_temp
    global target_bed_temp
    global x_curr
    global y_curr
    global z_curr
    global z_off
    global steps_per_mm
    global max_x_vel
    global max_y_vel
    global max_z_vel
    global max_e_vel

    global level_table

    global info_label_box
    global console
    global level_table_ui
    global sd_explorer

    #  == T:xxx.xx/xxx.xx == B:xxx.xx/xxx.xx
    # Takes in a line and tests if it is a temp (M155) pull response. If it is,
    # returns list of floats: current nozzle, target nozzle, current bed, target
    # bed. Else returns empty list
    def parse_temp(line):
        if line.find(" == T:") == 0:
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

    # look for level table
    def parse_level_table(line):
        if line.find("Bilinear") == 0:
            # found the first line of the grid, read the next couple lines till
            # we fill the table. May read input from other commands i.e. temp,
            # but we will just throw those lines out
            lines_read = 0
            new_table = []
            while lines_read < 4:
                next_line = recv(port)
                if next_line.find(str(lines_read)) == 1:
                    numbers = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", next_line)
                    new_table.append(numbers[1:])
                    lines_read += 1
                else:
                    continue
            return new_table
        return []

    # look for SD card list
    def parse_sd_list(line):
        if line.find("Begin file list") == 0:
            ret = []
            while True:
                new_line = recv(port)
                if new_line.find("End file list") == 0:
                    return ret

                if new_line.find(".GCO"):
                    ret.append(new_line)
        return []

    while True:
        serial_input = recv(port)

        if killed == 1:
            break

        # Serial input ready to be displayed
        if serial_input == "" :
            continue
        
        temps = parse_temp(serial_input)
        z_offs = parse_z_off(serial_input)
        steps = parse_steps_per_mm(serial_input)
        pos = parse_pos(serial_input)
        feeds =  parse_feed_rate(serial_input)
        levels = parse_level_table(serial_input)
        sd_list = parse_sd_list(serial_input)

        if len(temps) >= 4:
            current_nozzle_temp = temps[0]
            target_nozzle_temp  = temps[1]
            current_bed_temp    = temps[2]
            target_bed_temp     = temps[3]
            update_info_label_box(info_label_box)  # Update info values
        elif len(z_offs) == 2:
            z_off = z_offs[1]
            update_info_label_box(info_label_box)
        elif len(steps) == 5:
            steps_per_mm = steps[4]
            update_info_label_box(info_label_box)
        elif len(pos) > 6:
            x_curr = pos[0]
            y_curr = pos[1]
            z_curr = pos[2]
            update_info_label_box(info_label_box)
        elif len(feeds) > 4:
            max_x_vel = feeds[1]
            max_y_vel = feeds[2]
            max_z_vel = feeds[3]
            max_e_vel = feeds[4]
            update_info_label_box(info_label_box)
        elif len(levels) > 0:
            for i in range(0, 4):
                for j in range(0, 4):
                    level_table[i][j+1] = levels[i][j]
            level_table_ui.update(level_table)
        elif len(sd_list) > 0:
            updated_list = ""
            for s in sd_list:
                updated_list = updated_list + s
            sd_explorer.update(updated_list)
            sd_explorer.set_vscroll_position(1.0)
        else:
            update_console(console, serial_input)

###############################################################################
# Main
###############################################################################

if __name__ == "__main__":

    # Let the serial port boot
    time.sleep(2)

    # Start temp polling
    send(port, "M155 S1")

    # Start threads
    recver_thread = threading.Thread(target=_recver_thread)
    recver_thread.start()

    while True:
        event = ""
        event, values = window.read(1)    # block on GUI event

        if event == sg.WIN_CLOSED:       # Close button hit
            break

        # Enter hit while in command box
        elif event == "cmd_box" + "enter_hit":
            command = cmd_box.get()
            update_console(console, "Sending) " + command)
            cmd_box.update("")
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

        # steps per mm updated
        elif event == "steps" + "enter_hit":
            val = steps_input_box.get()
            send(port, "M92 E" + val)
            send(port, "M500")
            send(port, "M501")
            send(port, "M503")

        # Pull Coordinates button pressed
        elif event == "cord_button":
            send(port, "M114")
            send(port, "M503")

        # Home printer
        elif event == "home_button":
            send(port, "G28")

        # Goto Coordinates
        elif event == "pos_move":
            x = x_go_box.get()
            y = y_go_box.get()
            z = z_go_box.get()
            send(port, "G1 X" + x + " Y" + y + " Z" + z)

        # Extrude
        elif event == "extrude_button":
            amount = e_go_box.get()
            send(port, "G92 E0")
            send(port, "G1 E" + amount)
            send(port, "G92 E0")

        # Retract
        elif event == "retract_button":
            amount = e_go_box.get()
            send(port, "G92 E" + amount)
            send(port, "G1 E0")

        # Level
        elif event == "level_button":
            send(port, "G28")
            send(port, "G29 V4")
            send(port, "M500")
            send(port, "M501")
            send(port, "M420 S1 V1")

        # populate SD table
        elif event == "pop_SD":
            send(port, "M20")

        # send local file to SD
        elif event == "send_file_button":
            file_name = input_file_box.get()
            

    # Kill the recver thread
    killed = 1
    recver_thread.join()

    # Clean Up Resources
    window.close()
    port.close()
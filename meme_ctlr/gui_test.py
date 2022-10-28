# TODO doc

import PySimpleGUI as sg
import serial
import re

###############################################################################
# Global Consts
###############################################################################

port_dev = "/dev/ttyUSB0"
baud = 115200
serial_timeout = 0
port = 0                  # forward declaration of serial port obj

info_text_lines = 13
info_label_box_text = "\
Nozzle Temp Current\n\
Nozzle Temp Target\n\
Bed Temp Current\n\
Bed Temp Target\n\
X Current\n\
Y Current\n\
Z Current\n\n\
Z Offset\n\
Steps per mm\n\
X Limit\n\
Y Limit\n\
Z Limit\n"

info_value_box_text="\
0.0 C\n\
0.0 C\n\
0.0 C\n\
0.0 C\n\
0.0 mm\n\
0.0 mm\n\
0.0 mm\n\n\
0.0 mm\n\
0.0 mm\n\
0.0 mm\n\
0.0 mm\n\
0.0 mm"

current_nozzle_temp = 0.0
target_nozzle_temp = 0.0
current_bed_temp = 0.0
target_bed_temp = 0.0
x_curr = 0.0
y_curr = 0.0
z_curr = 0.0
z_off = 0.0
steps_per_mm = 0.0
x_lim = 0.0
y_lim = 0.0
z_lim = 0.0

###############################################################################
# Set Serial port and helpers
###############################################################################

# Send a command to printer
def send(port, cmd):
    return port.write((cmd+"\n").encode('ascii'))

# recv a single line from the printer
def recv(port):
    return port.readline().decode('ascii')

port = serial.Serial(port = port_dev, baudrate = baud, timeout = serial_timeout)

###############################################################################
# Queue for push and pull traffic on 
###############################################################################

class q_entry:
    def __init__(self):
        self.data = ""

    def set(self, text):
        self.data = text

class q:
    def __init__(self):
        self.queue = []

    def push(self, text):
        self.queue.append(text)
    
    def pull(self, text):
        self.queue[0]
        del self.queue[0]

#  == T:xxx.xx/xxx.xx == B:xxx.xx/xxx.xx
# Takes in a line and tests if it is a temp (M155) pull response. If it is,
# returns list of floats: current nozzle, target nozzle, current bed, target
# bed. Else returns empty list
def parse_temp(line):
    if line.find(" == T:") == 0:
        numbers = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", line)
        print(numbers)
        return numbers
    return []

push_q = q()     # elements in push q are single lines of g-code
pull_q = q()     # elements in pull q are single lines from serial reads


###############################################################################
# Set UP GUI
###############################################################################

# Define Window layout and Theme
sg.theme('DarkAmber')
layout = [  [sg.Text(info_label_box_text, size=(20,info_text_lines), key='info_label_box'), sg.Text(info_value_box_text, size=(10,info_text_lines), key='info_value_box') , sg.Multiline('', key="console", size=(80,20), disabled=1)],
            [sg.Text(" " * 56), sg.InputText(key="cmd_box", size=(80,1))],
        ]

# Create the Window and define elements
window = sg.Window('Window Title', layout, finalize=1)
window["cmd_box"].bind("<Return>", "enter_hit")
console = window["console"]
cmd_box = window["cmd_box"]
info_label_box = window["info_value_box"]

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
              str(target_bed_temp)     + " C\n" +\
              str(x_curr)              + " mm\n" +\
              str(y_curr)              + " mm\n" +\
              str(z_curr)              + " mm\n\n" +\
              str(z_off)               + " mm\n" +\
              str(steps_per_mm)        + " mm\n" +\
              str(x_lim)              + " mm\n" +\
              str(y_lim)              + " mm\n" +\
              str(z_lim)              + " mm\n"

    text_obj.update(new_text)



###############################################################################
# Main Loop
###############################################################################

while True:
    event = ""
    event, values = window.read(0)    # Check for GUI event
    serial_input = recv(port)         # Check for serial input

    # Window closed
    if event == sg.WIN_CLOSED:
        break

    # Enter hit while in command box
    elif event == "cmd_box" + "enter_hit":
        command = cmd_box.get()
        update_console(console, "Sending) " + command)
        cmd_box.update("")
        send(port, command)

    # Serial input ready to be displayed
    if serial_input != "" :
        temps = parse_temp(serial_input)
        if len(temps) >= 4:
            current_nozzle_temp = temps[0]
            target_nozzle_temp  = temps[1]
            current_bed_temp    = temps[2]
            target_bed_temp     = temps[3]
            update_info_label_box(info_label_box)
        
        else:
            update_console(console, serial_input)
       

window.close()
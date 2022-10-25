import PySimpleGUI as sg
import serial

###############################################################################
# Globals
###############################################################################

port_dev = "/dev/ttyUSB0"
baud = 115200
serial_timeout = 0
port = 0                  # forward declaration of serial port obj

###############################################################################
# Set UP GUI
###############################################################################

# Define Window layout and Theme
sg.theme('DarkAmber')
layout = [  [sg.Multiline('', key="console", size=(80,20), disabled=1)],
            [sg.InputText(key="cmd_box", size=(80,1))],
        ]

# Create the Window and define elements
window = sg.Window('Window Title', layout, finalize=1)
window["cmd_box"].bind("<Return>", "enter_hit")
console = window["console"]
cmd_box = window["cmd_box"]

# Helper to append multilin
def multi_line_append(multi_line_obj, text):
    multi_line_obj.update(multi_line_obj.get() + "\n" + text)
    multi_line_obj.set_vscroll_position(1.0)

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
        multi_line_append(console, "Sending) " + command)
        cmd_box.update("")
        send(port, command)

    # Serial input ready to be displayed
    if serial_input != "" :
        multi_line_append(console, serial_input)

window.close()
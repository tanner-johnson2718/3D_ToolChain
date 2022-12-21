# MEME Controller

G code sender, printer montoring and control, and interface for executing testing/calibration sequences.

# Serial Communication

* Sending and recv-ing commands is done through the USB serial port (/dev/ttyACM0 for skr mini E3 V3.0)
* Commands are send in ascii delimited by a new line char
* The command protocal is [G-code](../marlin/Marlin_Docs/_gcode/)
* All commands, if properly recv-ed by the printer, are ACK-ed with a response "ok" 

# Dependancies
* pip3 install customtkinter
* sudo apt-get install python3-tk
* Python 3.8.10

# Backend Architecture

![alt text]("MEME_Backend.png")

# TODO
* Doc base arch
* program stats and deal with unbounded sendQ
* Start up commands and macros
* Subcription system) I want parsed values from command x,y,z at a regular time interval
* Programmatic way of adding to the parsed command list i.e. state map
* send data over sockets instead of pipe (or can choose between the two)
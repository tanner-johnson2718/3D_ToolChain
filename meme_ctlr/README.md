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

![alt text](MEME_Backend.png)

## Data store
The data store is a per printer data structure that maintains 2 data elements and 5 main functions. Data elements:
1) **Send Q.** The send Q holds a list of g code commands to be sent to the printer. The next command is sent only when the active command is ACKed by the printer. Each command is wrapped in Job class that holds timestamps for when its enqueued, sent, and ACKed. Finally, all responses from the printer from when the command is sent to when it is ACKed are stored with the command for logging purposes.
2) **State Map**. Tracks relavent state i.e. nozzle temp, target temps, current position, firware settings, etc. Holds a unique prefix and regex for parsing the responses that contain state information. **NOTE**, something to think about, state map could be used to define per printer gcode protocal if some printers implement a different gcode set.
These data elements are accessed through the following functions:
1) **push_next_send(command).** Pushing a gcode command onto the sendQ to be sent when ready
2) **wait_on_next_to_send().** Blocks until the printer is ready for the next command. Returns string of command to be sent.
3) **push_reponse_line(line).** Register a response from the printer to the data store. Parsing of state happens here.
4) **wait_on_next_response().** Blocks until a response from the printer has been recved. Returns most recent response string.
5) **get_state(key).** Returns current state value of the given key. **TODO**, flesh this call out more.

# TODO
* program stats and deal with unbounded sendQ
* Start up commands and macros
* Subcription system) I want parsed values from command x,y,z at a regular time interval
* Programmatic way of adding to the parsed command list i.e. state map
* send data over sockets instead of pipe (or can choose between the two)
# MEME Controller

G code sender, printer montoring and control, and interface for executing testing/calibration sequences.

# Serial Communication

* Sending and recv-ing commands is done through the USB serial port (/dev/ttyACM0 for skr mini E3 V3.0)
* Commands are send in ascii delimited by a new line char
* The command protocal is [G-code](../marlin/Marlin_Docs/_gcode/)
* All commands, if properly recv-ed by the printer, are ACK-ed with a response "ok" 

# Dependancies
* Python 3.8.10
* python-tk
* custom tkinter

# Backend Architecture

![alt text](MEME_Backend.png)

## Data store
The data store is a per printer data structure that maintains 2 data elements and 4 main functions. Data elements:

1) `sendQ` The send Q holds a list of g code commands to be sent to the printer. The next command is sent only when the active command is ACKed by the printer. Each command is wrapped in Job class that holds timestamps for when its enqueued, sent, and ACKed. Finally, all responses from when the command is sent to when it is ACKed are stored with the command for logging purposes.
2) `StateMap` Tracks relavent state i.e. nozzle temp, target temps, current position, firware settings, etc. Holds a unique prefix and regex for parsing the responses that contain state information.

These data elements are accessed through the following functions:

1) `push_cmd(command)` Pushes a gcode command onto the sendQ to be sent when ready
2) `wait_cmd()` Blocks until the printer is ready for the next command. Returns string of command to be sent.
3) `push_reponse(line)` Register a response from the printer to the data store. Parsing of state happens here.
4) `query(key)` Returns current state value of the given key. Keys are short state decriptions like `nozzle temp current`. `get_all_state_keys()` returns list of acceptable keys.

## Backend
Implements all IO.
* **Send/Recv Thread.** Blocks on IO from printer via serial and registers IO with the data store
* **Response Publisher.** Thread to push ALL unparsed responses from printer over a port. This could be a pipe for local debugging or a socket for a networed UI to capture.
* **Command Recv/Macro.** Thread to recv commands and macros over a port and push them to the send Q. **TODO** need to decide format for macros, how to add and how to delete them.
* **Sub Thread.** **TODO** flesh this out more along with get_state function to define API for subscribing to state.

### Network API
The applciation protocol for communicating with the back end follows the following. All packets are 64bytes. The end of a packets data section is padded with null bytes. 

| API Call | Example Packet Structure | Comments | 
| --- | --- | --- |
| Send Command | `\|c|m|d| |M|5|0|3|null|...|null|` | cmd in ascii followed by space followed by command (max 59 char) |
| Sub Reponses Request | `|s|u|b|R|<V>|null|...|null|` | subR in ascii followed by 0,1,2 ascii int. V=0 -> Dont sent serial input. V=1 -> Send serial input but filter out polled responses (like auto temp report). V=2 -> Send all serial input. |
* register macro
* deregister macro
* get all macros
* unsub to responses
* add response filter
* remove response filter
* see all filters
* sub to state
* unsub to state
* see all subs

# TODO
* program stats and deal with unbounded sendQ and logging
* macros
* Subcription system) I want parsed values from command x,y,z at a regular time interval
* send data over sockets instead of pipe (or can choose between the two)
* Filter response output
* SD stuff
* storing macros, filters, and command state map thingy
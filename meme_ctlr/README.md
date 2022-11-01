# MEME Controller

My G-code sener and printer controller, reversed engineered using pronsole as a baseline.

# Init notes

* Downloaded zip of pronterface python code at e60a93fd6c0216d57f5dc0a78118e89e9fda2d9a
* Want to customize for my own liking and/or reverse engineer whats being sent over the serial port
* printcore.py has main read / write from serial port
    * Make sure to read until an endline is reached
* pronsole implements a queue, and writes straight gcode in ascii to the serial port (import serial)
    * responses from the printer are again straight up binary encoded ascii
* **Will sending G-Code command by command over serial slow down the printer vs loading from internal SD**
    * If you send a long cmd like G28, then try to get data like M503, it responds with an error message
* **How does printrun send full g-code files?**

# First Stab at Meme Controller Architecture
* Use pySimpleGUI to create very basic UI
    * pip3 install pysimplegui
    * sudo apt-get install python3-tk
* Have text box to push commands (cmd interface)
* Have bigger text box to read output from printer
* Have key info section that polls printer for temp, etc
* All push (sending over serial) operate on a single thread
* All pull (recving over serial) again operate on single thread
* Each of the GUI features above add jobs to the push / pull threads to be executed
* Macros, mesh viz, etc all can be added using this basic framework
    * either by giving its own dedicated UI feature or through cmd interface
* **KEY MISSING FEATURE** how to send and monitor print jobs

# Current Architecture
* **NOTE** pysimplegui must run on main thread
* There are two concurrent threads: Main and Recver
* Main thread handles all events from gui, updates gui elements, and sends commands to printer based on gui events
    * GUI accessors enforce the constraint that only main can access GUI elements
* The recver thread blocks on reads from the printer and updates globals to reflect changes in printer state
* Access to globals is regulated by single semaphore
* Recver thread updates these globals, when the main thread runs it checks for updates and updates gui accordingly
* The exception to the above scheme is when pushing a file to the SD card on the printer:
    * A file in the local dir is typed into gui element
    * Load button is pushed
    * Recver thread is put into pause state
    * Automatic reports (i.e. temp) are suspended
    * File is read line by line and sent over serial
    * For each line (i.e. gcode command) the sender (main thread) waits for a ACK from the printer and then continues to next line
    * **NOTE** this is only time main thread reads from serial, otherwise its always the recv thread
* Main Thread Execution:
    * Set up program, gui, threads, etc.
    * Block on GUI events
        * 1 Sec timeout
        * On timeout no event is reported from gui, but recv thread may have updates to globals
    * Based on the event, other GUI elements may be read to check state.
        * based on this a command is usually sent to the printer
    * Finally update GUI elements to reflect current global status
    * Example) Update temp event is triggered. Read temp from text box. Send M104 SXX.XX, where XX.XX is updated temp
* Recver Thread Execution:
    * Wait for input from serial
        * 1 Second timeout
        * Only use case for time out is to check if the app has been killed
    * Attempt to parse out data we want to display
        * This requires attempting to parse out all info we expect to get on serial port
    * If a recvieved line has data we want to display, update the corresponding global value
    * **NOTE** one key exception to this is if data (like mesh table) is presented over multiple lines
        * in this case we look for the first line of this multi line response
        * then in a seperate read statement, read lines until all lines of the data we want has come through
        * care must be taken to make sure we dont get stuck, if the app is killed, waiting for the multi line responses
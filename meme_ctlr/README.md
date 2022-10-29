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

# Final Architecture
* **NOTE** pysimplegui must run on main thread
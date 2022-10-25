# MEME Controller

My G-code sener and printer controller, reversed engineered using pronsole as a baselie.

# Init notes

* Downloaded zip of pronterface python code at e60a93fd6c0216d57f5dc0a78118e89e9fda2d9a
* Want to customize for my own liking and/or reverse engineer whats being sent over the serial port
* printcore.py has main read / write from serial port
* pronsole implements a queue, and write straight gcode in ascii to the serial port (import serial)
* **Will sending G-Code command by command over serial slow down the printer vs loading from internal SD**
* **How does printrun send full g-code files?**
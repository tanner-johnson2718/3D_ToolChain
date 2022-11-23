# Calibration Test Prints
## Z_Off_Test)
Print a 50mmX50mmX1mm square at slow speed in center of build plate. This print is just a simple test to verify printer works and Z offset is close. While printing fine tune Z offset. Best way to get an initial Z offset is the following)
    * Set Z off to 0.0.
    * Home
    * Turn off end stops with M211 S0
    * Move to Z0
    * Decrment Z until its where you want (i.e could use feeler gauge to get precise distance from nozzle to build plate) i.e. G0 Z-1.0, G0 Z-2.0, ...
    * Store that Z value as Z off
    * Turn on end stops M211 S1
## Level_Test)
Print 25mmX25mmx1mm squares at center and at four corners near edges of build plate. Verify good bed adhesion and proper z offset at four corners. This test just verifies the ABL is functioning properly.

## Temp_Tower)
Slice temp tower STL using current printer configs. Use the temp_adjust.py script to insert temp adjustments at the layers where temp is supposed to change. Printed object should show what temp is optimal.

##  Retraction_Spikes)
##  Geometric_Accuracy) 
Print 10mmx10mmx10mm cube. Use Calipers to measure accuracy. Adjust Steps per mm accordingly.
## Speed_Test) 
## Acceleration_CTRL) 
## Line_Width_Test)
## Flow_Rate_Test) 

# Key Calibration Parameters (GCode and Slicer configurable only)
| Parameter | Description | Value Ranges | Current Values | Comments |
| --- | --- | --- | --- | --- |
| Z offset | Affects distance of nozzle to bed | [-4.0mm, 0.0mm] | -3.00mm | Changing nozzle resets this. Nozzle size, line width and flow rate will affect the optimal value |
| Line Width | How wide each line of plastic is | +/- 50% of nozzle size | - | Can be used to get the affect of smaller / larger nozzle sizes without actually changing nozzles. When line width > nozzle diameter, increasing temp and flow rate can help |
| Flow Rate | - | - | - | - |
| Wall Width | - | - | - | - |
| Top / Bottom Width | - | - | - | - |
| Retract Distance | - | - | - | - |
| Retract Rate | - | - | - | - |
| Print Speed | - | - | - | - |
| Travel Speed | - | - | - | - |
| Fan Speed | - | - | - | - |
| Steps per mm | - | - | - | - |
| Linear Advance Settings?? | - | - | - | - | 
| Acceleration Settings?? | - | - | - | - |

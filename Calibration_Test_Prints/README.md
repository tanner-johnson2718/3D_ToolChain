# Calibration Test Prints
* Z_Off_Test) Just print square 50mmX50mmX1mm square at slow speed in center of build plate. This print is just a simple test to verify printer works and Z offset is close. While printing fine tune Z offset. Best way to get init Z off the following)
    * Set Z off to 0.0.
    * Home
    * Turn off end stops with M211 S0
    * Move to Z0
    * Decrment Z until its where you want (i.e could use feeler gauge to get precise distance from nozzle to build plate) i.e. G0 Z-1.0, G0 Z-2.0, ...
    * Store that Z value as Z off
    * Turn on end stops M211 S1
* Level_Test) 
* Temp_Tower)
* Retraction_Spikes)
* Geometric_Accuracy) Print 10mmx10mmx10mm cube. Use Calipers to measure accuracy. Adjust Steps per mm accordingly.
* Speed_Test) 
* Acceleration_CTRL) 
* Line_Width_Test)
* Flow_Rate_Test) 

# Key Calibration Parameters (GCode and Slicer configurable only)
| Parameter | Description | Value Ranges | Known Good Values (Of Current Set Up) | Comments |
| --- | --- | --- | --- | --- |
| Z offset | Affects distance of nozzle to bed | [-4.0mm, 0.0mm] | [-3.75mm, -3.95mm] | Changing nozzle resets this. Nozzle size, line width and flow rate will affect the optimal value |
| Nozzle Diameter | - | - | -| - |
| Line Width | - | - | - | - |
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

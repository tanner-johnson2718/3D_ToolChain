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

On the printed square, the print lines should overlap and form a uniform square of material. Watch for rough tough top finish (too close) and gaps in lines (too far).

## Level_Test)
Print 25mmX25mmx1mm squares at center and at four corners near edges of build plate. Verify good bed adhesion and proper z offset at four corners. This test just verifies the ABL is functioning properly.

## Temp_Tower)
Slice temp tower STL using current printer configs. Use the temp_adj.py script to insert temp adjustments at the layers where temp is supposed to change. Printed object should show what temp is optimal (minimal stringing, cleanest extrusions, crisp letters, etc). The included file, 180-200_PLA_Temp_calibration.stl has the following tempature transistions

| Temp | Layers |
| --- | --- |
| 220 | 0 - 40 |
| 215 | 40 - 75 |
| 210 | 75 - 105 |
| 205 | 105 - 140 |
| 200 | 140 - 175 |
| 195 | 175 - 205 |
| 190 | 205 - 240 | 
| 185 | 240 - 275 |
| 180 | 275 - 310 |

##  Retraction_Spikes)
Slice Retraction_Spikes.stl with current retraction settings. Print and observe stingy-ness, pooling, under/over extrusion, etc. Adjust accordingly. 

##  Geometric_Accuracy) 
Print 10mmx10mmx10mm cube. Use Calipers to measure accuracy. Adjust Steps per mm accordingly. Similarly to calibrate the E steps per mm, mark a point on filament roll just below extruder. Extrude a set amount of filament i.e. 10mm. Measure how much marked point moved. Adjust steps per mm accordingly.

## Speed_Test) 
## Acceleration_CTRL) 
## Line_Width_Test)
## Flow_Rate_Test) 

# Key Calibration Parameters (GCode and Slicer configurable only)
| Parameter | Description | Value Ranges | Current Values | Comments |
| --- | --- | --- | --- | --- |
| Z offset | Affects distance of nozzle to bed | [-4.0mm, 0.0mm] | -3.00mm | Changing nozzle resets this. Nozzle size, line width and flow rate will affect the optimal value |
| Line Width | How wide each line of plastic is | +/- 50% of nozzle size | - | Can be used to get the affect of smaller / larger nozzle sizes without actually changing nozzles. When line width > nozzle diameter, increasing temp and flow rate can help |
| Nozzle Diameter | Not a parameter but size of nozzle is good to track | .2mm - 1.0mm | .4mm | - |
| Temp | Depends on materail. Current values for PLA | 180 - 220 | 180 | 180 for percise prints |
| Retract Distance | How many mm's of filament is sucked back up the nozzle on a retraction | 2mm - 10mm | 5mm | At 180C, print speed of 80mm/s, travel speed of 200mm/s, these retraction settings worked very well. Uping print speed and temp may make these settings insuffcient (might need faster and longer retractions) |
| Retract Rate | How fast the filament is retracted | 10mm/s - 45mm/s | 45mm/s | At 180C, print speed of 80mm/s, travel speed of 200mm/s, these retraction settings worked very well |
| Flow Rate | - | - | - | - |
| Wall Width | - | - | - | - |
| Top / Bottom Width | - | - | - | - |
| Print Speed | - | - | - | - |
| Travel Speed | - | - | - | - |
| Fan Speed | - | - | - | - |
| Steps per mm | - | - | - | - |
| Linear Advance Settings?? | - | - | - | - | 
| Acceleration Settings?? | - | - | - | - |

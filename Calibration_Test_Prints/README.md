# Calibration Test Prints
## Z_Off_Test)
Print a 50mmX50mmX1mm square at slow speed in center of build plate. This print is just a simple test to verify printer works and Z offset is close. While printing fine tune Z offset. Best way to get an initial Z offset is the following)
* Set Z off to 0.0.
* Home
* Turn off end stops with M211 S0
* Move to Z0
* Decrment Z until its actually at 0 i.e. touching the build plate
    * Can check 0 with feeler gauge. When Z off is close, set G0 Z0.5. Then check that a 0.5mm feeler gauge fits snuggly between nozzle and build plate
* Store that Z value as Z off
* Turn on end stops M211 S1

On the printed square, the print lines should overlap and form a uniform square of material. Watch for rough tough top finish (too close) and gaps in lines (too far).

## Level_Test)
Print 25mmX25mmx1mm squares at center and at four corners near edges of build plate. Verify good bed adhesion and proper z offset at four corners. This test just verifies the ABL is functioning properly.

## Temp_Tower)
Slice temp tower STL using current printer configs. Use the temp_adj.py script to insert temp adjustments at the layers where temp is supposed to change. Printed object should show what temp is optimal (minimal stringing, cleanest extrusions, crisp letters, etc). Temp tower STLs included in this directory.

| Temp (PLA) | Temp (PETg) | Layers |
| --- | --- | ---
| 220 | 260 | 0 - 40 |
| 215 | 255 | 40 - 75 |
| 210 | 250 | 75 - 105 |
| 205 | 245 | 105 - 140 |
| 200 | 240| 140 - 175 |
| 195 | 235 | 175 - 205 |
| 190 | 230 | 205 - 240 | 
| 185 | 225 | 240 - 275 |
| 180 | 220| 275 - 310 |

##  Retraction_Spikes)
Slice Retraction_Spikes.stl with current retraction settings. Print and observe stingy-ness, pooling, under/over extrusion, etc. Also look closely at layer end lines as this where retractions occur. Adjust accordingly. 

##  Geometric_Accuracy) 
Print 10mmx10mmx10mm cube. Use Calipers to measure accuracy. Adjust Steps per mm accordingly. Similarly to calibrate the E steps per mm, mark a point on filament roll just below extruder. Extrude a set amount of filament i.e. 10mm. Measure how much marked point moved. Adjust steps per mm accordingly.

## Speed_Test) 
## Acceleration_CTRL) 
## Line_Width_Test)
## Flow_Rate_Test) 

# Current Calibration Parameters (GCode and Slicer configurable only)
| Parameter | Description | Value Ranges | Current Values | Comments |
| --- | --- | --- | --- | --- |
| Nozzle Diameter | Not a parameter but size of nozzle is good to track | .2mm - 1.0mm | .4mm | Brass |
| Z offset | Additive modifier such that at Z=0, the nozzle is just touching the bed | [-4.0mm, 0.0mm] | -1.75 | Check this when changing nozzles, or messing with hot end |
| Line Width | How wide each line of plastic is | +/- 50% of nozzle size | .3mm - .5mm | Can be used to get the affect of smaller / larger nozzle sizes without actually changing nozzles. When line width > nozzle diameter, increasing temp and flow rate can help |
| Nozzle Temp | Depends on material. Current values for PETg | 220 - 260 | 240 | Lower end gives better retraction but worse inital layer bed adhesion and under extrusion |
| Bed Temp | Temp of heated bed | 50 - 80 | 75 | PLA 50-60, PETg 70-80 | 
| Retract Distance | How many mm's of filament is sucked back up the nozzle on a retraction | 2mm - 10mm | 6mm | - |
| Retract Rate | How fast the filament is retracted | 10mm/s - 80mm/s | 35mm/s | - |
| Fan Speed | % Load on part cooling fan | 0 - 100 | 0 | Usually PETg does not need a fan but helps with briding and details |
| Print Speed | Speed while extruding | 10mm/s - 200mm/s | 40mm/s - 80mm/s | - |
| Travel Speed | Speed while not extruding (traveling) | 50mm/s - 250mm/s | 40mm/s - 100mm/s | - |
| Init Layer Print Speed | Speed while extruding on first layer | 5mm/s - 40mm/s | 15mm/s | - |
| Init Layer Travel Speed | Speed while not extruding on first layer | 5mm/s - 80mm/s | 40mm/s | On prints with long travels, if this value is too low it can cause oozing |
| Wall Width | Number of wall lines | 2-5 | 4 | Take the line width and multiply by number of walls to get wall width in mm |
| Top / Bottom Width | Number of top and bottom lines | 2-5 | 4 | Take the layer height and multiply by number of walls to get wall width in mm |
| Flow Rate | - | - | - | - |
| X,Y,Z Steps per mm | - | - | - | - |
| E Steps per mm | - | - | - | - |
| Linear Advance Settings?? | - | - | - | - | 
| Acceleration Settings?? | - | - | - | - |

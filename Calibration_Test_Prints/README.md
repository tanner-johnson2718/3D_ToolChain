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

## PID Tuning

PID tuning calibrates the heat / cool cycle used to keep the heated elements of the printer at a constant temp. This should be done infrequently, however, it should be done if making modifcations to the, bed, hot end, or anything affecting the thermal or electrical systems of the printer.

```
M303 E0 C8 S240 U ;PID tune nozzle heater 0, 8 cycles, target temp 240 and use the result
M303 E-1 C8 S75 U ;PID tune bed heater 0, 8 cycles, target temp 240 and use the results
M500 ;Save to EEPROM 
M501 ;Load from EEPROM
```

## Speed_Test) 
## Acceleration_CTRL) 
## Line_Width_Test)
## Flow_Rate_Test) 

# Current Calibration Parameters (GCode and Slicer configurable only)
| Parameter | Description | Value Ranges | Current Values | Comments |
| --- | --- | --- | --- | --- |
| Nozzle Diameter | Not a parameter but size of nozzle is good to track | .2mm - 1.0mm | .4mm | Brass |
| Layer Height | Height of individual layer of plastic | .1mm - .32mm | .16mm - .32mm | Affects quality and is a function of the nozzle size |
| Initial Layer Height | Height of individual layer of plastic on first layer | .1mm - .32mm | .16mm - .32mm | Same as above but can make this value smaller  |
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
| Fade Height | - | - | - | - |
| Velocity | - | - | - | - |
| Acceleration Settings?? | - | - | - | - |
| Jerk Settings | - | - | - | - |
| Linear Advance Settings?? | - | - | - | - | 

## Starter G-Code

```
M201 X500.00 Y500.00 Z100.00 E5000.00 ;Setup machine max acceleration
M203 X500.00 Y500.00 Z10.00 E50.00 ;Setup machine max feedrate
M204 P500.00 R1000.00 T500.00 ;Setup Print/Retract/Travel acceleration
M205 X8.00 Y8.00 Z0.40 E5.00 ;Setup Jerk
M220 S100 ;Reset Feedrate
M221 S100 ;Reset Flowrate

G28 ;Home
G29 A ; Verify UBL is activated
G29 L0 ; Load last saved mesh

G92 E0 ;Reset Extruder
G1 Z2.0 F3000 ;Move Z Axis up
G1 X10.1 Y20 Z0.28 F5000.0 ;Move to start position
G1 X10.1 Y200.0 Z0.28 F1500.0 E15 ;Draw the first line
G1 X10.4 Y200.0 Z0.28 F5000.0 ;Move to side a little
G1 X10.4 Y20 Z0.28 F1500.0 E30 ;Draw the second line
G92 E0 ;Reset Extruder
G1 Z2.0 F3000 ;Move Z Axis up
```

## Ending G-Code
```
G91 ;Relative positioning
G1 E-2 F2700 ;Retract a bit
G1 E-2 Z0.2 F2400 ;Retract and raise Z
G1 X5 Y5 F3000 ;Wipe out
G1 Z10 ;Raise Z more
G90 ;Absolute positioning

G1 X{machine_width} Y{machine_depth} ;Present print
M106 S0 ;Turn-off fan
M104 S0 ;Turn-off hotend
M140 S0 ;Turn-off bed

M84 X Y E ;Disable all steppers but Z
```
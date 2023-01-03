# Calibration Test Prints
## Z_Off_Test
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

### Probe offset
Marlin stores the distance from the probe to the nozzle in the probe offset `M851`. The Z value of the value of this command is configured with the routine above. The X and Y values should not change and should be verified with calipers.

## Level_Test
**Note** before leveling ensure both Z-rods are equidistance from the buildplate.

Print 25mmX25mmx1mm squares at center and at four corners near edges of build plate. Verify good bed adhesion and proper z offset at four corners. This test just verifies the ABL is functioning properly. Printing this is usually unnessacsy unless there is good reason to believe the ABL is not working. See below for guidance on leveling using the ABL system

### UBL Basic

UBL will measure the bed distance on a mesh and correct any deviations. Below is the GCODE sequence to execute this process, measure the mesh, and store it. Also be sure to have the temp of bed and nozzle stable during this procedure at what ever printing temp you plan to use.

```
G28          ;Home
G29 P1 V4 T0 ;Measure full mesh, full verbosity and output human readable table
G29 S0       ;Store mesh in slot 0
G29 A        ;Activate UBL
M500         ;Save current mesh in EEPROM
```

### UBL Corner Mesh Measuring (Tramming)

To assist in adjusting the 4 Corners of the bed one can run the following procedure. This will not store any mesh data it will simple measure the 4 corners and output the Z delta. X and Y values were chosen to get the probe reasonably close the points of adjustment. Following this procedure, run a full bed level to save the mesh as described above. Also be sure to have the temp of bed and nozzle stable during this procedure at what ever printing temp you plan to use.

```
G28 ;Home
G30 X30 Y50   ;Front Left
G30 X310 Y50  ;Front Right (Can only get so close given )
G30 X30 Y325  ;Back Left
G30 X310 Y325 ;Back Right
```

**NOTE** The goal here is NOT to get the Z values close to 0, its to get them as close to each other as possible. Z = 0 is measured at center of build plate not the corners.

## Linear Extrusion Test

After tuning the Z offset and ensuring a level Bed, on can do a simple test to verify the above and make sure filament will stick to the bed. This can be done by simply extruding a line of material onto the bed (at various locations if one so chooses). To do this we need to specify the following values:

* $d_f$ : Diameter of filament (usually 1.75mm)
* $w$ : Line width (usually nozzle diameter, see [below](#slicer-setting))
* $h$ : Layer height
* $L$ : The length of the linear movement

Assume a rectangluar cross section as Cura does (other slicers such as Slic3r uses a different cross section [calculation](https://manual.slic3r.org/advanced/flow-math)). Now the amount of material we need to extrude, $E$ is calculated as the following.


$$\pi \frac{d_f^2}{4} E = wh(L - w)$$

This simply states the volume of the material inputed through the extruder needs to equal the volume of the line we intend to draw. The term $(L-w)$ is to compensate for the fact that the nozzle does travel the entire length of the extruded line, it starts and stop half a line width away from the limits of the line. So,

$$ E = \frac{4wh(L-w)}{\pi d_f^2} $$

Now we can execute the following gcode to test a single line extrusion. Assume have the following inputs)

* T_b is the temp of the bed
* T_n is the temp of the nozzle
* X_i is the x pos of the start of the line
* X_f is the x pos of the start of the line
* Y_i is the y pos of the start of the line
* Y_f is the y pos of the start of the line
* V_t is the travel velocity in mm/s
* V_p is the printing velocity in mm/s
* V_r is the retraction velocity
* R is the retraction distance

```
G28     ;Home
G29 A   ;Activate UBL
G29 L0  ;Load saved mesh

M140 S{T_b}  ;Set Bed Temp
M104 S{T_n}  ;Set Nozzle Temp
M190 S{T_b}  ;Wait for bed to reach temp
M109 S{T_n}  ;Wait for Nozzle to reach temp

M82    ;absolute extrusion mode
G92 E0 ;Reset extrusion counter
G0 X{X_i +- w/2} Y{Y_i +- w/2} Z{LAYER_HEIGHT} F{60*V_t} ;Determine +- based on travel direction
G1 X{X_f -+ w/2} Y{Y_f -+ w/2} E{E} F{60*V_p}
G1 E{E-R} F{60*V_r}

G91
G0 X5 Y5 Z5
G90
G0 X180 Y25 Z10
```

## Temp_Tower
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

##  Retraction_Spikes
Slice Retraction_Spikes.stl with current retraction settings. Print and observe stingy-ness, pooling, under/over extrusion, etc. Also look closely at layer end lines as this where retractions occur. Adjust accordingly. 

##  Geometric_Accuracy
Print 10mmx10mmx10mm cube. Use Calipers to measure accuracy. Adjust Steps per mm accordingly. Similarly to calibrate the E steps per mm, mark a point on filament roll just below extruder. Extrude a set amount of filament i.e. 10mm. Measure how much marked point moved. Adjust steps per mm accordingly.

## PID Tuning

PID tuning calibrates the heat / cool cycle used to keep the heated elements of the printer at a constant temp. This should be done infrequently, however, it should be done if making modifcations to the, bed, hot end, or anything affecting the thermal or electrical systems of the printer.

```
M303 E0 C8 S240 U ;PID tune nozzle heater 0, 8 cycles, target temp 240 and use the result
M303 E-1 C8 S75 U ;PID tune bed heater 0, 8 cycles, target temp 240 and use the results
M500 ;Save to EEPROM 
M501 ;Load from EEPROM
```

## Speed_Test
## Acceleration Test
## Cornering Test

# Calibration and Settings Table

## Slicer Setting

The following settings are usually set in the slicer and will change frequently from print to print and material to material

| Parameter | Description | Value Ranges | Current Values | Comments |
| --- | --- | --- | --- | --- |
| Nozzle Diameter | Not a parameter but size of nozzle is good to track | .2mm - 1.0mm | .4mm | Brass |
| Layer Height | Height of individual layer of plastic | .1mm - .32mm | .16mm - .32mm | Affects quality and is a function of the nozzle size |
| Initial Layer Height | Height of individual layer of plastic on first layer | .1mm - .32mm | .16mm - .32mm | Same as above but can make this value smaller to get better squish on first layer |
| Z offset | Additive modifier such that at Z=0, the nozzle is just touching the bed | [-4.0mm, 0.0mm] | -1.75 | Check this when changing nozzles, or messing with hot end |
| Line Width | How wide each line of plastic is | +/- 50% of nozzle size | .3mm - .5mm | Can be used to get the affect of smaller / larger nozzle sizes without actually changing nozzles. When line width > nozzle diameter, increasing temp and flow rate can help |
| Nozzle Temp | Depends on material. Current values for PETg | 220 - 260 | 230 | Lower end gives better retraction but worse inital layer bed adhesion and under extrusion |
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

## Firmware Settings
| Parameter | Description | Value Ranges | Current Values | Comments |
| --- | --- | --- | --- | --- |
| X,Y,Z and E Steps per mm | Mechanical parameters that set by the gear ratios of the stepper motors. Determine how many steps executed by the motor correspond to a mm of linear movement on a given axix | Always 80,80,800 for XYZ, E is in around 93 | 80,80,800,93 | The E steps can change based on the material. The depth at which the extruder grabs the plastic will change this value |
| Fade Height | Bed Leveling will compensate for bed divations. At which height the firmware stops accounting for these is the fade height | 2-10mm | 2mm | If there is no fade bed deviations will propegate geometric errors |
| Max Velocity | Max linear velocity of all axis | XY: [250,500] Z:[5,15] E:[35,100] | 250,250,10,50 | - |
| Max Acceleration Settings | Max acceleration of all axis | XY: [1000,5000] Z:[50,100] E:[1000,10000] | 1000,1000,50,1000 | - |
| Print Acceleration | The acceleration it uses to print | See max Acceleration | 200 | - |
| Travel Acceleration | The acceleration it uses to travel | See max Acceleration | 200 | - |
| Retract Acceleration | The acceleration it uses to travel | See max Acceleration | 200 | - |
| Junction Deviation?? | - | - | - | - |
| Min Segment Time?? | - | - | - | - |
| Min Feedrate?? | - | - | - | - |
| Min Travel Feedrate?? | - | - | - | - |
| Linear Advance Settings?? | - | - | - | - | 

## Starter G-Code

```
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
G1 E-5 F2700 ;Retract a bit
G1 E-5 Z0.2 F2400 ;Retract and raise Z
G1 X5 Y5 F3000 ;Wipe out
G1 Z10 ;Raise Z more
G90 ;Absolute positioning

G1 X180 Y25;Present print
M106 S0 ;Turn-off fan
M104 S0 ;Turn-off hotend
M140 S0 ;Turn-off bed

M84 X Y E ;Disable all steppers but Z
```
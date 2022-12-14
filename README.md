# 3D Printing Tool Chain (Custom Ender 5 Plus)
Repo to hold scripts, source, designs, and config files for my 3D printing tool chain targeting an Ender 5 Plus. Also this repository will hold any modifications made to the printer. As of current, the modifications will be targeted towards the following requirements and end goals)

1) Print to tempatures up to 300C.
2) Maintain a chamber a chamber tempature up to  50C - 70C.
3) Chamber Heater and Enclosure of Printer.
4) Filament Dehydrator.
5) Custom Firmware, printer interface, and electronics to manage the printer and periphals and to give debug / developer control over all aspects and subsystems of the printer.
6) Suite of configuration and calibrations scripts to control and tune printer.

The end goal of this project is a a printer capable of printing higher temp plastics. Nylon is the ultimate goal, however PP and PC are possible. Secondary goal is simply education and understanding every aspect of the 3D printing process from slicing to the printer interface to the firmware and finally the mechanical and electrical aspects of 3D printing. A teritary goal is simply a printer, build from the ground up with as many custom features that target what I want out of my 3D printer.

## 3rd Party tools used

* FreeCAD 0.20 for 3D modeling
* OpenSCAD 2019.05 for programmatic 3D modeling
* Cura 5.0 for slicing 
* Platfrom IO VS code extension for building Marlin 

## Modifications, Current Hardware, and project directory

### Modifications and Project Directory

| Proejct | Date | Comment |
| --- | --- | --- |
|  [Slicer Settings, Calibration, and Test Prints](Calibration_Test_Prints) | Oct 2022 - | Holds documentation on settings/configurations (both firmware and slicer settings). Also has test prints and procedures for calibrating the printer. |
| [MEME Controller](MEME_CTLR) | Oct 2022 - | G code sender and print monitor.  |
| [Electronics Enclosure](Printer_Mods/Electronic_Enclosure) | Oct 2022 - Jan 2023 | Removed PSU and main board, printing custom enclosure to move electronics out from underneath printer and support printer customization and additional features i.e. chamber heater, dehydrator, etc. |
| [Custom Marlin Firmware](Marlin) | Dec 2022 - | **TODO** Need to think about how to document, modify, and track firmware changes |
| :heavy_check_mark: [Designs](Designs) | Dec 2022 | FreeCad Scripts and generic designs, images, and models used for 3D printing and likely to be used in more than a singular project |
| :heavy_check_mark: [Cable Track Wire Management System](Printer_Mods/Cable_Track) | Nov 2022 | [Stole from Reddit](https://www.reddit.com/r/ender5plus/comments/so2ulf/ender_5_plus_cable_chain_solution/) |


### Current Hardware
| Component | Date Installed | Comment |
| --- | --- | --- |
| Mother board | Jan 2023 | SKR Mini E3 V3. [Pinout](DataSheets/BTT%20E3%20SKR%20MINI%20V3.0_PIN.pdf). [Block Diagram](DataSheets/BTT%20E3%20SKR%20MINI%20V3.0_SCH.pdf). [MCU](DataSheets/stm32g0b1cc-2042221.pdf) |
| PSU | - | [Stock Meanwell RSP-500-24](DataSheets/MeanWell_500_Datasheet.pdf) |
| Extruder | Sept 2022 | Creality All metal Extruder https://www.amazon.com/dp/B07ZMFP2L8?psc=1&ref=ppx_yo2ov_dt_b_product_details |
| Steppers | - | Stock |
| Stepper Drivers | - | Stock |
| Bowden Tube | Sept 2022 | Capicorn XS https://www.captubes.com |
| Base Hot end | Nov 2022 | Micro Swiss All metal hot end https://store.micro-swiss.com/collections/all-metal-hotend-kits/products/all-metal-hotend-kit-for-cr-10 |
| Hot end Thermistor | Jan 2023 | https://www.amazon.com/dp/B0714MR5BC?psc=1&ref=ppx_yo2ov_dt_b_product_details. Has JST quick Connect. |
| Heater Cartridge | - | Stock 40W, Adding standard 20 AWG quick connects to make changing hotend faster. |
| Hot end fan and part cooler | Jan 2023 | https://www.amazon.com/gp/product/B08N8YDQCD/ref=ppx_yo_dt_b_asin_title_o00_s01?ie=UTF8&psc=1. Adding JST male and female at hot end. |
| External Bed Mosfett | Nov 2022 | Mosfet FYSETC https://www.amazon.com/dp/B07C4PGXFK?psc=1&ref=ppx_yo2ov_dt_b_product_details |
| Part Cooler | - | Stock |
| ABL | - | Stock BL Touch |
| X Gantry | - | Stock |
| Y Guides | - | Stock |
| Z Rails | Sept 2022 | Stock w/ Z axis POM Lead nut and spring https://www.amazon.com/dp/B07XYR3F4C?psc=1&ref=ppx_yo2ov_dt_b_product_details |

## Tasking

### Testing / calibration
* meme ctlr custom extrustion
    * Straight Line
    * L shape with specified angle
    * Extrusion multiplier, how does cura do it?
* Calibration flow rate doc and tests + calibration doc

### Enclosure
* Cut aluminum and plexiglass
* Make window panels a door instead

### MEME CTLR
#### V1.0
* SD stuff
    * Need to make it so in backend, a single read from the socket may contain several API calls
* Bed trammig Bed X:.. not showing up with filter
* //action heating bed not showing up with filter
* When un subbing, a MXXX S0 isnt sent

#### v2.0
* New idea, create set of scripts that connect to the backend for various activities
    * Would need to make backend more resillant to disconnecting of client, printer, etc...
* Make all subs Auto??
    * If we do this, then we need to change the way we sub to state i.e. sub to a command not a value
    * Make SD print progress an auto sub
* Remote Firmware writes??
    * requies binary transfer in marlin
* Make Printer resillant to serail connects and disconnects, failed or restarting a print, printer lossing power, printer loosing contact w/ controller, etc.

### Printer mods
* PETg hotend fan mount mount
* Open Problems and Questions for next iter of electronics, enclosure , dehydrator
    * ammeters
    * Chamber heater and extra thermistors?
    * SD Card and mini usb access
    * LEDs?
    * Raspberry PI??
    * dehydrator and storage box
    * 3D printed enclosure
    * Migrate to Klipper??
# 3D Printing Tool Chain (Custom Ender 5 Plus)
Repo to hold scripts, source, and config files for 3D printing tool chain targeting an Ender 5 Plus. Also this repository will hold any modifications made to the printer. As of current, the modifications will be targeted towards the following requirements)

1) Print to tempatures up to 300C
2) Maintain a chamber a chamber tempature up to  50C - 70C
3) Custom Firmware and Interface to printer, allowing custom features, more in depth monitoring of harwdare and software, and rapid implementaion of custom features (**This is a bad requirement needs to be refined**) 

The end goal of this project is a a printer capable of printing higher temp plastics. Nylon is the ultimate goal, however PP and PC are possible. Secondary goal is simply education and understanding every aspect of the 3D printing process from slicing to the printer interface to the firmware and finally the mechanical and electrical aspects of 3D printing.

## 3rd Party tools used

* FreeCAD 0.20 for 3D modeling
* Cura 5.0 for slicing 
* Arduino IDE 2.0.3 for building and flasing ATMega 2560 on main control board |

## Modifications, Current Hardware, and project directory

### Modifications and Project Directory

| Proejct | Date | Comment |
| --- | --- | --- |
| [Electronics Enclosure](Printer_Mods/Electronic_Enclosure) | Oct-Dec 2022 | Removed PSU and main board, printing custom enclosure to move electronics out from underneath printer. Wiring diagrams, electrical specs, and pinout diagrams can all be found there as well. |
| [Cable Track management system](Printer_Mods/Cable_Track) | Nov 2022 | [Stole from Reddit](https://www.reddit.com/r/ender5plus/comments/so2ulf/ender_5_plus_cable_chain_solution/) |
| [MEME Controller](meme_ctlr) | Oct 2022 - | G code sender and print monitor.  |
| [Slicer Settings, Calibration, and Test Prints](Calibration_Test_Prints) | Oct 2022 - | Holds documentation on settings/configurations (both firmware and slicer settings). Also has test prints and procedures for calibrating the printer. |
| [Custom Marlin Firmware](marlin) | Dec 2022 - | **TODO** Need to think about how to document, modify, and track firmware changes |


### Current Hardware


| Component | Date Installed | Comment |
| --- | --- | --- |
| Mother board | - | Stock Melzi v2.2 [Pinout](Printer_Mods/Electronic_Enclosure/melzi_pinout.jpg) and [ATMega2560 Datasheet](Printer_Mods/Electronic_Enclosure/Datasheets/ATmega2560_Datasheet.pdf) and [Adruino Mega pinout mapping](Printer_Mods/Electronic_Enclosure/Datasheets/Arduino-Mega-Pinout.jpg) (when programming in the Arduino IDE use these pins as a reference) |
| PSU | - | [Stock Meanwell RSP-500-24](Printer_Mods/Electronic_Enclosure/MeanWell_500_Datasheet.pdf) |
| Extruder | Sept 2022 | Creality All metal Extruder https://www.amazon.com/dp/B07ZMFP2L8?psc=1&ref=ppx_yo2ov_dt_b_product_details |
| Steppers | - | Stock |
| Stepper Drivers | - | Stock |
| Bowden Tube | Sept 2022 | Capicorn XS https://www.captubes.com |
| Hot end | Nov 2022 | Micro Swiss All metal hot end https://store.micro-swiss.com/collections/all-metal-hotend-kits/products/all-metal-hotend-kit-for-cr-10 |
| Hot end Thermistor | Nov 2022 | https://www.amazon.com/dp/B0714MR5BC?psc=1&ref=ppx_yo2ov_dt_b_product_details |
| External Bed Mosfett | Nov 2022 | Mosfet FYSETC https://www.amazon.com/dp/B07C4PGXFK?psc=1&ref=ppx_yo2ov_dt_b_product_details |
| Part Cooler | - | Stock |
| ABL | - | Stock BL Touch |
| X Gantry | - | Stock |
| Y Guides | - | Stock |
| Z Rails | Sept 2022 | Stock w/ Z axis POM Lead nut and spring https://www.amazon.com/dp/B07XYR3F4C?psc=1&ref=ppx_yo2ov_dt_b_product_details |

## Tasking
* meme ctlr custom extrustion
    * Straight Line
    * L shape with specified angle
    * Circle (how does cura do this)
    * Hows does accel control work in cura (corning)
* Calibration flow rate doc and tests
* meme ctlr re-org code.
    * Make a central key map to hold all globals, their keys and any gui elements
* meme ctlr refine doc
* enclosure finish cad and look into ammeters
* Cut t slot Al for elctronics enclosure
* Get running with skr board
* enclosure doc fan and go over power draw doc (i.e. board, heated bed, etc)

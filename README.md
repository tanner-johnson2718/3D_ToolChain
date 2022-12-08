# 3D Printing Tool Chain (Custom Ender 5 Plus)
Repo to hold scripts, source, and config files for 3D printing tool chain targeting an Ender 5 Plus. Also this repository will also hold any modifications made to the printer. As of current, the modifications will be targeted towards the following requirements)

1) Print to tempatures up to 300C
2) Maintain a chamber a chamber tempature up to  50C - 70C
3) Custom Firmware and Interface to printer, allowing custom features, more in depth monitoring of harwdare and software, and rapid implementaion of custom features (**This is a bad requirement needs to be refined and tareted with a broad but measurable goal**) 

The end goal of this project is a a printer capable of printing higher temp plastics. Nylon is the ultimate goal, however PP and PC are possible. Secondary goal is simply education and understanding every aspect of the 3D printing process from slicing to the printer interface to the firmware and finally the mechanical and electrical aspects of 3D printing.

## Tool Chain
The tools listed in the table below are used to operate, maintain, and modify the 3D printer.

| Tool | Version | Comments, Add ons, etc. |
| ---  | ---  | --- |
| FreeCAD for 3D modeling | 0.20 | No plans to modify or dig into this aspect of the tool chain |
| Cura for slicing | 5.0 | See [Calibration](Calibration_Test_Prints) for current slicer settings comments on these settings |
| [MEME CTLR](meme_ctlr) | - |Custom g code sender and printer serial monitor. This is the UI for the printer as modifcations required a custom interface. Also plan to integrate testing g-code generation into the interface |
| [Custom Marlin Firmware](marlin) | 2.1 bug fix | - |
| Arduino IDE | 2.0.3 | For building and flasing ATMega 2560 on main control board |

## Modifications, Current Hardware, and project directory

### Modifications and Project Directory

| Proejct | Date | Comment |
| --- | --- | --- |
| Electronics Enclosure | Oct-Dec 2022 | Removed PSU and main board, printing custom enclosure to move electronics out from underneath printer, see [Printer_Mods/Electronic_Enclosure](Printer_Mods/Electronic_Enclosure). Wiring diagrams, electrical specs, and pinout diagrams can all be found there as well. Added the physical infastructure to start using unused pins on the Melzi board (ATmega 2560) and to support current draw monitoring, a chamber heater, and a filament drier. |
| Cable Track management system | Nov 2022 | https://www.reddit.com/r/ender5plus/comments/so2ulf/ender_5_plus_cable_chain_solution/ [Printer_Mods/Cable_Track](Printer_Mods/Cable_Track)|
| MEME Controller | Oct 2022 - | [meme](meme_ctlr) |
| Slicer Settings, Calibration, and Test Prints | Oct 2022 - | [test](Calibration_Test_Prints) |
| [Custom Marlin Firmware](marlin) | Dec 2022 - | - |


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

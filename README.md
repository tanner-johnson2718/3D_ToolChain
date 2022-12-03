# 3D Printing Tool Chain
Repo to hold scripts, source, and config files for 3D printing tool chain. 
Current tool chain is as follows:

1) FreeCAD for 3D modeling
2) Cura for slicing
3) [MEME CTLR](meme_ctlr), custom g code sender and printer serial monitor. This is the UI for the printer as modifcations required a custom interface.
4) Marlin Firmware running on printer

Currently only targeting ender 5 Plus with following components

| Component | Date Installed | Comment |
| --- | --- | --- |
| Electronics Enclosure | Oct-Dec 2022 | Removed PSU and main board, printing custom enclosure to move electronics out from underneath printer, see [Printer_Mods/Electronic_Enclosure](Printer_Mods/Electronic_Enclosure). Wiring diagrams, electrical specs, and pinout diagrams can all be found there as well. Added the physical infastructure to start using unused pins on the Melzi board (ATmega 2560) and to support current draw monitoring, a chamber heater, and a filament drier. |
| Cable Track management system | Nov 2022 | https://www.reddit.com/r/ender5plus/comments/so2ulf/ender_5_plus_cable_chain_solution/ [Printer_Mods/Cable_Track](Printer_Mods/Cable_Track)|
| Steppers | - | Stock |
| Stepper Drivers | - | Stock |
| PSU | - | [Stock Meanwell RSP-500-24](Printer_Mods/Electronic_Enclosure/MeanWell_500_Datasheet.pdf) |
| Mother board | - | Stock Melzi v2.2 [Pinout](Printer_Mods/Electronic_Enclosure/melzi_pinout.jpg)|
| Extruder | Sept 2022 | Creality All metal Extruder https://www.amazon.com/dp/B07ZMFP2L8?psc=1&ref=ppx_yo2ov_dt_b_product_details |
| Bowden Tube | Sept 2022 | Capicorn XS https://www.captubes.com |
| Hot end | Nov 2022 | Micro Swiss All metal hot end https://store.micro-swiss.com/collections/all-metal-hotend-kits/products/all-metal-hotend-kit-for-cr-10 |
| Hot end Thermistor | Nov 2022 | https://www.amazon.com/dp/B0714MR5BC?psc=1&ref=ppx_yo2ov_dt_b_product_details |
| External Bed Mosfett | Nov 2022 | Mosfet FYSETC https://www.amazon.com/dp/B07C4PGXFK?psc=1&ref=ppx_yo2ov_dt_b_product_details |
| Part Cooler | - | Stock |
| ABL | - | Stock BL Touch |
| X Gantry | - | Stock |
| Y Guides | - | Stock |
| Z Rails | Sept 2022 | Stock w/ Z axis POM Lead nut and spring https://www.amazon.com/dp/B07XYR3F4C?psc=1&ref=ppx_yo2ov_dt_b_product_details |

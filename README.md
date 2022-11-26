# 3D Printing Tool Chain
Repo to hold scripts, source, and config files for 3D printing tool chain. 
Current tool chain is as follows:

1) FreeCAD for 3D modeling
2) Cura for slicing
3) MEME CTLR (custom g code sender and printer serial monitor)
4) Marlin Firmware running on printer

Currently only targeting ender 5 Plus with following components

| Component | Date Installed | Comment |
| --- | --- | --- |
| Steppers | - | Stock |
| Stepper Drivers | - | Stock |
| PSU | - | Stock |
| Mother board | - | Stock |
| Extruder | Sept 2022 | Creality All metal Extruder |
| Bowden Tube | Sept 2022 | Capicorn XS |
| Hot end | Nov 22 | Micro Swiss All metal hot end |
| Hot end Thermistor | Nov 22 | https://www.amazon.com/dp/B0714MR5BC?psc=1&ref=ppx_yo2ov_dt_b_product_details |
| Part Cooler | - | Stock |
| ABL | - | Stock BL Touch |
| X Gantry | - | Stock |
| Y Guides | - | Stock |
| Z Rails | Sept 2022 | Stock w/ Z axis POM Lead nut and spring |
| Electronics Enclosure | Oct-Dec 2022 | Removed PSU and main board, printing custom enclosure to move electronics out from underneath printer (See Printer_Mods/Electric_Enclosure. Wiring diagrams as well as electrical specs can be found there as well). |
| Cable Track management system | Nov 2022 | https://www.reddit.com/r/ender5plus/comments/so2ulf/ender_5_plus_cable_chain_solution/ (Printer_Mods/Cable_Track)|
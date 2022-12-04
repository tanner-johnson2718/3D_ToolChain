# Custom Electronics and Electronics Enclosure

# Requirements
* Support chamber heater and Filament dryer
    * Adding Mosfets and additional wiring and board pinout support to enable this
* Relocate electronics from underneath the printer to outside the chamber
* Measure power draw
* Electric components, especially main board and its pinouts should be "easily" accesible
    * Will encorpaerate a method "sliding" base plates that secucre components
    * Main ports on Melzi should be mapped to JST connectors embedded into the frame of the enclosure for quick connect and disconnect (even unused )
* All wiring should be evaluated for current draw and proper gauge wire shall be used
* Enclosure should have quick connects to quickly disconnect all wires going to the printer.

# PSU and MOSFET Wiring Diagrams

Power supply wiring diagram. The 10A GMA fuse is integrated into the iec320 AC plug. 

![Alt text](Datasheets/Power_Supply_Wiring.png)

| Connection Source | Connection Sink | Connector Source | Connector Sink | V | W | Wire Gauge |
| --- | --- | --- | --- | --- | --- | --- |
| Live iec320 | Live Ideal Connector | Female Disconnect | Bare (push in) | 120V AC | 1000W + | 12 gauge (rated to 20A AC or 2400W) |
| Neutral iec320 | Neutral Ideal Connector | Female Disconnect | Bare (push in) | 120V AC | 1000W + | 12 gauge (rated to 20A AC or 2400W) |
| Ground iec320 | Ground Ideal Connector | Female Disconnect | Bare (push in) | 120V AC | 1000W + | 12 gauge (rated to 20A AC or 2400W) |
| Live Ideal Connector | Printer Switch | Bare (push in) | Female Disconnect | 120V AC | 500W + | 16 gauge (rated to 10A AC or 1200W) |
| Live Ideal Connector | Chamber Switch | Bare (push in) | Female Disconnect | 120V AC | 500W + | 16 gauge (rated to 10A AC or 1200W) |
| Printer Switch | Printer PSU Live terminal | Female Disconnect | Spade connector (8 to 10 stud size) | 120V AC | 500W + | 16 gauge (rated to 10A AC or 1200W) |
| Chamber Switch | Chamber PSU Live terminal | Female Disconnect | Spade connector (8 to 10 stud size) | 120V AC | 500W + | 16 gauge (rated to 10A AC or 1200W) |
| Neutral Ideal Connector | Printer PSU Neutral Terminal | Bare (push in) | Spade connector (8 to 10 stud size) | 120V AC | 500W + | 16 gauge (rated to 10A AC or 1200W) |
| Neutral Ideal Connector | Chamber PSU Neutral Terminal | Bare (push in) | Spade connector (8 to 10 stud size) | 120V AC | 500W + | 16 gauge (rated to 10A AC or 1200W) |
| Ground Ideal Connector | Printer PSU Ground Terminal | Bare (push in) | Spade connector (8 to 10 stud size) | 120V AC | 500W + | 16 gauge (rated to 10A AC or 1200W) |
| Ground Ideal Connector | Ground PSU Neutral Terminal | Bare (push in) | Spade connector (8 to 10 stud size) | 120V AC | 500W + | 16 gauge (rated to 10A AC or 1200W) |
| Ground Ideal Connector | Chasis | Bare (push in) | .25in ring connector | 120V AC | 1000W + | 12 gauge (rated to 10A AC or 1200W) |
| Printer V1+/- | Melzi +/- Input | Spade connector (8 to 10 stud size) | Bare (screw down) | 24V DC |  <240W | 16 gauge (rated to 10A DC or 240W) |
| Printer V3+/- | Bed MOSFET +/- Input | Spade connector (8 to 10 stud size) | Bare (screw down) | 24V DC | 500W + | 12 gauge (rated to 20A DC or 480W) |
| Chamber V1+/- | Drier MOSFET +/- Input | Spade connector (8 to 10 stud size) | Bare (screw down) | 24V DC | 150W | 16 gauge (rated to 10A DC or 240W) |
| Chamber V3+/- | Chamber MOSFET +/- Input | Spade connector (8 to 10 stud size) | Bare (screw down) | 24V DC | ??? | ??? |
| Bed MOSFET Output +/- | Terminal Connector | Bare (screw down) | Male Disconnect  | 24V DC | 500W + | 12 gauge (rated to 20A DC or 480W) |
| Drier MOSFET Output +/- | Terminal Connector | Bare (screw down) | Male Disconnect  | 24V DC | 150W | 16 gauge (rated to 10A DC or 240W) |
| Chamber MOSFET Output +/- | Terminal Connector | Bare (screw down) | Male Disconnect | 24V DC | ??? | ??? |

# Melzi Wiring, Connectors, and Pinouts
 | Connector | ATmega2560 Pins | Connector Type (board side) | Connector Type (target side) |
 | --- | --- | --- | --- |
 | | | |

# Bill of Materials

| Material | Quantity | Link |
| --- | --- | --- |
| 2020 Aluminum T slot | 10 400mm | https://www.amazon.com/dp/B0B2P434PD?psc=1&ref=ppx_yo2ov_dt_b_product_details |
| 8mm M3 Bolts and 2020 M3 t slot nuts | 88  | To secure outer walls of case to frame. Each outer and upper wall gets 8. 2 fan plates, 4 Electronic wall plates, 2 upper plates, 2 psu wall plates, and 1 psu wall plate for 11 total.  |
| 12mm M3 Bolts | 16 | To secure fans to fan plate |
| 8mm M4 bolts | 8 | To secure PSUs to bottom plate |
| 16mm M3 Bolts + spaces + nuts | 17 | To secure melzi and MOSFET boards to bottom plates |
| 40x40x10 fans | 4 | At 24V, .07A draw. https://www.amazon.com/dp/B088665SKK?psc=1&ref=ppx_yo2ov_dt_b_product_details | 
| Additional NTC Thermistors | 5 | https://www.amazon.com/dp/B0714MR5BC?psc=1&ref=ppx_yo2ov_dt_b_product_details |
| PTC heater (filament dehydrator) | 1 at 150W | https://www.amazon.com/dp/B07JKNKK7J?psc=1&ref=ppx_yo2ov_dt_b_product_details |
| PTC heater (chamber heater) | 1-2 at 150-250W | - |
| Mosfets | 3 | https://www.amazon.com/dp/B07C4PGXFK?psc=1&ref=ppx_yo2ov_dt_b_product_details |
| Meanwell RSP-500-24 PSU | 2 | [Stock Meanwell RSP-500-24](MeanWell_500_Datasheet.pdf) |
| Creality Melzi v2.2 | 1 | Stock |
| Switches | 2 | Standard 30A 120V AC switches |
| 10A 250V GMA Fuse | 1 | Integrated in AC plug |
| Ideal 4 way Push in connectors | 3 | 16AWG to 12AWG, rated to 20A|
| Various disconnect connectors | >20 | Various sizes, 10AWG to 22AWG, amp rating appropiate to wire gauge. Use appropiate sized connectore given wire gauge |
| Spade Connectors | >20 | 16AWG to 12AWG, 8 to 10 Stud size | 
| AC Plug | 1 | iec320 C14 |
| Ampmeters?? | 2 | - |
| Wire | ??? | Fill this out |
| JST Connectors | ?? | Fill this out |

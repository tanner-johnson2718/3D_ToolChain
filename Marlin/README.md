# Custom Marlin Firmware

... Description todo ...

# Initial Setup
* Pulling Marlin bugfix-2.1.x at commit 8298a477e1f1fa6188788448eec3f349c1ba93de
* Pulled and replaced configs (Configuration.h and Configuration_adv.h) from Marlin Configurations Repo bugfix-2.1.x for Ender 5 plus at commit 81b89564117d024f50cb29fb8d5e78f8f5322804
* Pulling Marlin Documentation repo at commit a5796a995512eef9aff0984626facf9d1ae85bdb
* Install Platform IO and Auto Build Marlin for build targeting skr mini e3 v3
* Changed Configuration.h)
    * `#define MOTHERBOARD BOARD_BTT_SKR_MINI_E3_V3_0`
    * `#define SERIAL_PORT 2`
    * `#define SERIAL_PORT_2 -1`
    * Change all driver types to `TMC2209`
    * `#define HEATER_0_MAXTEMP 300`
    * `#define DEFAULT_MAX_FEEDRATE          { 1000, 1000, 10, 5000 }`
    * `#define INVERT_X_DIR true`
    * `#define INVERT_Y_DIR true`
    * `#define INVERT_Z_DIR true`
    * `#define INVERT_E0_DIR true`
    * `#define DEFAULT_MAX_ACCELERATION      { 1000, 1000, 50, 1000 }`
* To build deploy simply open Marlin_Custom dir in Auto Build Marlin, build, and copy to SD card as FIRMWARE.BIN.

# Marlin Key Functions / Files / 
* queue.cpp - advance()
* queue.cpp - get_serial_commands()
* MarlinCore.cpp - loop()
* pins_RAMPS.h
* Configuration.h
* COnfiguration_adv.h
# Custom Marlin Firmware

... Description todo ...

# Initial Setup
* Pulling Marlin bugfix-2.1.x at commit 8298a477e1f1fa6188788448eec3f349c1ba93de
* Pulled and replaced configs (Configuration.h and Configuration_adv.h) from Marlin Configurations Repo bugfix-2.1.x for Ender 5 plus at commit 81b89564117d024f50cb29fb8d5e78f8f5322804
* Pulling Marlin Documentation repo at commit a5796a995512eef9aff0984626facf9d1ae85bdb
* Downloading Arduino IDE 2.0.3
* Download AVR board support in IDE
* Open marlin.ino in IDE
* Compile and send image over serial
* Appear to have burned out pull up resistors on A14 and 13. Use the following work around
    * Mapped Nozzle Thermistor to pin A15 (PK7 on ATMega2560)
        * Was A13 and TEMP_PIN_1 was A15
        * in pin_RAMPS.h
    * Mapped Bed heater to pin A11 (PK3 on ATMega2560)
        * was A14
        * in pin_RAMPS.h
        * set TEMP_SENSOR_BED to 1000 i.e. custom thermistor settings
            * pull up res = 1000 ohm
            * R at 25C = 100000
            * B = 3950
            * C = 0

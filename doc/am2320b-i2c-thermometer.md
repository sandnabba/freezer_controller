# AM2320B/SHT21 I2C thermometer
The Aosong AM2320 sensor is a SHT21 compatible I2C thermometer and hygrometer, that can be connected using either I2C or 1-Wire.
Since I wanted to have protocol redundancy I'm using I2C in this project.

I have connected it to the Raspberry Pi using the following pins:

| Sensor     | GPIO | Pin# |  
|------------|------|------|  
| Red    (V) |      | 3.3v |  
| Black  (G) |      | GND  |  
| White  (S) |  SCL |  5   |
| Yellow (D) |  SDA |  3   |



# References:
https://forum.arduino.cc/index.php?topic=363900.0
https://www.raspberrypi.org/forums/viewtopic.php?t=152148

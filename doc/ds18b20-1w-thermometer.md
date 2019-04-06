# DS18B20 1-Wire thermometer
The DS18B20 thermometers are well documented, and a lot of examples could be found using Google.
They are really simple and easy to use, just remember the pull-up resistor between 3.3v and the data pin.

One wire will use to GPIO-4 (Pin 7) as default.

| Sensor | GPIO | Pin# |  
|--------|------|------|  
| Red    |      | 3.3v |  
| Black  |      | GND  |  
| Yellow | 4    | 7    |  

1-Wire devices can be found under `/sys/bus/w1/devices`.
A DS18B20 sensor will be named something like "28-021564a135ff".

To probe the sensor for the current temperature you can simply run:
`/sys/bus/w1/devices/28-021564a135ff/w1_slave`

To read the sensor in Python, I'm using the "w1thermsensor" package:
https://github.com/timofurrer/w1thermsensor


# References:
https://pinout.xyz/pinout/1_wire

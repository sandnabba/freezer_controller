#### DS18B20 1-Wire thermometer
One wire will default to GPIO-4 (Pin 7).

1-Wire devices can be found under `/sys/bus/w1/devices`.
A DS18B20 sensor will be named something like "28-021564a135ff".

To probe the sensor for the current temperature you can simply run:
`/sys/bus/w1/devices/28-021564a135ff/w1_slave`

To read the sensor in Python, I'm using the "w1thermsensor" package:
https://github.com/timofurrer/w1thermsensor

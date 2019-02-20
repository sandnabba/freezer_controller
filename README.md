# freezer_controller-
Replace the old thermostat with Linux, Python, a relay and a thermometer.

## Functionality

### Thermometer

### Control Compressor

### Sumbit metrics

### Logs

# Installation
`git submodule init` `git submodule update`

Python virtual environment:


Permissions to access I2C bus:
`usermod -a -G i2c $USER`

Permissions to access GPIO pins:
`usermod -a -G gpio $USER`


# Metrics
## What to alert on?
* Absent
* Low temp
* High temp
* Compressor on for long time?

# QA
General things:
* Disk full

## Thermometer
Lost connoction (All 4 pins, one at a time)

## Relay
* Lost connection

## Metrics  
* Timeout
* No route
* Wrong route
* Iptables DROP
* Iptables REJECT

## Logs (Correct log level, alert on >= ERROR)

# ToDo
Future improvements
* Can we detect if the door is open or not? Hook into existing switch, or add another sensor.
* 

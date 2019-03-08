# freezer_controller-
Replace the old thermostat with Linux, Python, a relay and a thermometer.

# Overview
Components used:
Raspberry Pi Zero W
DS18B20 1-Wire thermometer
AM2320B/SHT21 I2C thermometer + hygrometer
A solid state relay
ST7735R SPI display
An Electrolux Freezer (Could probably be applied to any fridge or freezer)

## Functionality

### Thermometer

### Control Compressor

### Sumbit metrics

### Logs

# Installation
You will need Git and a Python Virtual environment to install the freezer_controller.
In Raspbian, run:  
`sudo apt install git python3-venv`

Clone this repository:  
`git clone git@github.com:sandnabba/freezer_controller.git`

Checkout the submodule required to read the I2C thermometer:
`git submodule init` followed by `git submodule update`.

## Permissions
To be able to run the application as a user, you need access to the I2C bus and the GPIO pins.

Permissions to access I2C bus:
`sudo usermod -a -G i2c $USER`

Permissions to access GPIO pins:
`sudo usermod -a -G gpio $USER`


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

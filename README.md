# freezer_controller
Replace the old thermostat with Linux, Python, a relay and a thermometer.

# Overview
Components used:
* Raspberry Pi Zero W
* [DS18B20 1-Wire thermometer](/doc/ds18b20-1w-thermometer.md)
* [AM2320B/SHT21 I2C thermometer + hygrometer](/doc/i2c-am2320b-thermometer.md)
* [ST7735R SPI display](/doc/st7735r-spi-display.md)
* A solid state relay
* An Electrolux EUC3107 Freezer (Could probably be applied to any fridge or freezer)


# Installation
First you need to prepare the Raspberry pi and the operating system.
We are going to use both 1-Wire, I2C and SPI which will require some setup:
`sudo echo "dtoverlay=w1-gpio" >> /boot/config.txt`
`sudo echo "dtparam=i2c_arm=on" >> /boot/config.txt`
`sudo echo "dtparam=spi=on" >> /boot/config.txt`

## Permissions
To be able to run the application as a user, you need access to the I2C bus and the GPIO pins.

Permissions to access I2C bus:
`sudo usermod -a -G i2c $USER`

Permissions to access GPIO pins:
`sudo usermod -a -G gpio $USER`

## Application
You will need Git and a Python Virtual environment to install the freezer_controller.
In Raspbian, run:  
`sudo apt install git python3-venv`

Clone this repository:  
`git clone git@github.com:sandnabba/freezer_controller.git`

Checkout the submodule required to read the I2C thermometer:
`git submodule init` followed by `git submodule update`.


# Run the application

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
Lost connection (All 4 pins, one at a time)

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

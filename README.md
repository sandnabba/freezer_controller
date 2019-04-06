# freezer_controller
Replacing an old broken freezer thermostat with Linux, Python, a relay and some thermometers.

# Overview
When my freezer at home stopped working I quickly found out that it was the thermostat that was broken.
However, a new thermostat was $60 + shipping, something that I did not want to spend an a 15+ year old freezer.
So I decided to build my own solution with some stuff that I already got at home, mostly as a fun learning project. :)

Components used:  
* Raspberry Pi Zero W
* [DS18B20 1-Wire thermometer](/doc/ds18b20-1w-thermometer.md)
* [AM2320B/SHT21 I2C thermometer + hygrometer](/doc/i2c-am2320b-thermometer.md)
* [ST7735R SPI display](/doc/st7735r-spi-display.md)
* A solid state relay
* An Electrolux EUC3107 Freezer (Could probably be applied to any fridge or freezer)

For more information about the individual components, please see the links above.

# Installation
First you need to prepare the Raspberry pi and the operating system.
We are going to use both 1-Wire, I2C and SPI which will require some setup:
```bash
sudo echo "dtoverlay=w1-gpio" >> /boot/config.txt
sudo echo "dtparam=i2c_arm=on" >> /boot/config.txt
sudo echo "dtparam=spi=on" >> /boot/config.txt
```

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
Start by setting up the configuration. Copy the `config.py.example` to `config.py`.

Currently there are no proper start script. The preferred method is to run the applictaion within a `screen`.
Run the applictaion with:  
`./env/bin/python main.py`


# ToDo
Future improvements:  
* Can we detect if the door is open or not? Hook into existing switch, or add another sensor.
* Use the average temperature from both thermometers, detect if any of them are missing.
* Write an systemD service with auto start and logging
* Add a proper interrupt handler for handling shut down signals

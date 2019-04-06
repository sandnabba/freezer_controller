# This file is written for Python3.5, which was the default in Raspbian at the time of writing.

from am2320_python.am2320 import AM2320

import logging
logger = logging.getLogger(__name__)

try:
    import RPi.GPIO as GPIO
    from w1thermsensor import W1ThermSensor
except RuntimeError:
    logger.critical("Not running on a Raspberry Pi, continuing anyway")
    pass

import time

class Freezer:
    # Temperature:
    TEMP1 = 0.0
    TEMP2 = 0.0
    HUMIDITY = 0.0

    # Compressor:
    COMP_GPIO_PIN = None # This is the GPIO-pin, not the physical pin, Connected to 14
    COMP_STATE = 0
    COMP_ON_TIME = 0
    COMP_OFF_TIME = 0
    COMP_STATE_CHANGE_TIME = 0


    def __init__(self, COMP_PIN=None):
        logger.info("Initiating freezer")
        logger.info("Compressor_Pin: %s" % COMP_PIN)
        self.COMP_GPIO_PIN = COMP_PIN
        self.get_temperature()
        logger.info("Temp1: %s" % self.TEMP1)
        logger.info("Temp2: %s" % self.TEMP2)

        # Setup compressor pin:
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.COMP_GPIO_PIN, GPIO.OUT)
        except Exception as e:
            logger.error("Error setting up GPIO pins")
            print(e)
            pass

        # Get current compressor state:
        try:
            self.COMP_STATE = GPIO.input(self.COMP_GPIO_PIN)
            logger.info("compressor is: %s" % self.COMP_STATE)
        except:
            logger.error("Error reading compressor state")
            pass


    def get_temperature(self):
        logger.debug("Getting temperature 1")
        try:
            sensor = AM2320(1)
            (t,h) = sensor.readSensor()
            self.TEMP1 = round(float(t), 2)
            self.HUMIDITY = round(float(h), 2)
        except FileNotFoundError:
            logger.error("Could not get i2c device")
            pass
        except Exception as e:
            logger.error("Unknown error getting I2C temperature, ")
            print(e)
            pass

        self.TEMP1 = -18.2

        logger.debug("Getting temperature 2")
        try:
            sensor2 = W1ThermSensor()
            self.TEMP2 = round(float(sensor2.get_temperature()), 2)
        except Exception as e:
            logger.error("Unknown error getting 1-wire temperature, ")
            print(e)
            pass

        return 0


    def start(self):
        # Add check here so that we don't try to start the compressor if it's already running
        try:
            if GPIO.input(self.COMP_GPIO_PIN) == 1:
                logger.debug("Compressor is already running")
                return 1
        except Exception as e:
            logger.critical("Got an exception checking compressor state:")
            print(e)
            pass

        logger.info("Starting Compressor")
        try:
            GPIO.output(self.COMP_GPIO_PIN, GPIO.HIGH)
            self.COMP_STATE = 1
            self.COMP_ON_TIME = time.time()
        except Exception as e:
            logger.critical("Error starting compressor")
            print(e)
            pass


    def stop(self):
        logger.info("Stopping Compressor")
        if (time.time() - self.COMP_ON_TIME) < 300:
            wait_time = 300 - (time.time() - self.COMP_ON_TIME)
            logger.warning("Compressor started less than 5 minutes ago, wait %d more seconds" % wait_time)
            return wait_time
        else:
            try:
                GPIO.output(self.COMP_GPIO_PIN, GPIO.LOW)
                self.COMP_STATE = 0
                self.COMP_OFF_TIME = time.time()
            except:
                logger.error("Error stopping compressor")
                pass

from am2320_python.am2320 import AM2320
from w1thermsensor import W1ThermSensor

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Not running on a Raspberry Pi, continuing anyway")
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
        print("Initiating freezer")
        print("Compressor_Pin: ", COMP_PIN)
        self.COMP_GPIO_PIN = COMP_PIN
        self.get_temperature()
        print("Temp1: ", self.TEMP1)
        print("Temp2: ", self.TEMP2)

        # Setup compressor pin:
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.COMP_GPIO_PIN, GPIO.OUT)
        except Exception as e:
            print("Error setting up GPIO pins")
            print(e)
            pass

        # Get current compressor state:
        try:
            self.COMP_STATE = GPIO.input(self.COMP_GPIO_PIN)
            print("compressor is: ", self.COMP_STATE)
        except:
            print("Error reading compressor state")
            pass

    #@classmethod
    def get_temperature(self):
        print("Getting temperature 1")
        try:
            sensor = AM2320(1)
            (t,h) = sensor.readSensor()
            #print(t, h)
            self.TEMP1 = round(float(t), 2)
            self.HUMIDITY = round(float(h), 2)
        except FileNotFoundError:
            print("Could not get i2c device")
            pass
        except Exception as e:
            print("Unknown error getting I2C temperature, ")
            print(e)
            pass

        print("Getting temperature 2")
        try:
            sensor2 = W1ThermSensor()
            self.TEMP2 = round(float(sensor2.get_temperature()), 2)
        except Exception as e:
            print("Unknown error getting 1-wire temperature, ")
            print(e)
            pass

        return 0
    
    #@classmethod
    def start(self):
        # Add check here so that we don't try to start the compressor if it's already running
        try:
            if GPIO.input(self.COMP_GPIO_PIN) == 1:
                print("Compressor is already running")
                return 1
        except Exception as e:
            print("Got an exception checking compressor state:")
            print(e)
            pass

        print("Starting Compressor")
        try:
            GPIO.output(self.COMP_GPIO_PIN, GPIO.HIGH)
            self.COMP_STATE = 1
            self.COMP_ON_TIME = time.time()
        except Exception as e:
            print("Error starting compressor")
            print(e)
            pass

        
    #@classmethod
    def stop(self):
        print("Stopping Compressor")
        if (time.time() - self.COMP_ON_TIME) < 300:
            wait_time = 300 - (time.time() - self.COMP_ON_TIME)
            print("Compressor started less than 5 minutes ago, wait %d more seconds" % wait_time)
            return wait_time
        else:
            try:
                GPIO.output(self.COMP_GPIO_PIN, GPIO.LOW)
            except:
                print("Error stopping compressor")
                pass
            self.COMP_STATE = 0
            self.COMP_OFF_TIME = time.time()

        
    
    

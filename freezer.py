from am2320_python.am2320 import AM2320

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Not running on a Raspberry Pi, continuing anyway")
    pass

import time

class Freezer:
    # Temperature:
    CURRENT_TEMP = 0.0
    LAST_TEMP = 0.0

    # Compressor:
    COMP_GPIO_PIN = 12
    COMP_STATE = 0
    COMP_ON_TIME = 0
    COMP_OFF_TIME = 0
    COMP_STATE_CHANGE_TIME = 0


    def __init__(self):
        print("Initiating freezer")
        self.CURRENT_TEMP = self.get_temperature()

        # Setup compressor pin:
        try:
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.COMP_GPIO_PIN, GPIO.OUT, initial=GPIO.LOW)
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

    @staticmethod
    def get_temperature():
        print("Getting temperature")
        try:
            sensor = AM2320(1)
            (t,h) = sensor.readSensor()
            print(t, h)
            return float(t)
        except FileNotFoundError:
            print("Could not get i2c device")
            return -18.1
        except Exception as e:
            print("Unknown error, ")
            print(e)
            return 0
            pass
    
    @classmethod
    def start(self):
        print("Starting Compressor")
        try:
            GPIO.output(self.COMP_GPIO_PIN, GPIO.HIGH)
        except:
            print("Error starting compressor")
            pass
        self.COMP_STATE = 1
        self.COMP_ON_TIME = time.time()


        
    @classmethod
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

        
    
    

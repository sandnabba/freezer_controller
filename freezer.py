from am2320_python.am2320 import AM2320

try:
    import RPi.GPIO as GPIO
except:
    print("Error importing GPIO lib")
    pass

class Freezer:
    # Temperature:
    CURRENT_TEMP = 0.0
    LAST_TEMP = 0.0

    # Compressor:
    COMP_GPIO_PIN = 8
    COMP_STATE = 0
    COMP_ON_TIME = 0
    COMP_OFF_TIME = 0
    COMP_STATE_CHANGE_TIME = 0


    def __init__(self):
        print("Initiating freezer")
        self.CURRENT_TEMP = self.get_temperature()
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(COMP_GPIO_PIN, GPIO.OUT, initial=GPIO.LOW)
        except:
            print("Error setting up GPIO pins")
            pass

    @staticmethod
    def get_temperature():
        print("Getting temperature")
        try:
            sensor = AM2320(1)
            (t,h) = sensor.readSensor()
            print(t, h)
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
            GPIO.output(COMP_GPIO_PIN, GPIO.HIGH)
            self.COMP_STATE = 1
        except:
            print("Error starting compressor")
            self.COMP_STATE = 1
            pass


        
    @classmethod
    def stop(self):
        print("Stopping Compressor")
        try:
            GPIO.output(COMP_GPIO_PIN, GPIO.LOW)
            self.COMP_STATE = 0
        except:
            self.COMP_STATE = 0
            print("Error stopping compressor")
            pass

        
    
    

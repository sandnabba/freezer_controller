
class Freezer:
    # Temperature:
    CURRENT_TEMP = 0
    LAST_TEMP = 0

    # Compressor:
    COMP_STATE = 0
    COMP_ON_TIME = 0
    COMP_OFF_TIME = 0
    COMP_STATE_CHANGE_TIME = 0


    def __init__(self):
        print("Initiating freezer")
        self.CURRENT_TEMP = self.get_temperature()

    @staticmethod
    def get_temperature():
        print("Getting temperature")
        return -18.1
    
    @classmethod
    def start(self):
        print("Starting Compressor")
        self.COMP_STATE = 1
        
    @classmethod
    def stop(self):
        print("Stopping Compressor")
        self.COMP_STATE = 0
        
    
    

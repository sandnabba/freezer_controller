#!/usr/bin/env python3

# This is the main file.

import sys
import time
import appoptics_metrics
import logging
from freezer import Freezer

# Load configuration:
import config

# Setup global stuff:
#logger = logging.getLogger('freezer')
#logger.setLevel(logging.DEBUG)

ao = appoptics_metrics.connect(config.APPOPTICS_KEY, tags={'ENVIRONMENT': "prod"})
freezer = Freezer(config.GPIO_PINS["COMP_PIN"])


def send_metrics(freezer):
    #####

    #### Check here if we have an AppOptics Token, if not, break

    ####
    print("Sending metrics")
    q = ao.new_queue()
    q.add('freezer.temperature', freezer.TEMP1, tags={'type': 'i2c'}, inherit_tags=True)
    q.add('freezer.temperature', freezer.TEMP2, tags={'type': '1w'}, inherit_tags=True)
    q.add('freezer.humidity', freezer.HUMIDITY, tags={'type': 'i2c'}, inherit_tags=True)
    q.add('freezer.comp_state', freezer.COMP_STATE, inherit_tags=True)
    if freezer.COMP_STATE == 1:
        q.add('freezer.comp_state_bool', 1, tags={'state': 'ON'}, inherit_tags=True)
    else:
        q.add('freezer.comp_state_bool', 1, tags={'state': 'OFF'}, inherit_tags=True)
    q.submit()


def main(freezer):
    #print("Starting Main function")
    freezer.get_temperature()
    #print("Current temperature 1: %.2f" % freezer.TEMP1)
    #print("Current temperature 2: %.2f" % freezer.TEMP2)

    if freezer.TEMP1 > config.MAX_TEMP:
        # Temperature is to high:
        freezer.start()
    elif freezer.TEMP1 < config.MIN_TEMP:
        # Temperature is to low
        freezer.stop()
    else:
        # Will this ever happen?
        print("Temp OK")

    # Just print a newline:
    #print()

while 1:
    # Control the freezer:
    main(freezer)


    # Send metrics:
    ### Add check if we have an AppOptics key here
    ### Stop otherwise
    try:
        send_metrics(freezer)
    except appoptics_metrics.exceptions.Unauthorized:
        print("ERROR: Wrong AppOptics key, could not submit metrics")
        pass
    except Exception as e:
        print("An ERROR occured while sending metrics to AppOptics")
        print(e)
        pass

#### Debug:
#    freezer.CURRENT_TEMP += 0.05
#    if freezer.COMP_STATE == 1:
#        freezer.CURRENT_TEMP -= 0.1
#    print()
    time.sleep(60)

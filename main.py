#!/usr/bin/env python3

# This file is written for Python3.5, which was the default in Raspbian at the time of writing.

import sys
import time
import appoptics_metrics
import logging
from freezer import Freezer

# Load configuration:
import config

# Setup global stuff:
logger = logging.getLogger('freezer')
logger.setLevel(logging.getLevelName(config.LOGLEVEL))

# create console handler and add a formatter:
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

ao = appoptics_metrics.connect(config.APPOPTICS_KEY, tags={'ENVIRONMENT': "prod"})
freezer = Freezer(config.GPIO_PINS["COMP_PIN"])

def send_metrics(freezer):
    #####

    #### Check here if we have an AppOptics Token, if not, break
    if config.APPOPTICS_KEY == None:
        # We don't have an AppOptics key, no need to submit metrics
        return 0
    ####
    try:
        logger.debug("Sending metrics to AppOptics")
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

    except appoptics_metrics.exceptions.Unauthorized:
        logger.error("Wrong AppOptics key, could not submit metrics")
        pass
    except Exception as e:
        logger.error("An ERROR occured while sending metrics to AppOptics")
        print(e)
        pass


def main(freezer):
    logger.debug("Starting Main function")
    freezer.get_temperature()
    logger.debug("Current temperature 1: %s" % freezer.TEMP1)
    logger.debug("Current temperature 2: %s" % freezer.TEMP2)

    # If we don't have any temperature available, enter the emergency loop:
    if freezer.TEMP1 == None and freezer.TEMP2 == None:
        # Run compressor at a 40% duty cycle on a 15 minute interval
        # On 10 minutes (600 seconds)
        # Off 15 minutes (900 seconds)
        logger.error("Entering emergency loop")
        current_time = time.time()
        if freezer.COMP_STATE == 1:
            if (current_time - freezer.COMP_ON_TIME) > 600:
                freezer.stop()
        elif freezer.COMP_STATE == 0:
            if (current_time - freezer.COMP_OFF_TIME) > 900:
                freezer.start()
        else:
            # If nothing else, start the compressor:
            freezer.start()


    else:
        if freezer.TEMP1 > config.MAX_TEMP:
            # Temperature is to high:
            freezer.start()
        elif freezer.TEMP1 < config.MIN_TEMP:
            # Temperature is to low
            freezer.stop()
        else:
            # Will this ever happen?
            logger.debug("Temp OK")

    # Just print a newline:
    #print()

if __name__ == '__main__':
    while 1:
        # Control the freezer:
        main(freezer)
        send_metrics(freezer)
        time.sleep(60)

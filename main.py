#!/usr/bin/env python3

# This file is written for Python3.5, which was the default in Raspbian at the time of writing.

import sys
import time
import appoptics_metrics
import logging
from freezer import Freezer
import metrics

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
    if config.APPOPTICS_KEY:
        metrics.send_ao_metrics(freezer)
    if config.INFLUXDB["ENABLED"]:
        metrics.send_influx_metrics(freezer)

def main(freezer):
    logger.debug("Starting Main function")
    if freezer.get_temperature():
        # Debug, print temperatures:
        for t,n in zip(freezer.TEMP.values(), freezer.TEMP):
            if t['temperature']:
                logger.debug("Current temperature %s: %.2f, type: %s" % (n, t['temperature'], t['type']))

        if freezer.AVG_TEMP > config.MAX_TEMP:
            # Temperature is to high:
            freezer.start()
        elif freezer.AVG_TEMP < config.MIN_TEMP:
            # Temperature is to low
            freezer.stop()
        else:
            # All good
            logger.debug("Temp OK")
    else:
        logger.critical("Not getting temperature!")
        # Enter emergency loop here


if __name__ == '__main__':
    while 1:
        # Control the freezer:
        main(freezer)
        send_metrics(freezer)
        time.sleep(60)

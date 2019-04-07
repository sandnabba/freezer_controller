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
    freezer.get_temperature()
    logger.debug("Current temperature 1: %.2f" % freezer.TEMP1)
    logger.debug("Current temperature 2: %.2f" % freezer.TEMP2)

    if freezer.TEMP1 > config.MAX_TEMP:
        # Temperature is to high:
        freezer.start()
    elif freezer.TEMP1 < config.MIN_TEMP:
        # Temperature is to low
        freezer.stop()
    else:
        # Will this ever happen?
        logger.debug("Temp OK")

if __name__ == '__main__':
    while 1:
        # Control the freezer:
        main(freezer)
        send_metrics(freezer)
        time.sleep(60)

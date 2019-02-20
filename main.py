#!/usr/bin/python3

# This is the main file.

import sys
import time
import appoptics_metrics
from freezer import Freezer

MAX_TEMP = -18
MIN_TEMP = -18.5



def send_metrics(freezer):
    print("Sending metrics")
    print("AO-temp: ", freezer.CURRENT_TEMP)


def main(freezer):
    print("Starting Main function")
    print("Current temperature: %.2f" % round(freezer.CURRENT_TEMP, 2))

    if freezer.CURRENT_TEMP > MAX_TEMP:
        # Temperature is to high:
        freezer.start()
    elif freezer.CURRENT_TEMP < MIN_TEMP:
        # Temperature is to low
        freezer.stop()
    else:
        print("Temp OK")

    # Send metrics:
    #send_metrics(freezer)

freezer = Freezer()
while 1:
    main(freezer)
    freezer.CURRENT_TEMP += 0.05
    if freezer.COMP_STATE == 1:
        freezer.CURRENT_TEMP -= 0.1
    print()
    time.sleep(1)

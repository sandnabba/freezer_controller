from influxdb import InfluxDBClient
import appoptics_metrics
import logging
import datetime
import json

logger = logging.getLogger(__name__)

import config

def send_ao_metrics(freezer):
    try:
        logger.debug("Sending metrics to AppOptics")
        q = ao.new_queue()
        for t,n in zip(freezer.TEMP.values(), freezer.TEMP):
            if t['temperature']:
                q.add(
                    'freezer.temperature',
                    t['temperature'],
                    tags={'type': t['type'], 'name': t['name']},
                    inherit_tags=True
                )
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

def send_influx_metrics(freezer):
    try:
        logger.info("Sending metrics to InfluxDB")
        client = InfluxDBClient(host=config.INFLUXDB["HOST"], port=8086, database='freezer', timeout=5)

        current_time = datetime.datetime.utcnow()

        if freezer.COMP_STATE == 1:
            COMP_STATE = "ON"
        else:
            COMP_STATE = "OFF"

        json_body = [
            {
                "measurement": "humidity",
                "tags": {
                    "type": "i2c",
                    "environment": config.ENVIRONMENT,
                },
                "time": current_time,
                "fields": {
                    "value": freezer.HUMIDITY
                }
            },
            {
                "measurement": "compressor",
                "tags": {
                    "environment": config.ENVIRONMENT,
                    "state": COMP_STATE
                },
                "time": current_time,
                "fields": {
                    "value": 1
                }
            }
        ]

        # Add temperatues to json_body:
        for t,n in zip(freezer.TEMP.values(), freezer.TEMP):
            if t['temperature']:
                logger.debug("Current temperature %s: %.2f, type: %s" % (n, t['temperature'], t['type']))
                temp_object = {
                    "measurement": "temperature",
                    "tags": {
                        "type": t['type'],
                        "environment": config.ENVIRONMENT
                    },
                    "time": str(current_time),
                     "fields": {
                        "value": float(t['temperature']),
                        "name": n
                     }
                }
                json_body.append(temp_object)

        client.create_database("freezer")
        client.write_points(json_body)

    except Exception as e:
        logger.error("An ERROR occured while sending metrics to InfluxDB")
        print(e)
        pass

from influxdb import InfluxDBClient
import appoptics_metrics
import logging
import datetime

logger = logging.getLogger(__name__)

import config

def send_ao_metrics(freezer):
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

def send_influx_metrics(freezer):
    try:
        current_time = datetime.datetime.now()
        logger.info("Sending metrics to InfluxDB")
        client = InfluxDBClient(host='10.1.0.1', port=8086, database='freezer', timeout=5)
        json_body = [
            {
                "measurement": "temperature",
                "tags": {
                    "type": "i2c",
                    "environment": config.ENVIRONMENT,
                },
                "time": current_time,
                "fields": {
                    "value": freezer.TEMP1
                }
            },
            {
                "measurement": "temperature",
                "tags": {
                    "type": "1w",
                    "environment": config.ENVIRONMENT,
                },
                "time": current_time,
                "fields": {
                    "value": freezer.TEMP2
                }
            }
        ]
        client.create_database("freezer")
        client.write_points(json_body)

    except Exception as e:
        logger.error("An ERROR occured while sending metrics to InfluxDB")
        print(e)
        pass

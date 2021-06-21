from datetime import date, datetime, timedelta
import paho.mqtt.client as mqtt
import redis
import time
import json
import os

# Global definitions
broker_host = os.environ['MQTT_HOST']
readout_frequency = 5
timezone_offset = 2

# Initialize redis database
cache = redis.Redis(host='redis', port=6379, charset="utf-8", decode_responses=True)

# Initialize mqtt client
client = mqtt.Client()

# Connect to mqtt client and start loop
client.connect(broker_host)
client.loop_start()

# Check regularly if token is valid
qr_token = "oiuug8gzpbb"
while True:
    week = datetime.today().weekday()
    slot = (datetime.now().hour + timezone_offset) // 6
    bookings = cache.scan(match=f'slot:{week}:{slot}:*', count=280)[1]
    for booking in bookings:
        booking_token = cache.hget(booking, 'token')
        print(booking + ': ' + booking_token)
        if booking_token == qr_token:
            client.publish('time-slot-validation/0/value/door/setpoint', json.dumps({"open": "true"}))
            break
    time.sleep(readout_frequency)

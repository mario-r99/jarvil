from datetime import datetime
from pyzbar import pyzbar
import paho.mqtt.client as mqtt
import redis
import cv2
import pytz
import json
import os

# Global definitions
broker_host = os.environ['MQTT_HOST']
timezone = 'Europe/Berlin'

# Initialize redis database
cache = redis.Redis(host='redis', port=6379, charset="utf-8", decode_responses=True)

# Initialize mqtt client
client = mqtt.Client()

# Connect to mqtt client and start loop
client.connect(broker_host)
client.loop_start()

# Set up camera
camera = cv2.VideoCapture(0)
ret, frame = camera.read()

# Decode barcode
def read_barcode(frame):
    barcodes = pyzbar.decode(frame)
    if len(barcodes) > 0:
        return barcodes[0].data.decode('utf-8')

def validate_token(scanned_token):
    current_datetime = datetime.now(pytz.timezone(timezone))
    print(current_datetime)
    week = current_datetime.weekday()
    slot = (current_datetime.hour) // 6
    print(f'Scanning for week {week} in slot {slot}...')
    bookings = cache.scan(match=f'slot:{week}:{slot}:*', count=280)[1]
    print(bookings)
    for booking in bookings:
        booking_token = cache.hget(booking, 'token')
        print(booking + ': ' + booking_token)
        if booking_token == scanned_token:
            print('Token is valid, sending mqtt message...')
            client.publish('time-slot-validation/0/value/door/setpoint', json.dumps({"open": "true"}))
            return
    print('Token not valid')

# Camera reading
previous_data = None
while ret:
    ret, frame = camera.read()
    data = read_barcode(frame)
    # If data exists and is not used before
    if data is not None and data != previous_data:
        previous_data = data
        print('QR code detected: ' + data)
        validate_token(data)

camera.release()

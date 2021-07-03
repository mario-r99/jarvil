import paho.mqtt.client as mqtt
import pyfirmata
import time
import os
import json

# Global definitions
broker_host = os.environ['MQTT_HOST']
usb_port = os.environ['USB_PORT']
brightness_port = os.environ['BRIGHTNESS_PORT']
sensors_topic = "climate-service/0/value/sensors/state"
readout_frequency = 1

# Client initialization
client = mqtt.Client()

# Connect to mqtt broker and start loop
client.connect(broker_host)
client.loop_start()

# Setup arduino connection
board = pyfirmata.Arduino(usb_port)
board.analog[int(brightness_port)].mode = pyfirmata.INPUT  
it = pyfirmata.util.Iterator(board)  
it.start()

# Sensor readout loop
while True:
    brightness_state = board.analog[int(brightness_port)].read()
    # TODO
    temperature_state = 0
    # TODO
    humidity_state = 0

    sensor_status = {"brightness":brightness_state,
                     "temperature":temperature_state,
                     "humidity":humidity_state}
    
    sensor_status_out = json.dumps(sensor_status)

    print("Publishing sensor status:", sensor_status_out)
    client.publish(sensors_topic, sensor_status_out)

    time.sleep(readout_frequency)

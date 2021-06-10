import paho.mqtt.client as mqtt
import pyfirmata
import time
import os
import json

# Global definitions
broker_host = os.environ['MQTT_HOST']
usb_port = os.environ['USB_PORT']
brightness_port = os.environ['BRIGHTNESS_PORT']
sensors_topic = "pi-3/climate-service/value/sensors/state"
readout_frequency = 1

# Client initialization
client = mqtt.Client()

# Connect to mqtt client and start loop
client.connect(broker_host)
client.loop_start()

# Setup arduino connection
board = pyfirmata.Arduino(usb_port)
board.analog[brightness_port].mode = pyfirmata.INPUT  
it = pyfirmata.util.Iterator(board)  
it.start()

# Sensor readout loop
while True:
    brightness_state = board.analog[brightness_port].read()
    temperature_state = "comming soon"
    humidity_state = "comming soon"

    sensor_status = {"brightness":brightness_state,
                     "temperature":temperature_state,
                     "humidity":humidity_state}
    
    sensor_status_out = json.dumps(sensor_status)

    print("Publishing sensor status:", sensor_status_out)
    client.publish(sensors_topic, sensor_status_out)
    time.sleep(readout_frequency)

import paho.mqtt.client as mqtt
import pyfirmata
import time
import json

# Global definitions
broker_host = "localhost"
usb_port = 'COM6'
brightness_port = 0
sensors_topic = "pc-1/climate-service/0/value/sensors/state"

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
    # TODO
    temperature_state = 0.0
    # TODO
    humidity_state = 0.0

    if (brightness_state == None or temperature_state == None or humidity_state == None):
        continue

    sensor_status = {"brightness":brightness_state,
                     "temperature":temperature_state,
                     "humidity":humidity_state}
    
    sensor_status_out = json.dumps(sensor_status)

    print("Publishing brightness:", sensor_status_out)
    client.publish(sensors_topic, sensor_status_out)

    time.sleep(readout_frequency)

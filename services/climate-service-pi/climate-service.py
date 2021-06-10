import paho.mqtt.client as mqtt
import pyfirmata
import time
import os

# Global definitions
broker_host = os.environ['MQTT_HOST']
usb_port = os.environ['USB_PORT']
brightness_port = os.environ['BRIGHTNESS_PORT']
brightness_topic = "pi-3/climate-service/value/brightness/state"
readout_frequency = 1

# Client initialization
client = mqtt.Client()

# Connect to mqtt client and start loop
client.connect(broker_host)
client.loop_start()

# Setup arduino connection
board = pyfirmata.Arduino(usb_port)
board.analog[int(brightness_port)].mode = pyfirmata.INPUT  
it = pyfirmata.util.Iterator(board)  
it.start()

# Sensor readout loop
while True:
    brightness = board.analog[int(brightness_port)].read()
    print("Publishing brightness:", brightness)
    client.publish(brightness_topic, brightness)
    time.sleep(readout_frequency)

import paho.mqtt.client as mqtt
import pyfirmata
import time

# Global definitions
broker_host = "mqtt-broker"
usb_port = '/dev/ttyACM0'
brightness_topic = "pi-3/environment-service/value/brightness/state"
readout_frequency = 1

# Client initialization
client = mqtt.Client()

# Connect to mqtt client and start loop
client.connect(broker_host)
client.loop_start()

# Setup arduino connection
board = pyfirmata.Arduino(usb_port)
board.analog[0].mode = pyfirmata.INPUT  
it = pyfirmata.util.Iterator(board)  
it.start()

# Sensor readout loop
while True:
    brightness = board.analog[0].read()
    print("Publishing brightness:", brightness)
    client.publish(brightness_topic, brightness)
    time.sleep(readout_frequency)

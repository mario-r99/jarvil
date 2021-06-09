import paho.mqtt.client as mqtt
import pyfirmata
import time

# Global definitions
broker_host = "localhost"
usb_port = 'COM6'
brightness_port = 0
brightness_topic = "pc/climate-service/value/brightness/state"
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
    brightness = board.analog[brightness_port].read()
    print("Publishing brightness:", brightness)
    client.publish(brightness_topic, brightness)
    time.sleep(readout_frequency)

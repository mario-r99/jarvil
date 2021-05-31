import paho.mqtt.client as mqtt
import pyfirmata
import time

# Global definitions
broker_host = "mqtt-broker"
mqtt_topic = "room/brightness"
readout_frequency = 1

# Client initialization
client = mqtt.Client()

# Connect to mqtt client and start loop
client.connect(broker_host)
client.loop_start()

# Setup arduino connection
board = pyfirmata.Arduino('/dev/ttyACM0')
board.analog[0].mode = pyfirmata.INPUT  
it = pyfirmata.util.Iterator(board)  
it.start()

# Sensor readout loop
while True:
    brightness = board.analog[0].read()
    print("Publishing brightness:", brightness)
    client.publish(mqtt_topic, brightness)
    time.sleep(readout_frequency)

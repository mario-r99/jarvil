import paho.mqtt.client as mqtt
import os

# Global definitions
broker_host = os.environ['MQTT_HOST']

# Client initialization
client = mqtt.Client()

# Connect to mqtt client and start loop
client.connect(broker_host)
client.loop_start()


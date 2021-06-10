import paho.mqtt.client as mqtt
import os
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# Global definitions
host = os.environ['MQTT_HOST']
# Subscribing only value state logs
topic = "+/+/value/+/state"

# You can generate a Token from the "Tokens Tab" in the UI
token = os.environ['TOKEN']
org = os.environ['ORG']
bucket = os.environ['jarvil-bucket']
client = InfluxDBClient(url="http://influxdb:8086", token=token)
write_api = client.write_api(write_options=SYNCHRONOUS)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    decoded_payload =msg.payload.decode('UTF-8')
    value_name = msg.topic.split("/")[-1]
    device_id = msg.topic.split("/")[0]
    service_name = msg.topic.split("/")[1]
    print(msg.topic+": "+decoded_payload)
    data = f"{service_name},host={device_id} {value_name}={decoded_payload}"
    write_api.write(bucket, org, data)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(host)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()

def log_climate(service_name,device_id,value_name,payload):
    data = f"{service_name},host={device_id} {value_name}={payload}"
    write_api.write(bucket, org, data)
    return

def log_time_slot_booking(service_name,device_id,value_name,payload):
    return
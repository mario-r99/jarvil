import paho.mqtt.client as mqtt
import os
import json
from functools import partial
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# Global definitions
host = os.environ['MQTT_HOST']
# Subscribing only value state logs
topic = "+/+/value/+/state"

# Environmental variables
token = os.environ['TOKEN']
org = os.environ['ORG']
bucket = os.environ['BUCKET']

client = InfluxDBClient(url="http://influxdb:8086", token=token)
write_api = client.write_api(write_options=SYNCHRONOUS)

def log_climate(service_name,device_id,value_name,payload):
    name = service_name + "_" + value_name
    data=json.loads(payload)
    for key in data:
        log = f"{name},host={device_id} {key}={data[key]}"
        print(f"Write {service_name} log: {log}")
        write_api.write(bucket, org, log)
    return

def log_time_slot_booking(service_name,device_id,value_name,payload):
    data=json.loads(payload)
    name = service_name + "_" + value_name
    email = data["email"]
    first_second_name = data["firstname"]+"_"+data["lastname"]
    log = f"{name},host={device_id} {first_second_name}=\"{email}\""
    write_api.write(bucket, org, log)
    print(f"Write {service_name} log: {log}")
    for slot in data["bookings"]:
        slotID = slot["week"]*10+slot["slot"]
        log = f"{name},host={device_id} {email}={slotID}"
        print(f"Write {service_name} log: {log}")
        write_api.write(bucket, org, log)
    return

def invalid_service(service_name):
    print("Error: Invalid service name - ",service_name)
    return

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    decoded_payload =str(msg.payload.decode('UTF-8'))
    print("Received payload: " + decoded_payload + ", on topic: " + msg.topic)
    value_name = msg.topic.split("/")[-2]
    device_id = msg.topic.split("/")[0]
    service_name = msg.topic.split("/")[1]

    if service_name == "climate-service":
        log_climate(service_name,device_id,value_name,decoded_payload)
    elif service_name == "time-slot-booking":
        log_time_slot_booking(service_name,device_id,value_name,decoded_payload)
    else:
        invalid_service(service_name)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(host)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
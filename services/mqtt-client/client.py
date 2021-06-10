import paho.mqtt.client as mqtt
import os
import json
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# Global definitions
host = os.environ['MQTT_HOST']
# Subscribing only value state logs
topic = "+/+/value/+/state"

# You can generate a Token from the "Tokens Tab" in the UI
# token = os.environ['TOKEN']
# org = os.environ['ORG']
# bucket = os.environ['BUCKET']
# print(f"token {token}, type {type(token)}")
# print(f"token {org}, type {type(org)}")
# print(f"token {bucket}, type {type(bucket)}")

token = "V_g3T7i-QyHF3e_uDvBE05MRVKd-234xHwLDACXuw457UnhEBFOVP1Cr5IVb1EclrG6IRS5uBjMbOhMidnu8kA=="
org = "jarvil"
bucket = "jarvil-bucket"
client = InfluxDBClient(url="http://influxdb:8086", token=token)
write_api = client.write_api(write_options=SYNCHRONOUS)

def log_climate(service_name,device_id,value_name,payload):
    name = service_name + "_" + value_name
    data=json.loads(payload)
    print(f"data output {data}, type {type(data)}")
    for key in data:
        print(f"key output {key}, type {type(key)}")
        print(f"data[key] output {data[key]}, type {type(data[key])}")
        # log = f"{name},host={device_id} {key}={data[key]}"
        # log = "mem,host=host1 used_percent=23.43234543"
        # print("Write log: ", log)
        # write_api.write(bucket, org, log)
    return

def log_time_slot_booking(service_name,device_id,value_name,payload):
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

    log = "mem,host=host1 used_percent=23.43234543"
    print("1Write log: ", log)
    write_api.write(bucket, org, log)

    switcher = {
        "climate-service": log_climate(service_name,device_id,value_name,decoded_payload),
        "time-slot-booking": log_time_slot_booking(service_name,device_id,value_name,decoded_payload)
    }
# TODO: ad lambda method for switch
    switcher.get(service_name)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(host)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
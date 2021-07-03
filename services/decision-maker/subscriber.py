import paho.mqtt.client as mqtt
import os
import json

host = os.environ['MQTT_HOST']

# Subscribing only value state and setpoint logs
topic_state = "+/+/value/+/state"
topic_setpoint = "+/+/value/+/setpoint"

# Logging functions to influxdb
def log_climate(service_name,device_id,value_name,payload):
    measurement_name = service_name + "_" + value_name
    data=json.loads(payload)
    for key in data:
        log = f"{measurement_name},host={device_id} {key}={data[key]}"
    return

def log_setpoint(service_name, device_id, value_name, payload):
    measurement_name = service_name + "_" + value_name
    data=json.loads(payload)
    for key in data:
        log = f"{measurement_name},host={device_id} {key}={data[key]}"
    return

def invalid_service(service_name):
    print("Error: Invalid service name - ",service_name)
    return

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic_state)
    client.subscribe(topic_setpoint)

def on_message(client, userdata, msg):
    decoded_payload =str(msg.payload.decode('UTF-8'))
    print("Received payload: " + decoded_payload + ", on topic: " + msg.topic)
    value_name = msg.topic.split("/")[-2]
    device_id = msg.topic.split("/")[1]
    service_name = msg.topic.split("/")[0]
    
    if service_name == "climate-service":
        log_climate(service_name,device_id,value_name,decoded_payload)
    elif service_name == "control-dashboard":
        log_setpoint(service_name, device_id, value_name, decoded_payload)
    else:
        invalid_service(service_name)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(host)

client.loop_forever()
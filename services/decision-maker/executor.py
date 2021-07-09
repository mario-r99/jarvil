import os
import time
import requests
import paho.mqtt.client as mqtt
import json

# Global definitions
broker_host = os.environ['MQTT_HOST']
# publish_frequency = 10
actuator_status = {"thermostat": False,
                   "humidifier": False,
                   "airfilter": False,
                   "light": False}
mqtt_data = {"temperature_log":24,"temperature_def":20, # initial definiton
             "brightness_log":0.8,"brightness_def":0.8, # so that the state is fully defined
             "humidity_log":0.5,"humidity_def":0.5,
             "aircondition_log":0.5,"aircondition_def":0.5
             }

topic_climate = "climate-service/+/value/sensors/state"
topic_dashboard = "control-dashboard/+/value/+/setpoint"
topic_decision = "decision-maker/0/value/actuators/setpoint"
topic_door = "time-slot-validation/0/value/door/setpoint"
# last_sending_time = time.time() - publish_frequency

# # Client initialization
client = mqtt.Client()

def execute_planner():
    print("Create a plan")
    os.system("python -m py2pddl.parse climate_planner.py")

    data = {'domain': open('domain.pddl', 'r').read(),
            'problem': open('problem.pddl', 'r').read()}

    responce = requests.post('http://solver.planning.domains/solve', json=data).json()

    print("Executing the plan")
    try:
        for act in responce['result']['plan']:
            print(str(act['name']))
            action = str(act['name'])[1:-1].split()
            if action[0] == 'switch-on':
                actuator_status[action[2]] = True
            if action[0] == 'wait-increase':
                actuator_status[action[2]] = True
            if action[0] == 'switch-off':
                actuator_status[action[2]] = False
            if action[0] == 'wait-decrease':
                actuator_status[action[2]] = False
            if action[0] == 'energy-eco':
                actuator_status[action[2]] = False
    except:
        print("zero plan")

    actuator_status_out = json.dumps(actuator_status)

    print(f"Publishing actuators setpoints: {actuator_status_out}, on topic: {topic_decision}")
    client.publish(topic_decision, actuator_status_out)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic_climate)
    client.subscribe(topic_dashboard)
    client.subscribe(topic_door)

def on_message(client, userdata, msg):
    # Compute only if last sending time is older than readout frequency
    decoded_payload =str(msg.payload.decode('UTF-8'))
    print(f"Received payload: {decoded_payload}, on topic: {msg.topic}")
    value_name = msg.topic.split("/")[-2]
    service_name = msg.topic.split("/")[0]

    if service_name == "climate-service":
        if value_name == "sensors":
            mqtt_data["temperature_log"] = json.loads(decoded_payload)["temperature"]
            mqtt_data["brightness_log"] = json.loads(decoded_payload)["brightness"]
            mqtt_data["humidity_log"] = json.loads(decoded_payload)["humidity"]
            mqtt_data["aircondition_log"] = json.loads(decoded_payload)["aircondition"]
        else:
            print("ERROR: undefined vaue name - ", value_name)

    elif service_name == "control-dashboard":
        if value_name == "temperature":
            mqtt_data["temperature_def"] = json.loads(decoded_payload)["set"]
        elif value_name == "brightness":
            mqtt_data["brightness_def"] = json.loads(decoded_payload)["set"]
        elif value_name == "humidity":
            mqtt_data["humidity_def"] = json.loads(decoded_payload)["set"]
        elif value_name == "aircondition":
            mqtt_data["aircondition_def"] = json.loads(decoded_payload)["set"]
        else:
            print("ERROR: undefined value name - ", value_name)

    elif service_name == "time-slot-validation":
        if value_name == "door":
            mqtt_data["occupancy_log"] = json.loads(decoded_payload)["open"]

    print(mqtt_data)
    os.environ["MQTT_DATA"] = json.dumps(mqtt_data)
    execute_planner()

    # Execute panner only if last update is older than update frequency
    # global last_sending_time
    # current_time = time.time()
    # if current_time - last_sending_time > publish_frequency:
    #     last_sending_time = current_time
    #     print(mqtt_data)
    #     os.environ["MQTT_DATA"] = json.dumps(mqtt_data)
    #     execute_planner()

# first plan
execute_planner()

client.on_connect = on_connect
client.on_message = on_message


# # Connect to mqtt broker and start loop
client.connect(broker_host)
client.loop_forever()


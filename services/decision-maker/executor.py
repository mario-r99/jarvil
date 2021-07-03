import os
import time
import requests
import paho.mqtt.client as mqtt
import json


# Global definitions
broker_host = os.environ['MQTT_HOST']
publish_frequency = 10
actuator_status = {}

# Client initialization
client = mqtt.Client()

# Connect to mqtt broker and start loop
client.connect(broker_host)
client.loop_start()

while(True):
    os.system("python -m py2pddl.parse climate_planner.py")

    data = {'domain': open('domain.pddl', 'r').read(),
            'problem': open('problem.pddl', 'r').read()}

    responce = requests.post('http://solver.planning.domains/solve', json=data).json()

    print("whole responce: ", str(responce))

    for act in responce['result']['plan']:
        print(str(act['name']))
        if act['name'][0] == 'switch_on':
            actuator_status[act['name'][2]] = True
        if act['name'][0] == 'switch_off':
            actuator_status[act['name'][2]] = False
        if act['name'][0] == 'energy_eco':
            actuator_status[act['name'][2]] = False

    actuator_status_out = json.dumps(actuator_status)

    print("Publishing sensor status:", actuator_status_out)
    # client.publish(actuator_topic, actuator_status_out)

    time.sleep(publish_frequency)


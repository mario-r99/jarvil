import os
import time
import requests
import paho.mqtt.client as mqtt
import json

# # Global definitions
# broker_host = os.environ['MQTT_HOST']
publish_frequency = 10
actuator_status = {}

# # Client initialization
# client = mqtt.Client()

# # Connect to mqtt broker and start loop
# client.connect(broker_host)
# client.loop_start()

state = {'temperature_log':24,
         'temperature_set':20}

while(True):
    print('Am here!')
    os.system("python -m py2pddl.parse climate_planner.py")

    data = {'domain': open('domain.pddl', 'r').read(),
            'problem': open('problem.pddl', 'r').read()}

    responce = requests.post('http://solver.planning.domains/solve', json=data).json()

    for act in responce['result']['plan']:
        print(str(act['name']))
        action = str(act['name'])[1:-1].split()
        if action[0] == 'switch-on':
            actuator_status[action[2]] = True
        if action[0] == 'switch-off':
            actuator_status[action[2]] = False
        if action[0] == 'energy-eco':
            actuator_status[action[2]] = False

    actuator_status_out = json.dumps(actuator_status)

    print("Publishing sensor status:", actuator_status_out)
    # client.publish(actuator_topic, actuator_status_out)

    time.sleep(publish_frequency)


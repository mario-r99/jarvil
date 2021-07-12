import paho.mqtt.client as mqtt
import pyfirmata
import time
import os
import json
import threading

actuator_setpoint = {"open": False}

# Sensor readout loop
def publishingloop():
    # Global definitions
    broker_host = os.environ['MQTT_HOST']
    usb_port = os.environ['USB_PORT']
    door_port = int(os.environ['DOOR_PORT'])

    door_state_topic = "door-service/0/value/door/state"
    readout_frequency = 1

    # Client initialization
    client = mqtt.Client()

    # Connect to mqtt client and start loop
    client.connect(broker_host)
    client.loop_start()

    # Setup arduino connection
    board = pyfirmata.Arduino(usb_port)
    board.analog[door_port].mode = pyfirmata.OUTPUT
    it = pyfirmata.util.Iterator(board)
    it.start()

    while True:

        # Set actuators
        board.digital[door_port].write(actuator_setpoint["open"])
        
        #Read actuator status
        door_state = board.digital[door_port].read()

        if (door_state == None):
            print("door state recieves None!")
            time.sleep(readout_frequency)
            continue

        ## Logging data 
        actuator_status = {"open":door_state}

        actuator_status_out = json.dumps(actuator_status)

        print("Publishing actuators status:", actuator_status_out)
        client.publish(door_state_topic, actuator_status_out)

        time.sleep(readout_frequency)

def subscribingloop():
    # Global definitions
    broker_host = os.environ['MQTT_HOST']
    global actuator_setpoint

    door_setpoint_topic = "time-slot-validation/0/value/door/setpoint"

    # # Client initialization
    client = mqtt.Client()
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe(door_setpoint_topic)

    def on_message(client, userdata, msg):
        # Compute only if last sending time is older than readout frequency
        decoded_payload =str(msg.payload.decode('UTF-8'))
        print(f"Received payload: {decoded_payload}, on topic: {msg.topic}")
        data=json.loads(decoded_payload)
        for key in data:
            actuator_setpoint[key] = data[key]

    print("Initial state: ", actuator_setpoint)

    client.on_connect = on_connect
    client.on_message = on_message


    # # Connect to mqtt broker and start loop
    client.connect(broker_host)
    client.loop_forever()

thread1 = threading.Thread(target=publishingloop)
thread1.start()

thread2 = threading.Thread(target=subscribingloop)
thread2.start()

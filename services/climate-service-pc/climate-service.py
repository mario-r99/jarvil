import paho.mqtt.client as mqtt
import pyfirmata
import time
import json
# import RPi.GPIO as GPIO
# import Adafruit_DHT
import threading

actuator_setpoint = {"thermostat": False,
                    "humidifier": False,
                    "airfilter": False,
                    "light": False}

# Sensor readout loop
def publishingloop():
    # Global definitions
    broker_host = "localhost"
    usb_port = 'COM4'
    brightness_port = 0
    air_port = 5
    # temperature_port = 1
    dht11_port = 2
    light_port = 8
    airfilter_port = 9
    humidifier_port = 10
    thermostat_port = 11

    sensors_topic = "climate-service/value/sensors/state"
    actuator_state_topic = "climate-service/value/actuators/state"
    readout_frequency = 2


    # Client initialization
    client = mqtt.Client()

    # Connect to mqtt client and start loop
    client.connect(broker_host)
    client.loop_start()

    # Setup arduino connection
    board = pyfirmata.Arduino(usb_port)
    board.analog[brightness_port].mode = pyfirmata.INPUT
    board.analog[air_port].mode = pyfirmata.INPUT
    board.digital[light_port].mode = pyfirmata.OUTPUT
    board.digital[airfilter_port].mode = pyfirmata.OUTPUT
    board.digital[humidifier_port].mode = pyfirmata.OUTPUT
    board.digital[thermostat_port].mode = pyfirmata.OUTPUT
    it = pyfirmata.util.Iterator(board)
    it.start()

    while True:
        #Read sensor status
        brightness_state = board.analog[brightness_port].read()
        air_state = board.analog[air_port].read()
        
        # TODO
        humidity_state = 0.0
        temperature_state = 0.0

        #Read actuator status

        if (brightness_state == None or 
            air_state == None or
            temperature_state == None or 
            humidity_state == None):
            print("one of the sensors recieves None data!")
            time.sleep(readout_frequency)
            continue

        # Set actuators
        board.digital[light_port].write(not actuator_setpoint["light"])
        board.digital[airfilter_port].write(not actuator_setpoint["airfilter"])
        board.digital[humidifier_port].write(not actuator_setpoint["humidifier"])
        board.digital[thermostat_port].write(not actuator_setpoint["thermostat"])
        
        #Read actuator status
        light_state = not board.digital[light_port].read()
        airfilter_state = not board.digital[airfilter_port].read()
        humidifier_state = not board.digital[humidifier_port].read()
        thermostat_state = not board.digital[thermostat_port].read()
        if (light_state == None or 
            airfilter_state == None or
            humidifier_state == None or
            thermostat_state == None):
            print("one of the actuators recieves None data!")
            time.sleep(readout_frequency)
            continue

        ## Logging data 
        sensor_status = {"brightness":brightness_state,
                        "air":air_state,
                        "temperature":temperature_state,
                        "humidity":humidity_state}

        actuator_status = {"light":light_state,
                        "airfilter":airfilter_state,
                        "humidifier":humidifier_state,
                        "thermostat":thermostat_state}
        
        sensor_status_out = json.dumps(sensor_status)
        actuator_status_out = json.dumps(actuator_status)

        print("Publishing sensor status:", sensor_status_out)
        client.publish(sensors_topic, sensor_status_out)

        print("Publishing actuators status:", actuator_status_out)
        client.publish(actuator_state_topic, actuator_status_out)

        time.sleep(readout_frequency)

def subscribingloop():
    # Global definitions
    broker_host = "localhost"
    global actuator_setpoint

    topic_decision = "decision-maker/0/value/actuators/setpoint"

    # # Client initialization
    client = mqtt.Client()
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe(topic_decision)

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
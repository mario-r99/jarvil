import paho.mqtt.client as mqtt
import pyfirmata
import time
import json

# Global definitions
broker_host = "localhost"
usb_port = 'COM6'
brightness_port = 0
air_port = 5
temperature_port = 1
light_port = 8
sensors_topic = "pc-1/climate-service/value/sensors/state"
actuator_state_topic = "pc-1/climate-service/value/actuators/state"
readout_frequency = 2

# Configuration
brightness_switching_state = 0.75


# Client initialization
client = mqtt.Client()

# Connect to mqtt client and start loop
client.connect(broker_host)
client.loop_start()

# Setup arduino connection
board = pyfirmata.Arduino(usb_port)
board.analog[brightness_port].mode = pyfirmata.INPUT
board.analog[air_port].mode = pyfirmata.INPUT
board.analog[temperature_port].mode = pyfirmata.INPUT
board.digital[light_port].mode = pyfirmata.OUTPUT
it = pyfirmata.util.Iterator(board)
it.start()

# Sensor readout loop
while True:
    #Read sensor status
    brightness_state = board.analog[brightness_port].read()
    air_state = board.analog[air_port].read()
    temperature_state = board.analog[temperature_port].read()
    # TODO
    humidity_state = 0.0

    #Read actuator status
    # light_state = board.digital[light_port].read()

    if (brightness_state == None or 
        air_state == None or
        temperature_state == None or 
        humidity_state == None):
        print("one of the sensors recieves None data!")
        time.sleep(readout_frequency)
        continue

    # Set actuators
    if brightness_state < brightness_switching_state:
        board.digital[light_port].write(0)
    elif brightness_state >= brightness_switching_state:
        board.digital[light_port].write(1)

    #Read actuator status
    light_state = board.digital[light_port].read()
    if (light_state == None):
        print("one of the actuators recieves None data!")
        time.sleep(readout_frequency)
        continue

    ## Logging data 
    sensor_status = {"brightness":brightness_state,
                     "air":air_state,
                     "temperature":temperature_state,
                     "humidity":humidity_state}

    actuator_status = {"light":light_state}
    
    sensor_status_out = json.dumps(sensor_status)
    actuator_status_out = json.dumps(actuator_status)

    print("Publishing sensor status:", sensor_status_out)
    client.publish(sensors_topic, sensor_status_out)

    print("Publishing actuators state status:", actuator_status_out)
    client.publish(actuator_state_topic, actuator_status_out)

    time.sleep(readout_frequency)

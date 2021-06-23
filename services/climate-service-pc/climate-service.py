import paho.mqtt.client as mqtt
import pyfirmata
import time
import json
import datetime
# import array
import numpy as np

# Global definitions
broker_host = "localhost"
usb_port = 'COM6'
brightness_port = 0
air_port = 5
# temperature_port = 1
dht11_port = 2
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

def current_micros_time():
    return round(time.time() * 1000000)

# Setup arduino connection
board = pyfirmata.Arduino(usb_port)
board.analog[brightness_port].mode = pyfirmata.INPUT
board.analog[air_port].mode = pyfirmata.INPUT
# board.analog[temperature_port].mode = pyfirmata.INPUT
board.digital[light_port].mode = pyfirmata.OUTPUT
it = pyfirmata.util.Iterator(board)
it.start()
# starting_time_mcs = datetime.now().microseconds
starting_time_mcs = current_micros_time()

def delay_timer(delay_value):
    delay_time = current_micros_time()
    while (current_micros_time() - delay_time) < delay_value:
        pass

def read_DHT11(port):
    temp = 0
    hum = 0
    dht_error = False

    data_time = 0
    result = np.ndarray([])
    # dht_data = array("B")
    dht_data = np.ndarray([])
    data_array = 0
    # data_counter = 0
    block_dht = False

    # Trigger Sensor 
    board.digital[port].mode = pyfirmata.OUTPUT
    board.digital[port].write(1)
    delay_timer(250000) #Wait 250millisec
    board.digital[port].write(0)
    delay_timer(20000) #Wait 30millisec
    board.digital[port].write(1)
    delay_timer(40) #Wait 50microsec
    board.digital[port].mode = pyfirmata.INPUT
    delay_timer(50)
    while True:
        print("bug ",board.digital[port].read())


    while True:
        if board.digital[port].read() == 0 and block_dht == False:
            block_dht = True
            result[data_array] = current_micros_time() - starting_time_mcs - data_time
            data_array+=1
            data_time = current_micros_time() - starting_time_mcs
        # If DHT pin is low, go to next Dataset
        if board.digital[port].read() == 1:
            block_dht = False
        if ((current_micros_time() - starting_time_mcs - data_time) < 150): #if DTH Sensor high for more than 150 usec, leave loop
            break

    # Asign 1 or 0 to Result variable. If more than 80uS Data as "1"
    # Starting at Data set 02. First two Datasets are ignored!
    for i in range(2,data_array):
        if result[i] <= 90:
            result[i]=0
        else:
            result[i]=1
    
    dht_data = np.packbits(result[2:42].reshape((5,8)))

    if (dht_data[4]==np.sum(dht_data[:4])):
        hum = dht_data[0]
        temp = float(f"{dht_data[2]}.{dht_data[3]}")
        dht_error = False
    else:
        dht_error = True

    return temp, hum

# Sensor readout loop
while True:
    #Read sensor status
    brightness_state = board.analog[brightness_port].read()
    air_state = board.analog[air_port].read()
    # temperature_state = board.analog[temperature_port].read()
    temperature_state,humidity_state = read_DHT11(dht11_port)
    # TODO
    # humidity_state = 0.0

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

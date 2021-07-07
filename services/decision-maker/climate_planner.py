from py2pddl import Domain, create_type
from py2pddl import predicate, action
import os
import json

class ClimateDomain(Domain):

    Sensor = create_type("Sensor")
    Actuator = create_type("Actuator")
    Room = create_type("Room")
    Person = create_type("Person")

    @predicate(Actuator)
    def on(self, a):
        """Complete the method signature and specify
        the respective types in the decorator"""

    @predicate(Sensor)
    def low(self, s):
        """Complete the method signature and specify
        the respective types in the decorator"""

    @predicate(Sensor)
    def high(self, s):
        """Complete the method signature and specify
        the respective types in the decorator"""

    @predicate(Sensor, Actuator)
    def contol_with(self, s, a):
        """Complete the method signature and specify
        the respective types in the decorator"""
    
    @predicate(Room, Sensor, Actuator)
    def at(self, r, s, a):
        """Complete the method signature and specify
        the respective types in the decorator"""
    
    @predicate(Room, Person)
    def at_person(self, r, p):
        """Complete the method signature and specify
        the respective types in the decorator"""

    @action(Sensor, Actuator, Room, Person)
    def switch_on(self, s, a, r, p):
        precond = [self.at_person(r, p), self.contol_with(s, a), 
            self.at(r, s, a), self.low(s)]
        effect = [self.on(a), ~self.low(s)]
        return precond, effect

    @action(Sensor, Actuator, Room, Person)
    def switch_off(self, s, a, r, p):
        precond = [self.at_person(r, p), self.contol_with(s, a), 
            self.at(r, s, a), self.high(s)]
        effect = [~self.on(a), ~self.high(s)]
        return precond, effect

    @action(Sensor, Actuator, Room, Person)
    def energy_eco(self, s, a, r, p):
        precond = [~self.at_person(r, p), self.contol_with(s, a), 
            self.at(r, s, a)]
        effect = [~self.on(a), ~self.low(s), ~self.high(s)]
        return precond, effect
    

from py2pddl import goal, init

class ClimateProblem(ClimateDomain):

    def __init__(self):
        super().__init__()
        self.actuators = ClimateDomain.Actuator.create_objs(["thermostat", "humidifier", "airfilter", "light"])
        self.sensors = ClimateDomain.Sensor.create_objs(["temperature", "humidity", "aircondition", "brightness"])
        self.rooms = ClimateDomain.Room.create_objs(["workingArea", "bookcaseArea"])
        self.occupants = ClimateDomain.Person.create_objs(["occupant"])

    @init
    def init(self):

        # Static state
        at = [self.at_person(self.rooms["workingArea"], self.occupants["occupant"]),
        
    #   self.high(self.sensors["temperatureW"]),
        # self.on(self.actuators["thermostat"]),
        self.contol_with(self.sensors["temperature"], self.actuators["thermostat"]),
        self.at(self.rooms["workingArea"], self.sensors["temperature"], self.actuators["thermostat"]),

    #   self.low(self.sensors["temperatureB"]),
    #   self.contol_with(self.sensors["temperatureB"], self.actuators["thermostatB"]),
    #   self.at(self.rooms["bookcaseArea"], self.sensors["temperatureB"], self.actuators["thermostatB"]),

    #   self.low(self.sensors["humidity"]),
        # self.on(self.actuators["humidifier"]),
        self.contol_with(self.sensors["humidity"], self.actuators["humidifier"]),
        self.at(self.rooms["workingArea"], self.sensors["humidity"], self.actuators["humidifier"]),

    #   self.high(self.sensors["aircondition"]),
    #   self.on(self.actuators["airfilter"]),
        self.contol_with(self.sensors["aircondition"], self.actuators["airfilter"]),
        self.at(self.rooms["workingArea"], self.sensors["aircondition"], self.actuators["airfilter"]),

    #   self.low(self.sensors["brightness"]),
        self.contol_with(self.sensors["brightness"], self.actuators["light"]),
        self.at(self.rooms["workingArea"], self.sensors["brightness"], self.actuators["light"])]

        # Defining normal range
        epsilon_temperature = 0.5
        epsilon_humidity = 0.03
        epsilon_brightness = 0.03
        epsilon_aircondition = 0.03

        #Getting mqtt logs
        json_state = os.environ["MQTT_DATA"]
        print("Environment data: " + json_state)
        initial_state = json.loads(json_state)
        
        if initial_state != None:
            print("Reading out the predicates")
            if (initial_state['temperature_log']-initial_state['temperature_def'] >= epsilon_temperature):
                at.append(self.high(self.sensors["temperature"]))
            if (initial_state['temperature_log']-initial_state['temperature_def'] <= -epsilon_temperature):
                at.append(self.low(self.sensors["temperature"]))

            if (initial_state['humidity_log']-initial_state['humidity_def'] >= epsilon_humidity):
                at.append(self.high(self.sensors["humidity"]))
            if (initial_state['humidity_log']-initial_state['humidity_def'] <= -epsilon_humidity):
                at.append(self.low(self.sensors["humidity"]))

            if (initial_state['brightness_log']-initial_state['brightness_def'] >= epsilon_brightness):
                at.append(self.high(self.sensors["brightness"]))
            if (initial_state['brightness_log']-initial_state['brightness_def'] <= -epsilon_brightness):
                at.append(self.low(self.sensors["brightness"]))

            if (initial_state['aircondition_log']-initial_state['aircondition_def'] >= epsilon_aircondition):
                at.append(self.high(self.sensors["aircondition"]))
            if (initial_state['aircondition_log']-initial_state['aircondition_def'] <= -epsilon_aircondition):
                at.append(self.low(self.sensors["aircondition"]))

        return at

    @goal
    def goal(self):
        return [~self.low(self.sensors["temperature"]),~self.high(self.sensors["temperature"]),
                # ~self.low(self.sensors["temperatureB"]),~self.high(self.sensors["temperatureB"]),
                ~self.low(self.sensors["humidity"]),~self.high(self.sensors["humidity"]),
                ~self.low(self.sensors["aircondition"]),~self.high(self.sensors["aircondition"]),
                ~self.low(self.sensors["brightness"]),~self.high(self.sensors["brightness"])]
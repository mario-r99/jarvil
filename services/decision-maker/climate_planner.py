from py2pddl import Domain, create_type
from py2pddl import predicate, action
import os

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
            self.at(r, s, a), ~self.on(a), self.low(s)]
        effect = [self.on(a), ~self.low(s)]
        return precond, effect

    @action(Sensor, Actuator, Room, Person)
    def wait_increase(self, s, a, r, p):
        precond = [self.at_person(r, p), self.contol_with(s, a), 
            self.at(r, s, a), self.on(a), self.low(s)]
        effect = [~self.low(s)]
        return precond, effect

    @action(Sensor, Actuator, Room, Person)
    def switch_off(self, s, a, r, p):
        precond = [self.at_person(r, p), self.contol_with(s, a), 
            self.at(r, s, a), self.on(a), self.high(s)]
        effect = [~self.on(a), ~self.high(s)]
        return precond, effect

    @action(Sensor, Actuator, Room, Person)
    def wait_decrease(self, s, a, r, p):
        precond = [self.at_person(r, p), self.contol_with(s, a), 
            self.at(r, s, a), ~self.on(a), self.high(s)]
        effect = [~self.high(s)]
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
        self.actuators = ClimateDomain.Actuator.create_objs(["thermostatW", 
            "thermostatB", "humidifier", "airfilter", "light"])
        self.sensors = ClimateDomain.Sensor.create_objs(["temperatureW", 
            "temperatureB", "humidity", "airpolusion", "brightness"])
        self.rooms = ClimateDomain.Room.create_objs(["workingArea", "bookcaseArea"])
        self.occupants = ClimateDomain.Person.create_objs(["occupant"])

    @init
    def init(self):
        mqtt_data = os.environ["MQTT_DATA"]
        print("Environment data: " + mqtt_data)
        at = [self.at_person(self.rooms["workingArea"], self.occupants["occupant"]),
              
              self.high(self.sensors["temperatureW"]),
              self.on(self.actuators["thermostatW"]),
              self.contol_with(self.sensors["temperatureW"], self.actuators["thermostatW"]),
              self.at(self.rooms["workingArea"], self.sensors["temperatureW"], self.actuators["thermostatW"]),

              self.low(self.sensors["temperatureB"]),
              self.contol_with(self.sensors["temperatureB"], self.actuators["thermostatB"]),
              self.at(self.rooms["bookcaseArea"], self.sensors["temperatureB"], self.actuators["thermostatB"]),

              self.low(self.sensors["humidity"]),
              self.on(self.actuators["humidifier"]),
              self.contol_with(self.sensors["humidity"], self.actuators["humidifier"]),
              self.at(self.rooms["workingArea"], self.sensors["humidity"], self.actuators["humidifier"]),

              self.high(self.sensors["airpolusion"]),
            #   self.on(self.actuators["airfilter"]),
              self.contol_with(self.sensors["airpolusion"], self.actuators["airfilter"]),
              self.at(self.rooms["workingArea"], self.sensors["airpolusion"], self.actuators["airfilter"]),

              self.low(self.sensors["brightness"]),
              self.contol_with(self.sensors["brightness"], self.actuators["light"]),
              self.at(self.rooms["workingArea"], self.sensors["brightness"], self.actuators["light"])]
        return at

    @goal
    def goal(self):
        return [~self.low(self.sensors["temperatureW"]),~self.high(self.sensors["temperatureW"]),
                ~self.low(self.sensors["temperatureB"]),~self.high(self.sensors["temperatureB"]),
                ~self.low(self.sensors["humidity"]),~self.high(self.sensors["humidity"]),
                ~self.low(self.sensors["airpolusion"]),~self.high(self.sensors["airpolusion"]),
                ~self.low(self.sensors["brightness"]),~self.high(self.sensors["brightness"])]
(define
	(problem climate)
	(:domain climate)
	(:objects
		thermostat humidifier airfilter light - actuator
		occupant - person
		workingArea bookcaseArea - room
		temperature humidity aircondition brightness - sensor
	)
	(:init (at-person workingArea occupant) (contol-with temperature thermostat) (at workingArea temperature thermostat) (contol-with humidity humidifier) (at workingArea humidity humidifier) (contol-with aircondition airfilter) (at workingArea aircondition airfilter) (contol-with brightness light) (at workingArea brightness light) (low temperature) (low humidity) (high brightness))
	(:goal (and (not (low temperature)) (not (high temperature)) (not (low humidity)) (not (high humidity)) (not (low aircondition)) (not (high aircondition)) (not (low brightness)) (not (high brightness))))
)

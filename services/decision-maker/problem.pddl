(define
	(problem climate)
	(:domain climate)
	(:objects
		thermostatW thermostatB humidifier airfilter light - actuator
		occupant - person
		workingArea bookcaseArea - room
		temperatureW temperatureB humidity airpolusion brightness - sensor
	)
	(:init (at-person workingArea occupant) (high temperatureW) (on thermostatW) (contol-with temperatureW thermostatW) (at workingArea temperatureW thermostatW) (low temperatureB) (contol-with temperatureB thermostatB) (at bookcaseArea temperatureB thermostatB) (low humidity) (on humidifier) (contol-with humidity humidifier) (at workingArea humidity humidifier) (high airpolusion) (contol-with airpolusion airfilter) (at workingArea airpolusion airfilter) (low brightness) (contol-with brightness light) (at workingArea brightness light))
	(:goal (and (not (low temperatureW)) (not (high temperatureW)) (not (low temperatureB)) (not (high temperatureB)) (not (low humidity)) (not (high humidity)) (not (low airpolusion)) (not (high airpolusion)) (not (low brightness)) (not (high brightness))))
)

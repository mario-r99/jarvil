(define (problem jarvilProblem_1) (:domain JarvilLib_1)
(:objects 
thermostat_w thermostat_b humidifier airfilter light - actuator
temperature_w temperature_b humidity  airpolusion brightness - sensor
working_area bookcase_area - room
occupant - person
)

(:init
    (at_person working_area occupant)

    (high temperature_w)
    (on thermostat_w)
    (contol_with temperature_w thermostat_w)
    (at working_area temperature_w thermostat_w)

    (low temperature_b)
    (contol_with temperature_b thermostat_b)
    (at bookcase_area temperature_b thermostat_b)

    (low humidity)
    (on humidifier)
    (contol_with humidity humidifier)
    (at working_area humidity humidifier)

    (high airpolusion)
    (on airfilter)
    (contol_with airpolusion airfilter)
    (at working_area airpolusion airfilter)
    
    (low brightness)
    (contol_with brightness light)
    (at working_area brightness light)
)

(:goal (and
    (not(low temperature_w))
    (not(high temperature_w))
    (not(low temperature_b))
    (not(high temperature_b))
    (not(low humidity))
    (not(high humidity))
    (not(low airpolusion))
    (not(high airpolusion))
    (not(low brightness))
    (not(high brightness))
))

;un-comment the following line if metric is needed
;(:metric minimize (???))
)

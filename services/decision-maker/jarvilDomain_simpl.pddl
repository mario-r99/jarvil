(define (domain JarvilLib_1)

    (:requirements
        :strips
        :typing
        :negative-preconditions
    )

    (:types
        sensor actuator room person - object
    )

    (:predicates
        (on ?a - actuator)
        (low ?s - sensor)
        (high ?s - sensor)
        (contol_with ?s - sensor ?a - actuator)
        (at ?r - room ?s - sensor ?a - actuator)
        (at_person ?r - room ?p - person)
    )

  ;; comment
    (:action switch_on
        :parameters (?sens - sensor ?act - actuator ?room - room ?pers - person)
        :precondition (and (at_person ?room ?pers) (contol_with ?sens ?act) (at ?room ?sens ?act) (not(on ?act)) (low ?sens))
        :effect (and 
        (on ?act)
        (not(low ?sens))
        )
    )
   
    (:action switch_off
        :parameters (?sens - sensor ?act - actuator ?room - room ?pers - person)
        :precondition (and (at_person ?room ?pers) (contol_with ?sens ?act) (at ?room ?sens ?act) (on ?act) (high ?sens))
        :effect (and 
        (not(on ?act))
        (not(high ?sens))
        )
    )

    (:action energy_eco
        :parameters (?sens - sensor ?act - actuator ?room - room ?pers - person)
        :precondition (and (not(at_person ?room ?pers)) (contol_with ?sens ?act) (at ?room ?sens ?act))
        :effect (and 
        (not(on ?act))
        (not(high ?sens))
        (not(low ?sens))
        )
    )

    (:action wait_decrease
        :parameters (?sens - sensor ?act - actuator ?room - room ?pers - person)
        :precondition (and (at_person ?room ?pers) (contol_with ?sens ?act) (at ?room ?sens ?act) (not(on ?act)) (high ?sens))
        :effect (and 
        (not(high ?sens))
        )
    )

    (:action wait_increase
        :parameters (?sens - sensor ?act - actuator ?room - room ?pers - person)
        :precondition (and (at_person ?room ?pers) (contol_with ?sens ?act) (at ?room ?sens ?act) (on ?act) (low ?sens))
        :effect (and
        (not(low ?sens))
        )
    )

)
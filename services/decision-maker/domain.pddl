(define
	(domain climate)
	(:requirements :strips :typing)
	(:types
		actuator
		person
		room
		sensor
	)
	(:predicates
		(at ?r - room ?s - sensor ?a - actuator)
		(at-person ?r - room ?p - person)
		(contol-with ?s - sensor ?a - actuator)
		(high ?s - sensor)
		(low ?s - sensor)
		(on ?a - actuator)
	)
	(:action energy-eco
		:parameters (?s - sensor ?a - actuator ?r - room ?p - person)
		:precondition (and (not (at-person ?r ?p)) (contol-with ?s ?a) (at ?r ?s ?a))
		:effect (and (not (on ?a)) (not (low ?s)) (not (high ?s)))
	)
	(:action switch-off
		:parameters (?s - sensor ?a - actuator ?r - room ?p - person)
		:precondition (and (at-person ?r ?p) (contol-with ?s ?a) (at ?r ?s ?a) (on ?a) (high ?s))
		:effect (and (not (on ?a)) (not (high ?s)))
	)
	(:action switch-on
		:parameters (?s - sensor ?a - actuator ?r - room ?p - person)
		:precondition (and (at-person ?r ?p) (contol-with ?s ?a) (at ?r ?s ?a) (not (on ?a)) (low ?s))
		:effect (and (on ?a) (not (low ?s)))
	)
	(:action wait-decrease
		:parameters (?s - sensor ?a - actuator ?r - room ?p - person)
		:precondition (and (at-person ?r ?p) (contol-with ?s ?a) (at ?r ?s ?a) (not (on ?a)) (high ?s))
		:effect (not (high ?s))
	)
	(:action wait-increase
		:parameters (?s - sensor ?a - actuator ?r - room ?p - person)
		:precondition (and (at-person ?r ?p) (contol-with ?s ?a) (at ?r ?s ?a) (on ?a) (low ?s))
		:effect (not (low ?s))
	)
)
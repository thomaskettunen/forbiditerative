(define (domain logistics-strips)
  (:requirements :strips) 
  (:predicates 	(OBJ ?obj)
	       	(TRUCK ?truck)
               	(LOCATION ?loc)
		(CAR ?car)
                (LOCATION ?loc)
                (empty ?car) 
		(at ?obj ?loc)
		(in ?obj1 ?obj2))
  ; (:types )		; default object

(:action LOAD-TRUCK
  :parameters
   (?obj
    ?truck
    ?loc)
  :precondition
   (and (OBJ ?obj) (TRUCK ?truck) (LOCATION ?loc)
   (at ?truck ?loc) (at ?obj ?loc))
  :effect
   (and (not (at ?obj ?loc)) (in ?obj ?truck)))

(:action UNLOAD-TRUCK
  :parameters
   (?obj
    ?truck
    ?loc)
  :precondition
   (and (OBJ ?obj) (TRUCK ?truck) (LOCATION ?loc)
        (at ?truck ?loc) (in ?obj ?truck))
  :effect
   (and (not (in ?obj ?truck)) (at ?obj ?loc)))


(:action DRIVE-TRUCK
  :parameters
   (?truck
    ?loc-from
    ?loc-to
    )
  :precondition
   (and (TRUCK ?truck) (LOCATION ?loc-from) (LOCATION ?loc-to)
   (at ?truck ?loc-from))
  :effect
   (and (not (at ?truck ?loc-from)) (at ?truck ?loc-to)))

(:action LOAD-CAR
  :parameters
   (?obj
    ?car
    ?loc)
  :precondition
   (and (OBJ ?obj) (CAR ?car) (LOCATION ?loc)
   (at ?car ?loc) (at ?obj ?loc) (empty ?car))
  :effect
   (and (not (at ?obj ?loc)) (in ?obj ?car) (not (empty ?car))))

(:action UNLOAD-CAR
  :parameters
   (?obj
    ?car
    ?loc)
  :precondition
   (and (OBJ ?obj) (CAR ?car) (LOCATION ?loc)
        (at ?car ?loc) (in ?obj ?car))
  :effect
   (and (not (in ?obj ?car)) (at ?obj ?loc) (empty ?car)))


(:action DRIVE-CAR
  :parameters
   (?car
    ?loc-from
    ?loc-to
    )
  :precondition
   (and (CAR ?car) (LOCATION ?loc-from) (LOCATION ?loc-to)
   (at ?car ?loc-from))
  :effect
   (and (not (at ?car ?loc-from)) (at ?car ?loc-to)))
)
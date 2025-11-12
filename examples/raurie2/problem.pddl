(define (problem logistics-c3-s2-p2-a1)
(:domain logistics-strips)
(:objects t1 t2 
          la lb lc ld le
          p1 p2
)
(:init
    (CAR t1)
    (CAR t2)
    (LOCATION la)
    (LOCATION lb)
    (LOCATION lc)
    (LOCATION ld)
    (LOCATION le)
    (OBJ p1)
    (OBJ p2)
    (at t1 la)
    (at t2 lc)
    (at p1 lb)
    (at p2 lb)
    (empty t1)
    (empty t2)
    (connected la lb)
    (connected lb lc)
    (connected lb ld)
    (connected lb le)
)
(:goal
    (and
        (at p1 ld)
        (at p2 le)
    )
)
)
(define (problem logistics-c3-s2-p2-a1)
(:domain logistics-strips)
(:objects c0 c1
          t0 t1 
          l0 l1 l2 l3 l4 l5 l6
          p0 p1
)
(:init
    (TRUCK t0)
    (TRUCK t1)
    (CAR c0)
    (CAR c1)
    (LOCATION l0)
    (LOCATION l1)
    (LOCATION l2)
    (LOCATION l3)
    (LOCATION l4)
    (LOCATION l5)
    (LOCATION l6)
    (OBJ p0)
    (OBJ p1)
    (at t0 l0)
    (at t1 l0)
    (at c0 l0)
    (at c1 l0)
    (at p0 l0)
    (at p1 l0)
)
(:goal
    (and
        (at p0 l1)
        (at p1 l6)
        (at t0 l0)
        (at t1 l0)
        (at c0 l0)
        (at c1 l0)
    )
)
)
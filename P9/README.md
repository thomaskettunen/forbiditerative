# post_process of plans to filter out reorderings, operator dominance, or grouped operator dominance.

# Running
## Reordering Relation
```
# ./post_process.py <input-folder> <output-folder> <relation>
./post_process.py ../found_plans/done ../found_plans/unrelated_plans reorder
```
## Operator Dominance Relation
```
# ./post_process.py <input-folder> <output-folder> <relation>
./post_process.py ../found_plans/done ../found_plans/unrelated_plans operator_dominance
```
## Prefix Group Operator Dominance Relation
```
# ./post_process.py <input-folder> <output-folder> <relation>
./post_process.py ../found_plans/done ../found_plans/unrelated_plans prefix_group_operator_dominance
```
## Truck Group Operator Dominance Relation
```
# ./post_process.py <input-folder> <output-folder> <relation>
./post_process.py ../found_plans/done ../found_plans/unrelated_plans truck_group_operator_dominance
```
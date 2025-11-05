#!/bin/bash

# $1 domain
# $2 problem
# $3 number of plans (k)
# $4 quality bound (optional)

if [ "$#" -lt 3 ] || [ "$#" -gt 4 ]; then
    echo "Illegal number of parameters"
    exit 1
fi

QBOUND=""
if [ "$#" -eq 4 ]; then
    QBOUND="--quality-bound $4"
fi

SOURCE="$( dirname "${BASH_SOURCE[0]}" )"
export PYTHONPATH=$PWD && $SOURCE/forbiditerative/plan.py --planner submultisets_topk --domain $1 --problem $2 --number-of-plans $3 $QBOUND --use-local-folder --clean-local-folder --reordering "NONE" #--suppress-planners-output
# export PYTHONPATH=$PWD && $SOURCE/forbiditerative/plan.py --planner submultisets_topk --domain $1 --problem $2 --number-of-plans $3 --symmetries --use-local-folder --keep-intermediate-tasks #--clean-local-folder --suppress-planners-output


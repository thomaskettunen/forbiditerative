#!/bin/bash

# $1 domain
# $2 problem
# $3 number of plans (k)

NUM_REQUIRED_ARGS=3

if [ "$#" -lt $NUM_REQUIRED_ARGS ]; then
    echo "Illegal number of parameters"
    exit 1
fi

SOURCE="$(readlink -f "$(dirname "${BASH_SOURCE[0]}")")"
echo ""$(readlink -f "${BASH_SOURCE[0]}")":${LINENO} INFO Running: "$SOURCE/forbiditerative/plan.py" --planner supermultisetgroups_topk --domain $1 --problem $2 --number-of-plans $3 --use-local-folder --clean-local-folder "${@:NUM_REQUIRED_ARGS+1:9999}""

export PYTHONPATH="$SOURCE" && "$SOURCE/forbiditerative/plan.py" --planner supermultisetgroups_topk --domain $1 --problem $2 --number-of-plans $3 --use-local-folder --clean-local-folder "${@:NUM_REQUIRED_ARGS+1:9999}" # --suppress-planners-output # --reordering "NONE"
# export PYTHONPATH=$PWD && $SOURCE/forbiditerative/plan.py --planner supermultisetgroups_topk --domain $1 --problem $2 --number-of-plans $3 $QBOUND --symmetries --use-local-folder --keep-intermediate-tasks #--clean-local-folder --suppress-planners-output


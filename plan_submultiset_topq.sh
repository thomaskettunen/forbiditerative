#!/bin/bash
# $1 domain
# $2 problem
# $3 quality bound (>= 1.0)

NUM_REQUIRED_ARGS=3

if [ "$#" -lt $NUM_REQUIRED_ARGS ]; then
    echo "Illegal number of parameters"
    exit 1
fi

SOURCE="$(readlink -f "$(dirname "${BASH_SOURCE[0]}")")"
echo ""$(readlink -f "${BASH_SOURCE[0]}")":${LINENO} INFO Running: "$SOURCE/forbiditerative/plan.py" --planner submultisets_topq --domain $1 --problem $2 --quality-bound $3 --use-local-folder --clean-local-folder "${@:NUM_REQUIRED_ARGS+1:9999}""

export PYTHONPATH="$SOURCE" && "$SOURCE/forbiditerative/plan.py" --planner submultisets_topq --domain $1 --problem $2 --quality-bound $3 --use-local-folder --clean-local-folder "${@:NUM_REQUIRED_ARGS+1:9999}"

# export PYTHONPATH=$SOURCE && $SOURCE/forbiditerative/plan.py --planner submultisets_topq --domain $1 --problem $2 --quality-bound $3 $KBOUND --symmetries --use-local-folder --clean-local-folder --overall-time-limit 600 # --suppress-planners-output
# export PYTHONPATH=$PWD && $SOURCE/forbiditerative/plan.py --planner submultisets_topq --domain $1 --problem $2 --quality-bound $3 $KBOUND --symmetries --use-local-folder --keep-intermediate-tasks #--clean-local-folder --suppress-planners-output


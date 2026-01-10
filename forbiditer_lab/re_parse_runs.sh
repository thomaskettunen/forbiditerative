#!/bin/bash
[ -e ./data ] && { echo "./data exists. Exiting." ; exit 1; }

for name in ./runs/* ;
do echo "$name" ;
   mv "$name/data" ./data ;
   yes 'o' | ./run_experiments.sh -- 3 4 5 ;
   mv ./data "$name/data" ;
done ;
[ -e ./runs.zip ] && { echo "./runs.zip exists. moving to ./runs.zip.old" ; mv ./runs.zip ./runs.zip.old ; }
zip -r runs.zip runs
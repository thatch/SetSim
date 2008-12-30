#!/bin/bash

t=0
for n in `seq 100`; do
    d=$(python simulate_sets.py | grep draw | wc -l)
    echo -n .
    t=$(( $t + $d ))
done

echo
echo "Draw probability is $(dc -e "2 k $t 100 / p") per game"

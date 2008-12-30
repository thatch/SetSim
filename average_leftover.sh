#!/bin/bash

d=$(python simulate_sets.py 100 | grep exhausted | sed -e 's/.*(//' | \
awk '{print $1}' | awk '{ sum+= $1 } END { print sum }')

echo "Average leftovers are $(dc -e "2 k $d 100 / p") per game"

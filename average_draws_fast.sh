#!/bin/bash

d=$(python simulate_sets.py 100 | grep draw | wc -l)

echo "Draw probability is $(dc -e "2 k $d 100 / p") per game"

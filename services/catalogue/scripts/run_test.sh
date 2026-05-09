#!/bin/bash
for i in {1..5}; do
    python3 -m scripts.contention_script &
done
wait

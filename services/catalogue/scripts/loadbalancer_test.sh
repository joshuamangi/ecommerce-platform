#!/bin/bash
for i in {1..10}; do
    curl localhost:8000/api/catalogue/hostname
    echo
done

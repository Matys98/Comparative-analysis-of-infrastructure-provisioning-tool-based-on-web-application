#!/bin/bash

# Input values
while getopts a:t:p: flag
do
    case "${flag}" in
        a) APP_NAME=${OPTARG};;
        t) TOOL=${OPTARG};;
        p) PATH=${OPTARG};;
    esac
done

FILE=/tmp/exit.txt

if [ -f "$FILE" ]; then
    echo "file exists"
else
    # CPU & RAM
    ./benchmark_CPU_RAM.sh -n $TOOL-$APP_NAME &

    # Network
    ./benchmark_NET.sh -n $TOOL-$APP_NAME &
fi

#!/bin/bash

# Input values
while getopts n:l: flag
do
    case "${flag}" in
        n) LOG_NAME=${OPTARG};;
        l) LOG_PATH=${OPTARG};;
    esac
done

FILE=/tmp/exit.txt

i=0
while true
do  
    ((i++))
    time_with_ms=$(date +"%T.%3N")
    cpu_percentage=$(top -bn1 | awk '/^%Cpu/ {printf "%s",$2}')
    # cpu_core=$(top 1 -bn1 | awk '/^%Cpu0/ {printf "%f",$2}')
    mem_percentage=$(free | awk '/^Mem/ {printf "%f",$3/$2*100}')
    mem_kibibytes=$(free | awk '/^Mem/ {printf "%s",$3}')
    if [ $i == 1 ]; then
        echo "ID; Time; CPU %; MEM %; MEM KiB" > $LOG_PATH/ps-$LOG_NAME-$(date +%F).log
    fi
        echo "$i;$time_with_ms;$cpu_percentage;$mem_percentage;$mem_kibibytes" >> $LOG_PATH/ps-$LOG_NAME-$(date +%F).log

    if [ -f "$FILE" ]; then 
        echo "Build Completed" >> $LOG_PATH/ps-$LOG_NAME-$(date +%F).log
        exit 0
    fi
done




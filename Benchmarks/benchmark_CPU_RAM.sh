#!/bin/bash

# Input values
while getopts n:a: flag
do
    case "${flag}" in
        a) APP_NAME=${OPTARG};;
        n) LOG_NAME=${OPTARG};;
    esac
done

i=0
while true
do  
    ((i++))
    time_with_ms=$(date +"%T.%3N")
    cpu=$(top -bn1 | awk '/^%Cpu/ {printf "%d%s",$2,"%"}')
    mem=$(free | awk '/^Mem/ {printf "%d%s",$3/$2*100,"%"}')
    app=( $(ps -e -o pcpu,pmem,args --sort=pcpu | cut -d" " -f1-5 | tail | grep $APP_NAME) )
    app_cpu=${app[0]}
    app_ram=${app[1]}
    if [ $i == 1 ]; then
        echo "ID;Time;CPU %;MEM %; APP_CPU %; APP_RAM %; APP_NAME" > ps-$LOG_NAME.log
    fi
        echo "$i;$time_with_ms;$cpu;$mem;$app_cpu;$app_ram;${app[2]}" >> ps-$LOG_NAME.log
    # if [  ] 
    # Add exit check out for script
done




#!/bin/bash

# Input values
while getopts n:l: flag
do
    case "${flag}" in
        n) LOG_NAME=${OPTARG};;
        l) LOG_PATH=${OPTARG};;
    esac
done

INTERVAL="1" # 1s
net_interface='enp0s25'
FILE=/tmp/exit.txt

i=0
while true
do  
    ((i++))
    time_with_ms=$(date +"%T.%3N")

    R1=`cat /sys/class/net/$net_interface/statistics/rx_bytes`
    T1=`cat /sys/class/net/$net_interface/statistics/tx_bytes`
    sleep $INTERVAL
    R2=`cat /sys/class/net/$net_interface/statistics/rx_bytes`
    T2=`cat /sys/class/net/$net_interface/statistics/tx_bytes`

    TBPS=`expr $T2 - $T1`
    RBPS=`expr $R2 - $R1`
    
    if [ $i == 1 ]; then
        echo "ID; Time; Network interface; TBPS; RBPS" > $LOG_PATH/net-$LOG_NAME-$(date +%F).log
    fi
        echo "$i;$time_with_ms;$net_interface;$TBPS;$RBPS" >> $LOG_PATH/net-$LOG_NAME-$(date +%F).log

    if [ -f "$FILE" ];  then
        echo "Build Completed" >> $LOG_PATH/net-$LOG_NAME-$(date +%F).log
        exit 0
    fi
done


#!/bin/bash

sudo nohup tcpdump -w 0001.pcap -n -i enp0s3 port 22 > /dev/null 2>&1 &
while true
do
    if [ -f finish.log ]; then
        kill $(pidof sudo)
        break
    fi
done
tcpdump -r 0001.pcap > packet-readed.log

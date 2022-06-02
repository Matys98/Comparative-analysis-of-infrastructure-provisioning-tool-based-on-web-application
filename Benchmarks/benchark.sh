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


# CPU & RAM


top -n 1 -p $(ps -a | grep $APP_NAME | awk -F' ' '{print $1}')
while true; do uptime >> uptime_$APP_NAME.log; sleep 1; done

while true 
do 
    (echo "%CPU %MEM ARGS $(date)" && ps -e -o pcpu,pmem,args --sort=pcpu | cut -d" " -f1-5 | tail) >> ps.log; sleep 5; 
done

iteration = 0
while 
do  
    ((iteration++))
    time_with_ms=$(date +"%T.%3N")
    cpu=$(top -bn1 | awk '/^%Cpu/ {printf "%d%s",$2,"%"}')
    mem=$(free | awk '/^Mem/ {printf "%d%s",$3/$2*100,"%"}')

    if [ $iteration == 1 ]
        echo "ID;Time;CPU %;MEM %"
    fi
    echo "ID=$iteration time=$time_with_ms cpu=$cpu  mem=$mem"
done


# Network
tcpdump -i enp0s3
netstat -a | more


if [ $APP_NAME == 'fabric' ]
    start=`date +%s.%N`
    fab $APP_NAME
    end=`date +%s.%N`
elif [ $APP_NAME == 'ansible' ]
    start=`date +%s.%N`
    ansible-playbook -i hosts playbook.yml
    end=`date +%s.%N`
elif [ $APP_NAME == 'cheef' ]
    start=`date +%s.%N`
    fab $APP_NAME
    end=`date +%s.%N`
else
    echo Command not recognized
fi


runtime=$( echo "$end - $start" | bc -l )

AVG_CPU MAX_CPU MIN_CPU


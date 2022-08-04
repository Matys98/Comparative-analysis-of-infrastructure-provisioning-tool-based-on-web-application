#!/bin/bash

# Input values
while getopts d:n: flag
do
    case "${flag}" in
        d) DEPLOYMENT=${OPTARG};;
        n) SAMPLE_NUMBER=${OPTARG};;
    esac
done

APP_NAME="static"

LOG_PATH=/home/matys/data_for_master_degree/bash/$APP_NAME

NEW_LOG_PATH=$LOG_PATH/$DEPLOYMENT/$SAMPLE_NUMBER

mkdir -p $NEW_LOG_PATH

if [ $DEPLOYMENT = "single" ]; then
# Deploy to Instance1 (Frontend)
    ./benchmark/benchmark.sh -a $APP_NAME -t bash -p $NEW_LOG_PATH && start_date=`date +"%T.%3N"` && start=`date +%s.%N` && ./staticwebapp.sh && stop=`date +%s.%N` && ./benchmark/finished.sh 
    runtime_s=$( echo "$stop - $start" | bc -l )
    runtime_m=$( echo "$runtime_s / 60" | bc -l )
    echo "Deploy statrted at $start_date | In seconds: $runtime_s | In minutes: $runtime_m" > $NEW_LOG_PATH/deploy_time.txt
fi

if [ $DEPLOYMENT = "multi" ]; then
    # Deploy to All instances (Frontend)
    ./benchmark/benchmark.sh -a $APP_NAME -t bash -p $NEW_LOG_PATH && start_date=`date +"%T.%3N"` && start=`date +%s.%N` && ./multi_staticwebapp.sh && stop=`date +%s.%N` && ./benchmark/finished.sh
    runtime_s=$( echo "$stop - $start" | bc -l )
    runtime_m=$( echo "$runtime_s / 60" | bc -l )
    echo "Deploy statrted at $start_date | In seconds: $runtime_s | In minutes: $runtime_m" > $NEW_LOG_PATH/deploy_time.txt
fi

if [ $DEPLOYMENT = "test" ]; then
    # Deploy test
    ./benchmark/benchmark.sh -a $APP_NAME -t bash -p $NEW_LOG_PATH && start_date=`date +"%T.%3N"` && start=`date +%s.%N` && sleep 5 && stop=`date +%s.%N` && ./benchmark/finished.sh
    runtime_s=$( echo "$stop - $start" | bc -l )
    runtime_m=$( echo "$runtime_s / 60" | bc -l )
    echo "Deploy statrted at $start_date | In seconds: $runtime_s | In minutes: $runtime_m" > $NEW_LOG_PATH/deploy_time.txt
fi
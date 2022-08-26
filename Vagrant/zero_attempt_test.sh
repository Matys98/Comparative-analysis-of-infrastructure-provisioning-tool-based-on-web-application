#!/bin/bash

# Input values
while getopts t:a:d: flag; do
    case "${flag}" in
    t) TOOL=${OPTARG} ;;
    a) APP=${OPTARG} ;;
    d) DEPLOYMENT=${OPTARG} ;;
    esac
done

# DEPLOYMENT="multi"
if [ $TOOL = "ansible" ]; then
    CD_PATH=../Ansible
fi

if [ $TOOL = "fabric" ]; then
    if [ $APP = "static" ]; then CD_PATH=../Fabric/static; fi
    if [ $APP = "grafana" ]; then CD_PATH=../Fabric/grafana; fi
    if [ $APP = "tiquet" ]; then CD_PATH=../Fabric/tiquet; fi
fi

if [ $TOOL = "bash" ]; then
    if [ $APP = "static" ]; then CD_PATH=../Bash_Scripts/bash_deployment/static; fi
    if [ $APP = "grafana" ]; then CD_PATH=../Bash_Scripts/bash_deployment/grafana; fi
    if [ $APP = "tiquet" ]; then CD_PATH=../Bash_Scripts/bash_deployment/tiquet; fi
fi

vagrant destroy -f

if [ $DEPLOYMENT = "single" ]; then
    vagrant up Instance1
    vagrant snapshot save Instance1 initial-setup1
fi

if [ $DEPLOYMENT = "multi" ]; then
    vagrant up
    vagrant snapshot save Instance1 initial-setup1
    vagrant snapshot save Instance2 initial-setup2
    vagrant snapshot save Instance3 initial-setup3
fi

if [ $DEPLOYMENT = "split" ] && [ $APP = "grafana" ]; then
    vagrant up Instance1
    vagrant up Instance2
    vagrant snapshot save Instance1 initial-setup1
    vagrant snapshot save Instance2 initial-setup2
fi

if [ $DEPLOYMENT = "split" ] && [ $APP = "tiquet" ]; then
    vagrant up
    vagrant snapshot save Instance1 initial-setup1
    vagrant snapshot save Instance2 initial-setup2
    vagrant snapshot save Instance3 initial-setup3
fi

./reset_ssh.sh

CURRENT_PATH=$(pwd)

./reset_ssh.sh
cd $CD_PATH

if [ $APP = "static" ]; then ./benchmark_staticwebapp.sh -d $DEPLOYMENT -n 0; fi
if [ $APP = "grafana" ]; then ./benchmark_grafana.sh -d $DEPLOYMENT -n 0; fi
if [ $APP = "tiquet" ]; then ./benchmark_tiquet.sh -d $DEPLOYMENT -n 0; fi

echo "----------------------"
echo "------- READY --------"
echo "----------------------"

read  -n 1 -p "Wait until check is finished:" mainmenuinput

cd $CURRENT_PATH

if [ $DEPLOYMENT = "single" ]; then
    vagrant snapshot restore Instance1 initial-setup1
fi

if [ $DEPLOYMENT = "multi" ]; then
    vagrant snapshot restore Instance1 initial-setup1
    vagrant snapshot restore Instance2 initial-setup2
    vagrant snapshot restore Instance3 initial-setup3
fi

if [ $DEPLOYMENT = "split" ] && [ $APP = "grafana" ]; then
    vagrant snapshot restore Instance1 initial-setup1
    vagrant snapshot restore Instance2 initial-setup2
fi

if [ $DEPLOYMENT = "split" ] && [ $APP = "tiquet" ]; then
    vagrant snapshot restore Instance1 initial-setup1
    vagrant snapshot restore Instance2 initial-setup2
    vagrant snapshot restore Instance3 initial-setup3
fi

vagrant destroy -f
echo "----------------------"
echo "-------- DONE --------"
echo "----------------------"

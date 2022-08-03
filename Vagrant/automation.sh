#!/bin/bash

# Input values
while getopts t:a: flag
do
    case "${flag}" in
        t) TOOL=${OPTARG};;
        a) APP=${OPTARG};;
    esac
done

DEPLOYMENT="multi"
if [ $TOOL = "ansible" ]; then
  CD_PATH=Ansible
fi

if [ $TOOL = "fabric" ]; then
  if [ $APP = "static" ]; then; CD_PATH=Fabric/static; fi
  if [ $APP = "grafana" ]; then; CD_PATH=Fabric/grafana; fi
  if [ $APP = "tiquet" ]; then; CD_PATH=Fabric/tiquet; fi
fi

if [ $TOOL = "bash" ]; then
  if [ $APP = "static" ]; then; CD_PATH=Bash_Scripts/bash_deployment/static; fi
  if [ $APP = "grafana" ]; then; CD_PATH=Bash_Scripts/bash_deployment/grafana; fi
  if [ $APP = "tiquet" ]; then; CD_PATH=Bash_Scripts/bash_deployment/tiquet; fi
fi


CURRENT_PATH=$(pwd)

for i in {1..10}
do
   echo "Run $i times"
   vagrant destroy -f
   vagrant up
   ./reset_ssh.sh
   cd $PATH
   
   if [ $APP = "static" ]; then; ./benchmark_staticwebapp.sh; fi
   if [ $APP = "grafana" ]; then; ./benchmark_grafana.sh; fi
   if [ $APP = "tiquet" ]; then; ./benchmark_tiquet.sh; fi
   
done

#!/bin/bash
echo "Iniciando el switch..." > /root/start_s1.log
sleep 3
cd /behavioral-model/targets/simple_switch_grpc
simple_switch_grpc --no-p4 -i 1@eth1 -i 2@eth2 --thrift-port 9090 --device-id 1
echo "Switch iniciado" >> /root/start_s1.log
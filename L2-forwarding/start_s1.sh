#!/bin/bash
echo "Iniciando el switch..."
sleep 3
#Path to behavioral-model (simple_switch_grpc) y logs en /root
export PATH=$PATH:/behavioral-model/targets/simple_switch_grpc/
stdbuf -oL simple_switch_grpc --no-p4 -i 1@eth1 -i 2@eth2 --thrift-port 9090 --device-id 1 --log-console trace 2>&1 | tee s1-bmv2.log

#simple_switch_grpc --no-p4 -i 1@eth1 -i 2@eth2 --thrift-port 9090 --device-id 1 --log-console trace 2>&1 | tee s1-bmv2.log 
echo "Switch iniciado"
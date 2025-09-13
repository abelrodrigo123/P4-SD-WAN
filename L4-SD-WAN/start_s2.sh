#!/bin/bash
echo "Finalizando proceso del switch sin logs"
kill -9 $(pgrep simple_sw)

echo "Iniciando el switch con logs..."
sleep 3
#Path to behavioral-model (simple_switch_grpc) y logs en /root
export PATH=$PATH:/behavioral-model/targets/simple_switch_grpc/
#simple_switch_grpc --no-p4 -i 1@eth1 -i 2@eth2 -i 4@eth4 --thrift-port 9091 --device-id 2 --log-console -L trace 2>&1 | tee s2-bmv2.log 
stdbuf -oL simple_switch_grpc --no-p4 -i 1@eth1 -i 2@eth2 -i 4@eth4 --thrift-port 9091 --device-id 2 --log-console trace 2>&1 | tee s2-bmv2.log

echo "Switch iniciado"

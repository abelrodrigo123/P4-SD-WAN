#!/bin/bash
# init_switch.sh
SWITCH_BINARY="/behavioral-model/targets/simple_switch_grpc/simple_switch_grpc"
JSON_CONFIG="/behavioral-model/targets/simple_switch_grpc/my_program.json"

echo "Iniciando el switch BMv2..."
$SWITCH_BINARY \
    -i 1@eth1 -i 2@eth2 -i 3@eth3 \
    --log-console \
    --thrift-port 9090 \
    --device-id 1 \
    $JSON_CONFIG

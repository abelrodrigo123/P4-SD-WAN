#!/bin/bash
# populate_tables.sh

CLI_TOOL="/behavioral-model/tools/runtime_CLI.py"
THRIFT_PORT=9090

echo "Conectándose al switch para poblar las tablas..."
$CLI_TOOL --thrift-port $THRIFT_PORT << EOF
table_add MyIngress.ipv4_lpm MyIngress.ipv4_forward 10.0.0.1/32 => 02:fd:00:00:00:01 1
table_add MyIngress.ipv4_lpm MyIngress.ipv4_forward 10.1.0.0/24 => 02:fd:00:00:03:02 2
table_add MyIngress.ipv4_lpm MyIngress.ipv4_forward 172.17.2.0/24 => 02:fd:00:00:02:03 3
table_set_default MyIngress.ipv4_lpm MyIngress.drop
EOF

echo "Tablas pobladas correctamente."

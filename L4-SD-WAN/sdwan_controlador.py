#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from p4utils.utils.sswitch_p4runtime_API import SimpleSwitchP4RuntimeAPI

# --------- Rutas a artefactos P4 ---------
JSON = 'sdwan.json'
P4RT = 'sdwan.p4rt.txt'

# --------- Conexión gRPC ---------
S1 = dict(device_id=1, grpc_ip='172.17.2.1', grpc_port=9559,
          json_path=JSON, p4rt_path=P4RT)
S2 = dict(device_id=2, grpc_ip='172.17.2.2', grpc_port=9559,
          json_path=JSON, p4rt_path=P4RT)

# --------- MACs y puertos físicos ---------
MAC_H1 = '02:fd:00:00:00:01'
MAC_H2 = '02:fd:00:00:01:01'

# En s1: eth1->h1, eth2->enlace L2 normal a s2, eth4->WAN/MPLS hacia s2
# En s2: eth1->h2, eth2->enlace L2 normal a s1, eth4->WAN/MPLS hacia s1
S1_ETH1, S1_ETH2, S1_ETH4 = '1', '2', '4'
S2_ETH1, S2_ETH2, S2_ETH4 = '1', '2', '4'

# Puerto prioritario (TCP/UDP)
PRIO_L4 = '6000'   # iperf -p 6000

def add(api, table, action, match, params):
    print(f"add {api.device_id}: {table} {match} -> {action} {params}")
    api.table_add(table, action, match, params)

def program_switches():
    # ========== S1 ==========
    s1 = SimpleSwitchP4RuntimeAPI(**S1)

    # L2 normal (tabla dmac): h2 por eth2, h1 por eth1
    add(s1, 'dmac', 'forward', [MAC_H2], [S1_ETH2])
    add(s1, 'dmac', 'forward', [MAC_H1], [S1_ETH1])

    # Prioridad SIN BUCLES:
    # Tráfico del cliente -> servidor (dst port 6000) sale por WAN (eth4)
    add(s1, 'prio_udp_dst', 'prio_forward', [PRIO_L4], [S1_ETH4])
    add(s1, 'prio_tcp_dst', 'prio_forward', [PRIO_L4], [S1_ETH4])
    # Respuestas del servidor (src port 6000) hacia el host local por eth1
    add(s1, 'prio_udp_src', 'prio_forward', [PRIO_L4], [S1_ETH1])
    add(s1, 'prio_tcp_src', 'prio_forward', [PRIO_L4], [S1_ETH1])

    # ========== S2 ==========
    s2 = SimpleSwitchP4RuntimeAPI(**S2)

    # L2 normal (tabla dmac): h1 por eth2, h2 por eth1
    add(s2, 'dmac', 'forward', [MAC_H1], [S2_ETH2])
    add(s2, 'dmac', 'forward', [MAC_H2], [S2_ETH1])

    # Prioridad espejo en s2 (sin bucles):
    # Llegadas al servidor (dst 6000) -> directo a h2 (eth1)
    add(s2, 'prio_udp_dst', 'prio_forward', [PRIO_L4], [S2_ETH1])
    add(s2, 'prio_tcp_dst', 'prio_forward', [PRIO_L4], [S2_ETH1])
    # Respuestas del servidor (src 6000) -> WAN hacia s1 (eth4)
    add(s2, 'prio_udp_src', 'prio_forward', [PRIO_L4], [S2_ETH4])
    add(s2, 'prio_tcp_src', 'prio_forward', [PRIO_L4], [S2_ETH4])

    print("\n[done] Reglas instaladas (L2 + prioridad TCP/UDP puerto 6000 sin bucles).")

if __name__ == '__main__':
    program_switches()

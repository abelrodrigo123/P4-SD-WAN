from p4utils.utils.helper import load_topo
from p4utils.utils.sswitch_p4runtime_API import SimpleSwitchP4RuntimeAPI


# ----- Switch S1 -----
s1 = SimpleSwitchP4RuntimeAPI(
    device_id=1,
    grpc_ip='172.17.2.1',
    grpc_port=9559,
    json_path='my_program.json',
    p4rt_path='my_program.p4rt.txt'
)


# Poblado de tabla dmac (MAC destino → puerto)
s1.table_add('dmac', 'forward', ['02:fd:00:00:00:01'], ['1'])  # h1 (conectado a eth1)
s1.table_add('dmac', 'forward', ['02:fd:00:00:01:01'], ['2'])  # h2 vía s2

# Agregamos manejo de broadcast (ff:ff:ff:ff:ff:ff)
s1.table_add('dmac', 'broadcast', ['ff:ff:ff:ff:ff:ff'], [])  # difundir

# Poblado de tabla arp_table para responder ARP requests
s1.table_add('arp_table', 'send_arp_reply', ['10.0.0.1'], ['02:fd:00:00:00:01', '10.0.0.1'])  # h1
s1.table_add('arp_table', 'send_arp_reply', ['10.0.0.2'], ['02:fd:00:00:01:01', '10.0.0.2'])  # h2


# Multicast (puertos 1 y 2)
# grp = s1.mc_mgrp_create(1)
# node = s1.mc_node_create(0, [1, 2])
# s1.mc_node_associate(1, node)
# Configuración de multicast para broadcast
#s1.table_add('dmac', 'multicast', ['ff:ff:ff:ff:ff:ff'], [grp])  # difundir a todos los puertos
# Configuración de multicast para ARP requests
#s1.table_add('arp_table', 'multicast_arp_request', ['10.0.0.255'], [grp])  # difundir ARP requests a todos los puertos



# ----- Switch S2 -----
s2 = SimpleSwitchP4RuntimeAPI(
    device_id=2,
    grpc_ip='172.17.2.2',
    grpc_port=9559,
    json_path='my_program.json',
    p4rt_path='my_program.p4rt.txt'
)       

# Tabla de forwarding
s2.table_add('dmac', 'forward', ['02:fd:00:00:01:01'], ['1'])  # h2
s2.table_add('dmac', 'forward', ['02:fd:00:00:00:01'], ['2'])  # h1 vía s1

# Broadcast en s2 también
s2.table_add('dmac', 'broadcast', ['ff:ff:ff:ff:ff:ff'], [])

# ARP table entries (opcional según topología)
s2.table_add('arp_table', 'send_arp_reply', ['10.0.0.2'], ['02:fd:00:00:01:01', '10.0.0.2'])
s2.table_add('arp_table', 'send_arp_reply', ['10.0.0.1'], ['02:fd:00:00:00:01', '10.0.0.1'])

# Multicast (puertos 1 y 2)
# grp = s2.mc_mgrp_create(1)
# node = s2.mc_node_create(0, [1, 2])
# s2.mc_node_associate(1, node)   

# Configuración de multicast para broadcast
#s2.table_add('dmac', 'multicast', ['ff:ff:ff:ff:ff:ff'], [grp])  # difundir a todos los puertos
# Configuración de multicast para ARP requests
#s2.table_add('arp_table', 'multicast_arp_request', ['10.   0.0.255'], [grp])  # difundir ARP requests a todos los puertos
# ----- Controlador -----




print("✅ Controlador configurado correctamente.")






#### ANTERIOR 

# ##### S1 ##### 
# controller = SimpleSwitchP4RuntimeAPI(device_id=1, grpc_port=9559, grpc_ip='172.17.2.1',
#                                       p4rt_path='my_program.p4rt.txt',
#                                       json_path='my_program.json')

# #controller.table_clear('dmac')

# controller.table_add('dmac', 'forward', ['02:fd:00:00:00:01'], ['1']) #h1-eth1
# controller.table_add('dmac', 'forward', ['02:fd:00:00:01:01'], ['2']) #h2-eth1 via s2


# #### SW 2 ######

# controller = SimpleSwitchP4RuntimeAPI(device_id=2, grpc_port=9559, grpc_ip='172.17.2.2',
#                                       p4rt_path='my_program.p4rt.txt',
#                                       json_path='my_program.json')

# #controller.table_clear('dmac')
# controller.table_set_default('dmac','drop')
# controller.table_add('dmac', 'forward', ['02:fd:00:00:01:01'],['1']) #h2-eth1
# controller.table_add('dmac', 'forward', ['02:fd:00:00:00:01'],['2']) #h1-eth1 via s1
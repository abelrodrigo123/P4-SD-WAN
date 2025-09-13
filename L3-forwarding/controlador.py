from p4utils.utils.sswitch_p4runtime_API import SimpleSwitchP4RuntimeAPI

##### S1 ##### 
controller = SimpleSwitchP4RuntimeAPI(device_id=1, grpc_port=9559, grpc_ip='172.17.2.1',
                                      p4rt_path='my_program.p4rt.txt',
                                      json_path='my_program.json')

#controller.table_clear('ipv4_lpm')
controller.table_set_default('ipv4_lpm','drop')
controller.table_add('ipv4_lpm', 'ipv4_forward',['10.0.0.1/32'], ['02:fd:00:00:00:01','1'])
controller.table_add('ipv4_lpm', 'ipv4_forward',['10.1.0.0/24'], ['02:fd:00:00:03:02','2'])
controller.table_add('ipv4_lpm', 'ipv4_forward',['172.17.2.0/24'], ['02:fd:00:00:02:03','3'])

# VERISION CLI
# table_add MyIngress.ipv4_lpm MyIngress.ipv4_forward 10.0.0.1/32 => 02:fd:00:00:00:01 1
# table_add MyIngress.ipv4_lpm MyIngress.ipv4_forward 10.1.0.0/24 => 02:fd:00:00:03:02 2
# table_add MyIngress.ipv4_lpm MyIngress.ipv4_forward 172.17.2.0/24 => 02:fd:00:00:02:03 3

#### SW 2 ######

controller = SimpleSwitchP4RuntimeAPI(device_id=2, grpc_port=9559, grpc_ip='172.17.2.2',
                                      p4rt_path='my_program.p4rt.txt',
                                      json_path='my_program.json')

#controller.table_clear('ipv4_lpm')
controller.table_set_default('ipv4_lpm','drop')
controller.table_add('ipv4_lpm', 'ipv4_forward',['10.1.0.2/32'], ['02:fd:00:00:01:01','1'])
controller.table_add('ipv4_lpm', 'ipv4_forward',['10.0.0.0/24'], ['02:fd:00:00:02:02','2'])
controller.table_add('ipv4_lpm', 'ipv4_forward',['172.17.2.0/24'], ['02:fd:00:00:03:03','3'])

# GPRC_CLI_RUNTIME
# table_add MyIngress.ipv4_lpm MyIngress.ipv4_forward 10.1.0.2/32 => 02:fd:00:00:01:01 1
# table_add MyIngress.ipv4_lpm MyIngress.ipv4_forward 10.0.0.0/24 => 02:fd:00:00:02:02 2
# table_add MyIngress.ipv4_lpm MyIngress.ipv4_forward 172.17.2.0/24 => 02:fd:00:00:03:03 3
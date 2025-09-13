from p4utils.utils.helper import load_topo
from p4utils.utils.sswitch_p4runtime_API import SimpleSwitchP4RuntimeAPI

##### S1 ##### 
controller = SimpleSwitchP4RuntimeAPI(device_id=1, grpc_port=9559, grpc_ip='172.17.2.1',
                                      p4rt_path='my_program.p4rt.txt',
                                      json_path='my_program.json')

#controller.table_clear('dmac')

# controller.table_add('dmac', 'forward', ['02:fd:00:00:00:01'], ['1']) #h1-eth1
# controller.table_add('dmac', 'forward', ['02:fd:00:00:01:01'], ['2']) #h2-eth1 via s2


#### SW 2 ######

controller = SimpleSwitchP4RuntimeAPI(device_id=2, grpc_port=9559, grpc_ip='172.17.2.2',
                                      p4rt_path='my_program.p4rt.txt',
                                      json_path='my_program.json')

#controller.table_clear('dmac')
# controller.table_set_default('dmac','drop')
# controller.table_add('dmac', 'forward', ['02:fd:00:00:01:01'],['1']) #h2-eth1
# controller.table_add('dmac', 'forward', ['02:fd:00:00:00:01'],['2']) #h1-eth1 via s1

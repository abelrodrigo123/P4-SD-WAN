#!/usr/bin/env python3
from p4utils.mininetlib.network_API import NetworkAPI

net = NetworkAPI()

net.setLogLevel('info')
net.enableCli()

net.setCompiler(p4rt=True) #en caso de ejecutar 'net.setP4SourceAll' se compilaría el programa P4 directamente
#net.execScript('python3 controlador.py', reboot=True)

net.addP4RuntimeSwitch('s1')
net.addP4RuntimeSwitch('s2')
net.addP4RuntimeSwitch('s3')
#net.setP4SourceAll('forwarding.p4')

net.addHost('h1')
net.addHost('h2')
net.addHost('h3')
net.addHost('h4')

net.addLink('h1', 's1')
net.addLink('h2', 's2')
net.addLink('s1', 's2')
net.addLink('h3', 's3')
net.addLink('h4', 's3')
net.addLink('s1', 's3')

net.mixed()

net.enablePcapDumpAll()
net.enableLogAll()

net.startNetwork()

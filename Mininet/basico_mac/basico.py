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

##Crear Sw y cambiar su ID de forma manual, de lo contratrio es correlativo el orden.
net.addP4RuntimeSwitch('s21', device_id=21)

#net.setP4SourceAll('forwarding.p4')

net.addHost('h1')
net.addHost('h2')
net.addHost('h3')
net.addHost('h4')
net.addHost('h21')
net.addHost('h22')

net.addLink('h1', 's1')
net.addLink('h2', 's2')
net.addLink('s1', 's2')
net.addLink('h3', 's3')
net.addLink('h4', 's3')
net.addLink('s1', 's3')
net.addLink('h21','s21')
net.addLink('s3','s21')
net.addLink('h22','s21')

#estrategia de asignacion de direcciones y MAC
net.mixed()

# CAMBIAR DIRECCIONES MAC DE NODOS Y ENLACES

# Asignar dirección MAC a h21 después de crearlo
#MAC DE H21 ('00:00:00:00:XX:XX)
net.setIntfMac('h21', 's21', '00:00:00:00:21:01')
# MAC en s21 conectada a h21 
net.setIntfMac('s21', 'h21', '00:00:0a:00:21:01')
# MAC en s21 para el enlace a s3
net.setIntfMac('s21', 's3', '00:00:0a:03:21:03') 

##H22
net.setIntfMac('h22','s21','00:00:00:00:21:02')
##Enlace entre h22 y s21 (00:00:0a:xx:xx:xx)
net.setIntfMac('s21','h22','00:00:0a:00:21:02')



net.enablePcapDumpAll()
net.enableLogAll()

net.startNetwork()

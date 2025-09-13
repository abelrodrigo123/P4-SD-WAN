# ESCENARIO VNX CON SWITCH P4 BMv2

## INDICE 
- [Instrucciones ](#instrucciones)
  - [Instrucciones ](#ejecutar-escenario)
- [Conexion mediante GPRC](#Conexion-GRPC)
- [Compilar Programa P4 para L2](#compilar-p4-l2)
- [Conexion mediante CLI ](#USANDO-CLI)
- [Pruebas de conexion y depuración ](#pruebas)



## TOPOLOGIA

![Diseño](DiseñoL2.drawio.png)

## INSTRUCCIONES:

### Ejecutar escenario.

```python
sudo vnx -f p4_sdwan.xml  -v --create 
```

al finalizar para limpiar escenario.

```python
sudo vnx -f p4_sdwan.xml  -v --destroy 

```
O utilizar 

```python
sudo vnx --clean-host

```



#### Ver Topologia

```python
sudo vnx -f p4_sdwan.xml -v --show-map 
```

![Topologia](Propuesta1-SD-WAN1.drawio.png)




## Compilar 

```python
sudo p4c --target bmv2 --arch v1model --p4runtime-files sdwan.p4info.txt sdwan.p4
```







EN CONSOLA 2 de S1, abrir con el comando desde el host:

```python
ibdn@ibdn-VirtualBox:~/TFG_P4-main/TFG_P4-main$ sudo vnx -f p4_sdwan.xml  -v -console -M s1
```

Ver puede observar el Sw BMv2 con el PID 313 que tiene 2 puertos uno de grpc y el thrift 


```python
root@s1:~# sudo lsof -i
COMMAND   PID            USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
systemd-r  95 systemd-resolve   13u  IPv4 237875      0t0  UDP localhost:domain 
systemd-r  95 systemd-resolve   14u  IPv4 237876      0t0  TCP localhost:domain (LISTEN)
sshd      190            root    3u  IPv4 239177      0t0  TCP *:ssh (LISTEN)
sshd      190            root    4u  IPv6 239179      0t0  TCP *:ssh (LISTEN)
simple_sw 313            root   13u  IPv6 248243      0t0  TCP *:9559 (LISTEN)
simple_sw 313            root   20u  IPv4 248252      0t0  TCP *:9090 (LISTEN)
root@s1:~# 
```

Verifica el puerto gRPC
Después de iniciar el switch, verifica que el puerto gRPC está activo:

```python
netstat -tuln | grep 9559
```

```python

ip link show
```
Verificaciones 





###################################

## Compilar codigo 

## Compilar 

```python
sudo p4c --target bmv2 --arch v1model --p4runtime-files sdwan.p4info.txt sdwan.p4
```







## CREAR ESCENARIO 
```python
sudo vnx -f p4_sdwan.xml --create

```






## EJECUTAR CODIGO

```python
python3 sdwan_controlador.py \
  --p4info sdwan.p4info.txt \
  --json   sdwan.json \
  --s1-ip 172.17.2.1 --s2-ip 172.17.2.2 \
  --s1-grpc 9559     --s2-grpc 9559 \
  --prio-port 6000 --proto tcp
```


iperf -s -i 1 -p 6000



iperf -c 10.1.0.2 -i 1 -p 6000



sudo p4c --target bmv2 --arch v1model \
    --p4runtime-files sdwan.p4info.txt \
    sdwan.p4





sudo python3 sdwan_controlador.py \
  --p4info sdwan.p4info.txt --json sdwan.json \
  --s1-ip 172.17.2.1 --s2-ip 172.17.2.2 \
  --s1-grpc 9559     --s2-grpc 9559 \
  --prio-port 6000 --proto both --clear-prio



sudo python3 sdwan_controlador.py \
  --p4info sdwan.p4info.txt --json sdwan.json \
  --s1-ip 172.17.2.1 --s2-ip 172.17.2.2 \
  --s1-grpc 9559     --s2-grpc 9559 \
  --prio-port 6000 --proto tcp --clear-prio


  SOLUCION DE ERRORES

### S1
simple_switch_CLI --thrift-port 9090
> table_dump IngressImpl.prio_tcp_dst
> table_dump IngressImpl.prio_tcp_src



### S2
simple_switch_CLI --thrift-port 9091
> table_dump IngressImpl.prio_tcp_dst
> table_dump IngressImpl.prio_tcp_src




## Abrir consolas adicionales en s1 y s2

```python
sudo vnx -f p4_sdwan.xml -v -console -M s1
sudo vnx -f p4_sdwan.xml -v -console -M s2
```




## Encontrar los contenedores en el host para copiar logs

Los archivos de los contenedores LXC se almacenan típicamente en la ruta /var/lib/lxc/. Dentro de esta carpeta, debe haber un directorio con el nombre de tu contenedor.



```python
sudo ls /var/lib/lxc/

```
El archivo se copiar a la raiz de la ruta donde se ejecuta el comando.

Copia el archivo s1-bmv2.log:


```python
sudo cp /var/lib/lxc/s1/rootfs/root/s1-bmv2.log .

```
Copia el archivo de s2:

```python
sudo cp /var/lib/lxc/s2/rootfs/root/s2-bmv2.log .

```

EN H1 Y H2

```python
tcpdump -i eth1 -vv

```












### OTROS COMANDOS

sudo vnx -f p4_sdwan.xml -v --create



sudo p4c --target bmv2 --arch v1model --p4runtime-files sdwan.p4info.txt sdwan.p4



sudo python3 sdwan_controlador.py   --p4info sdwan.p4info.txt --json sdwan.json   --s1-ip 172.17.2.1 --s2-ip 172.17.2.2   --s1-grpc 9559     --s2-grpc 9559   --prio-port 6000 --proto both



sudo vnx -f p4_sdwan.xml -v -console -M s1
sudo vnx -f p4_sdwan.xml -v -console -M s2






en el h2 (voip-gw)
iperf -s -u -i 1 -p 6000


En el h1 (emisor)
.--------------------------------
iperf -c 10.1.0.2 -p 6000 -u -b 2M -l 1200 -t 3





en el h2 (voip-gw)
iperf -s -i 1 -p 6000


En el h1 (emisor)
.--------------------------------
iperf -c 10.1.0.2 -p 6000 -b 2M -l 1200 -t 3








en el h2 (voip-gw)
iperf -s -u -i 1 -p 5000


En el h1 (emisor)
.--------------------------------
iperf -c 10.1.0.2 -p 5000 -b 2M -l 1200 -t 2


sudo p4c --target bmv2 --arch v1model \
    --p4runtime-files sdwan.p4info.txt \
    sdwan.p4



TCP
sudo python3 sdwan_controlador.py \
  --p4info sdwan.p4info.txt --json sdwan.json \
  --s1-ip 172.17.2.1 --s2-ip 172.17.2.2 \
  --s1-grpc 9559     --s2-grpc 9559 \
  --prio-port 6000 --proto tcp --clear-prio



UPD
sudo python3 sdwan_controlador.py \
  --p4info sdwan.p4info.txt --json sdwan.json \
  --s1-ip 172.17.2.1 --s2-ip 172.17.2.2 \
  --s1-grpc 9559     --s2-grpc 9559 \
  --prio-port 6000 --proto udp --clear-prio



sudo python3 sdwan_controlador.py \
  --p4info sdwan.p4info.txt --json sdwan.json \
  --s1-ip 172.17.2.1 --s2-ip 172.17.2.2 \
  --s1-grpc 9559     --s2-grpc 9559 \
  --prio-port 6000 --proto both --clear-prio




*********************************************

sudo python3 3sdwan_controlador.py \
  --p4info sdwan.p4info.txt --json sdwan.json \
  --s1-ip 172.17.2.1 --s2-ip 172.17.2.2 \
  --s1-grpc 9559     --s2-grpc 9559 \
  --prio-port 6000 --proto both --clear-prio







tail -f s1-bmv2.log
tail -f s2-bmv2.log






SOLUCION DE ERRORES


S1
simple_switch_CLI --thrift-port 9090
  table_dump IngressImpl.ipv4_lpm
  table_dump IngressImpl.prio_udp_dst
  table_dump IngressImpl.prio_udp_src
  table_dump IngressImpl.prio_tcp_dst
  table_dump IngressImpl.prio_tcp_src


S2
simple_switch_CLI --thrift-port 9091
  table_dump IngressImpl.ipv4_lpm
  table_dump IngressImpl.prio_udp_dst
  table_dump IngressImpl.prio_udp_src
  table_dump IngressImpl.prio_tcp_dst
  table_dump IngressImpl.prio_tcp_src



ADICIONAL

show_tables
show_actions





LIMPIAR


S1

table_clear IngressImpl.prio_udp_dst
table_clear IngressImpl.prio_udp_src
table_clear IngressImpl.prio_tcp_dst
table_clear IngressImpl.prio_tcp_src



table_add IngressImpl.prio_udp_dst IngressImpl.set_nexthop_prio 1 6000 => 02:fd:00:00:03:04 02:fd:00:00:02:04 4
table_add IngressImpl.prio_tcp_dst IngressImpl.set_nexthop_prio 1 6000 => 02:fd:00:00:03:04 02:fd:00:00:02:04 4
table_add IngressImpl.prio_udp_src IngressImpl.set_nexthop_prio 4 6000 => 02:fd:00:00:00:01 02:fd:00:00:02:01 1
table_add IngressImpl.prio_tcp_src IngressImpl.set_nexthop_prio 4 6000 => 02:fd:00:00:00:01 02:fd:00:00:02:01 1

*******************

EN S2
table_clear IngressImpl.prio_udp_dst
table_clear IngressImpl.prio_udp_src
table_clear IngressImpl.prio_tcp_dst
table_clear IngressImpl.prio_tcp_src


table_add IngressImpl.prio_udp_dst IngressImpl.set_nexthop_prio 4 6000 => 02:fd:00:00:01:01 02:fd:00:00:03:01 1
table_add IngressImpl.prio_tcp_dst IngressImpl.set_nexthop_prio 4 6000 => 02:fd:00:00:01:01 02:fd:00:00:03:01 1
table_add IngressImpl.prio_udp_src IngressImpl.set_nexthop_prio 1 6000 => 02:fd:00:00:02:04 02:fd:00:00:03:04 4
table_add IngressImpl.prio_tcp_src IngressImpl.set_nexthop_prio 1 6000 => 02:fd:00:00:02:04 02:fd:00:00:03:04 4



******


VERIFICAR TABLAS


table_dump IngressImpl.prio_udp_dst
table_dump IngressImpl.prio_udp_src
table_dump IngressImpl.prio_tcp_dst
table_dump IngressImpl.prio_tcp_src


****************



EN H2
iperf -s -p 6000          # TCP
# en otra prueba
iperf -s -p 6000 -u       # UDP


EN H1

iperf -c 10.1.0.2 -p 6000           # TCP: debe conectar y medir
iperf -c 10.1.0.2 -p 6000 -u -t 3   # UDP: ya debe recibir ACKs y reporte en h2


*************+



Si pruebas UDP por 6000, lanza el controlador con --proto udp o --proto both. Si no, UDP seguirá por LPM (eth2), como debe.

python3 sdwan_controlador.py \
  --p4info sdwan.p4info.txt --json sdwan.json \
  --s1-ip 172.17.2.1 --s2-ip 172.17.2.2 \
  --s1-grpc 9559     --s2-grpc 9559 \
  --prio-port 6000 --proto both --clear-prio


1) ¿--proto both qué hace?

En el sdwan_controlador.py que te pasé, --proto both instala las 4 tablas de prioridad:

prio_tcp_dst y prio_tcp_src

prio_udp_dst y prio_udp_src

Si ejecutas primero --proto udp y después --proto tcp con --clear-prio, estás borrando las reglas del primero cuando programas el segundo. Para tener los dos activos, usa una sola ejecución con --proto both (o ejecuta 2 veces sin --clear-prio la segunda).





COPIAR LOGS

sudo cp /var/lib/lxc/s1/rootfs/root/s1-bmv2.log .

sudo cp /var/lib/lxc/s2/rootfs/root/s2-bmv2.log .



tcpdump -i eth1 -vv






1) Soluciona el offload en el anfitrión (usaste un nombre inválido)
# Lista sólo el nombre puro de cada veth (sin @ifX)

```python
ip -o link show type veth | awk -F': ' '{print $2}' | cut -d'@' -f1

```
# Desactiva offloads en todas las veth del lab (algunas dirán "Operation not supported"; ignóralo)
for i in $(ip -o link show type veth | awk -F': ' '{print $2}' | cut -d'@' -f1); do
  echo "== $i ==";
  sudo ethtool -K "$i" rx off tx off tso off gso off gro off lro off 2>/dev/null || true
done

# Verifica en algunas (elige varias, p. ej. h1-e1, s1-e4, s2-e4, h2-e1)

```python
sudo ethtool -k h1-e1
sudo ethtool -k s1-e4
sudo ethtool -k s2-e4
sudo ethtool -k h2-e1

```


Abrir consolas para depuracion.

```python
sudo vnx -f p4_sdwan.xml -v -console -M h1
sudo vnx -f p4_sdwan.xml -v -console -M h2
sudo vnx -f p4_sdwan.xml -v -console -M s1
sudo vnx -f p4_sdwan.xml -v -console -M s2
```






## CREACION DEL ESCENARIO P4 SDWAN 

```python
ibdn@ibdn-VirtualBox:~/TFG_P4-main/TFG_P4-main/LXC-VNX-P4-L4-SDWAN$ sudo vnx -f p4_sdwan.xml --create
[sudo] password for ibdn: 
localuser:root being added to access control list

------------------------------------------------------------------------------------------
Virtual Networks over LinuX (VNX) -- http://www.dit.upm.es/vnx - vnx@dit.upm.es
Version: 2.0b.6841 (built on 03/04/2025_17:57)
------------------------------------------------------------------------------------------
  OS=Ubuntu 22.04.5 LTS
  VNX executed as root
  xhost +SI:localuser:root executed 
  CONF file: /etc/vnx.conf
  IPv6 enabled: yes
  TMP dir=/tmp
  VNX dir=/root/.vnx
  INPUT file: p4_sdwan.xml
------------------------------------------------------------------------------------------
Defining virtual machine 'h1' of type 'lxc'...
...OK
Defining virtual machine 'h2' of type 'lxc'...
...OK
Defining virtual machine 's1' of type 'lxc'...
...OK
Defining virtual machine 's2' of type 'lxc'...
...OK
Starting virtual machine 'h1' of type 'lxc'...
...OK
Starting virtual machine 'h2' of type 'lxc'...
...OK
Starting virtual machine 's1' of type 'lxc'...
...OK
Starting virtual machine 's2' of type 'lxc'...
...OK
Calling execute_cmd for vm 's1' with seq 'on_boot'...
...execute_cmd for vm 's1' with seq 'on_boot' returns OK
Calling execute_cmd for vm 's2' with seq 'on_boot'...
...execute_cmd for vm 's2' with seq 'on_boot' returns OK

------------------------------------------------------------------------------------------
 Scenario "P4_SDWAN" started

 VM_NAME     | TYPE                | CONSOLE ACCESS COMMAND
-----------------------------------------------------------------------------------------
 h1          | lxc                 | con0:  'lxc-console -n h1'
             |                     | con1:  'lxc-console -n h1'
-----------------------------------------------------------------------------------------
 h2          | lxc                 | con0:  'lxc-console -n h2'
             |                     | con1:  'lxc-console -n h2'
-----------------------------------------------------------------------------------------
 s1          | lxc                 | con0:  'lxc-console -n s1'
             |                     | con1:  'lxc-console -n s1'
-----------------------------------------------------------------------------------------
 s2          | lxc                 | con0:  'lxc-console -n s2'
             |                     | con1:  'lxc-console -n s2'
-----------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------
Total time elapsed: 14 seconds
------------------------------------------------------------------------------------------

```

## EJECUCCION DE CONTROLADOR
```python

ibdn@ibdn-VirtualBox:~/TFG_P4-main/TFG_P4-main/LXC-VNX-P4-L4-SDWAN$ sudo p4c --target bmv2 --arch v1model --p4runtime-files sdwan.p4info.txt sdwan.p4
ibdn@ibdn-VirtualBox:~/TFG_P4-main/TFG_P4-main/LXC-VNX-P4-L4-SDWAN$ 
ibdn@ibdn-VirtualBox:~/TFG_P4-main/TFG_P4-main/LXC-VNX-P4-L4-SDWAN$ sudo python3 sdwan_controlador.py \
  --p4info sdwan.p4info.txt --json sdwan.json \
  --s1-ip 172.17.2.1 --s2-ip 172.17.2.2 \
  --s1-grpc 9559     --s2-grpc 9559 \
  --prio-port 6000 --proto both

== Programando S1 ==
Adding default action to: IngressImpl.ipv4_lpm
action: IngressImpl.drop
[ok] default IngressImpl.ipv4_lpm -> IngressImpl.drop
  add LPM 10.0.0.0/24 -> 02:fd:00:00:00:01/02:fd:00:00:02:01 port 1
Adding entry to: IngressImpl.ipv4_lpm
match:
field_id: 1
lpm {
  value: "\n\000\000\000"
  prefix_len: 24
}

action: IngressImpl.ipv4_forward
param_id: 1
value: "\002\375\000\000\000\001"

param_id: 2
value: "\002\375\000\000\002\001"

param_id: 3
value: "\000\001"

  add LPM 10.1.0.0/24 -> 02:fd:00:00:03:02/02:fd:00:00:02:02 port 2
Adding entry to: IngressImpl.ipv4_lpm
match:
field_id: 1
lpm {
  value: "\n\001\000\000"
  prefix_len: 24
}

action: IngressImpl.ipv4_forward
param_id: 1
value: "\002\375\000\000\003\002"

param_id: 2
value: "\002\375\000\000\002\002"

param_id: 3
value: "\000\002"

  add PRIO tcp dstPort=6000 -> 02:fd:00:00:03:04/02:fd:00:00:02:04 port 4
Adding entry to: IngressImpl.prio_tcp_dst
match:
field_id: 1
exact {
  value: "\027p"
}

action: IngressImpl.set_nexthop_prio
param_id: 1
value: "\002\375\000\000\003\004"

param_id: 2
value: "\002\375\000\000\002\004"

param_id: 3
value: "\000\004"

  add PRIO tcp srcPort=6000 -> 02:fd:00:00:00:01/02:fd:00:00:02:01 port 1
Adding entry to: IngressImpl.prio_tcp_src
match:
field_id: 1
exact {
  value: "\027p"
}

action: IngressImpl.set_nexthop_prio
param_id: 1
value: "\002\375\000\000\000\001"

param_id: 2
value: "\002\375\000\000\002\001"

param_id: 3
value: "\000\001"

  add PRIO udp dstPort=6000 -> 02:fd:00:00:03:04/02:fd:00:00:02:04 port 4
Adding entry to: IngressImpl.prio_udp_dst
match:
field_id: 1
exact {
  value: "\027p"
}

action: IngressImpl.set_nexthop_prio
param_id: 1
value: "\002\375\000\000\003\004"

param_id: 2
value: "\002\375\000\000\002\004"

param_id: 3
value: "\000\004"

  add PRIO udp srcPort=6000 -> 02:fd:00:00:00:01/02:fd:00:00:02:01 port 1
Adding entry to: IngressImpl.prio_udp_src
match:
field_id: 1
exact {
  value: "\027p"
}

action: IngressImpl.set_nexthop_prio
param_id: 1
value: "\002\375\000\000\000\001"

param_id: 2
value: "\002\375\000\000\002\001"

param_id: 3
value: "\000\001"


== Programando S2 ==
Adding default action to: IngressImpl.ipv4_lpm
action: IngressImpl.drop
[ok] default IngressImpl.ipv4_lpm -> IngressImpl.drop
  add LPM 10.1.0.0/24 -> 02:fd:00:00:01:01/02:fd:00:00:03:01 port 1
Adding entry to: IngressImpl.ipv4_lpm
match:
field_id: 1
lpm {
  value: "\n\001\000\000"
  prefix_len: 24
}

action: IngressImpl.ipv4_forward
param_id: 1
value: "\002\375\000\000\001\001"

param_id: 2
value: "\002\375\000\000\003\001"

param_id: 3
value: "\000\001"

  add LPM 10.0.0.0/24 -> 02:fd:00:00:02:02/02:fd:00:00:03:02 port 2
Adding entry to: IngressImpl.ipv4_lpm
match:
field_id: 1
lpm {
  value: "\n\000\000\000"
  prefix_len: 24
}

action: IngressImpl.ipv4_forward
param_id: 1
value: "\002\375\000\000\002\002"

param_id: 2
value: "\002\375\000\000\003\002"

param_id: 3
value: "\000\002"

  add PRIO tcp dstPort=6000 -> 02:fd:00:00:01:01/02:fd:00:00:03:01 port 1
Adding entry to: IngressImpl.prio_tcp_dst
match:
field_id: 1
exact {
  value: "\027p"
}

action: IngressImpl.set_nexthop_prio
param_id: 1
value: "\002\375\000\000\001\001"

param_id: 2
value: "\002\375\000\000\003\001"

param_id: 3
value: "\000\001"

  add PRIO tcp srcPort=6000 -> 02:fd:00:00:02:04/02:fd:00:00:03:04 port 4
Adding entry to: IngressImpl.prio_tcp_src
match:
field_id: 1
exact {
  value: "\027p"
}

action: IngressImpl.set_nexthop_prio
param_id: 1
value: "\002\375\000\000\002\004"

param_id: 2
value: "\002\375\000\000\003\004"

param_id: 3
value: "\000\004"

  add PRIO udp dstPort=6000 -> 02:fd:00:00:01:01/02:fd:00:00:03:01 port 1
Adding entry to: IngressImpl.prio_udp_dst
match:
field_id: 1
exact {
  value: "\027p"
}

action: IngressImpl.set_nexthop_prio
param_id: 1
value: "\002\375\000\000\001\001"

param_id: 2
value: "\002\375\000\000\003\001"

param_id: 3
value: "\000\001"

  add PRIO udp srcPort=6000 -> 02:fd:00:00:02:04/02:fd:00:00:03:04 port 4
Adding entry to: IngressImpl.prio_udp_src
match:
field_id: 1
exact {
  value: "\027p"
}

action: IngressImpl.set_nexthop_prio
param_id: 1
value: "\002\375\000\000\002\004"

param_id: 2
value: "\002\375\000\000\003\004"

param_id: 3
value: "\000\004"


[done] Reglas instaladas. eth2=Internet, eth4=MPLS, puerto prioritario=6000 (both).
ibdn@ibdn-VirtualBox:~/TFG_P4-main/TFG_P4-main/LXC-VNX-P4-L4-SDWAN$ 
ibdn@ibdn-VirtualBox:~/TFG_P4-main/TFG_P4-main/LXC-VNX-P4-L4-SDWAN$ 

```


arp -s 10.0.0.254 02:fd:00:00:02:01 


iperf -s -p 6000  
iperf -c 10.0.0.2 -p 6000  


Si aún ves “incorrect”, mira en h1:
tcpdump -i eth1 -nnvvv "tcp port 6000 and (tcp[tcpflags] & (tcp-syn|tcp-ack) != 0)"


En h2 corre:

tcpdump -i eth1 -nnvvv "tcp port 6000" -s 0 -XX


Deberías dejar de ver “incorrect” en el cksum. Si se ve “unverified” es normal (tcpdump no siempre revalida), lo importante es que desaparezca el “incorrect -> 0x…” y que aparezca el SYN/ACK.


*******************
Apágalos ya en las patas del host (esto no requiere entrar al contenedor):

# interfaces lado host (ajusta la lista a las que tengas activas)
ifaces="h1-e1 h2-e1 s1-e1 s1-e2 s1-e4 s2-e1 s2-e2 s2-e4"

for d in $ifaces; do
  sudo ethtool -K "$d" rx off tx-checksum-ip-generic off gso off gro off tso off
done

# Verifica que quedaron en off
for d in $ifaces; do
  echo "== $d =="; sudo ethtool -k "$d" | egrep 'rx-check|tx-checksum-ip-generic|tso|gso|gro'
done




****************



CON ESTO HA FUNCIONADO


C) Plan B si no logras tocar offloads del LXC

Puedes hacer que el host corrija los checksums al vuelo con tc en los veth del host:

```python
for d in h1-e1 h2-e1 s1-e1 s1-e2 s1-e4 s2-e1 s2-e2 s2-e4; do
  sudo tc qdisc del dev "$d" clsact 2>/dev/null
  sudo tc qdisc add dev "$d" clsact
  sudo tc filter add dev "$d" egress protocol ip flower action csum ip tcp udp
done

```

Si quieres eliminar el “incorrect” en h1
1) Apaga offloads dentro de los LXC (sin instalar nada dentro)

Usa nsenter con los nombres reales (h1, h2, s1, s2), no “p4-h1”:

# Obtener PIDs
for c in h1 h2 s1 s2; do
  echo -n "$c PID: "; sudo lxc-info -n $c -Hp
done

# Ejemplo para h1 (cambia PID por el que salga arriba)
PID_H1=$(sudo lxc-info -n h1 -Hp)

# Ejecuta el ethtool del host *dentro* del netns del contenedor
sudo nsenter -t "$PID_H1" -n /usr/sbin/ethtool -K eth1 rx off tx off gso off gro off tso off tx-checksum-ip-generic off

# Verifica
sudo nsenter -t "$PID_H1" -n /usr/sbin/ethtool -k eth1 | egrep 'rx-check|tx-checksum-ip-generic|tso|gso|gro'


Repite para h2 si también capturas allí.

No hace falta “instalar ethtool en cada LXC”; con nsenter usas el binario del host en el netns del contenedor.

2) Mantén (opcional) el “plan B” de tc que ya aplicaste

Eso fuerza recomputar checksum en egreso del veth del host y ayuda a evitar falsos “incorrect”. Si quieres quitarlo:

for d in h1-e1 h2-e1 s1-e1 s1-e2 s1-e4 s2-e1 s2-e2 s2-e4; do
  sudo tc qdisc del dev "$d" clsact 2>/dev/null
done

¿Temporal o permanente?

ethtool -K y tc: son temporales (se pierden al reiniciar o al re-crear la topo).

Para hacerlos persistentes:

En el host: crea un script y un servicio systemd.

# /usr/local/sbin/p4-offloads-fix.sh
#!/usr/bin/env bash
ifaces="h1-e1 h2-e1 s1-e1 s1-e2 s1-e4 s2-e1 s2-e2 s2-e4"
for d in $ifaces; do
  ethtool -K "$d" rx off tx-checksum-ip-generic off gso off gro off tso off || true
  tc qdisc del dev "$d" clsact 2>/dev/null || true
  tc qdisc add dev "$d" clsact
  tc filter add dev "$d" egress protocol ip flower action csum ip tcp udp
done

# /etc/systemd/system/p4-offloads-fix.service
[Unit]
Description=Disable offloads and enforce checksums on P4 veths
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
ExecStart=/usr/local/sbin/p4-offloads-fix.sh
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target


Actívalo:

sudo chmod +x /usr/local/sbin/p4-offloads-fix.sh
sudo systemctl daemon-reload
sudo systemctl enable --now p4-offloads-fix.service


Con VNX/LXC: añade un “post-start”/script en tus start_s*.sh o en el XML (bloques exec/guest_cmd) para ejecutar los ethtool -K dentro de cada contenedor mediante nsenter.

Sobre tu P4 (por cerrar el tema)

Con el ajuste de meta.l4_len + update_checksum_with_payload que hicimos, el switch recalcula bien los checksums (incluyendo SYN con opciones). No necesitas lógica extra en MyVerifyChecksum ni tocar MyEgress para este caso.

El hecho de que h2 reporte cksum correct confirma que la corrección es efectiva y el camino de datos está OK.

Mini checklist final

 iperf OK en TCP/UDP por el camino que querías.

 Checksums correctos en puntos intermedios / receptor.

 (Opcional) Apagar offloads dentro de h1 si quieres que tcpdump en h1 deje de marcar “incorrect”.

 (Opcional) Persistir ethtool/tc con systemd o scripts VNX.

Si te parece, dime si quieres que te deje listos los scripts de VNX para aplicar nsenter+ethtool automáticamente al levantar h1/h2/s1/s2, y te los armo con los nombres exactos de tus contenedores.

ChatGPT puede cometer errores. Considera v
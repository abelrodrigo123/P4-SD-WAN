# ESCENARIO VNX CON SWITCH P4 BMv2

## INDICE 
- [Instrucciones ](#instrucciones)
  - [Instrucciones ](#ejecutar-escenario)
- [Conexion mediante GPRC](#Conexion-GRPC)
- [Compilar Programa P4 para L2](#compilar-p4-l2)
- [Conexion mediante CLI ](#USANDO-CLI)
- [Pruebas de conexion y depuración ](#pruebas)



## TOPOLOGIA

![Diseño](Imagenes\DiseñoL2.drawio180.png)

## INSTRUCCIONES:

### Ejecutar escenario.

```python
sudo vnx -f p4_vnx.xml -v --create 
```

al finalizar para limpiar escenario.

```python
sudo vnx -f p4_vnx.xml -v --destroy 

```
O utilizar 

```python
sudo vnx --clean-host

```
CONSIDERACIONES:
- Este escenario requiere de ARP para que h1 y h2 pueda obtener la direccion MAC al momento de realizar la prueba de ping, por lo que el programa inicial de p4 se tendria que modificar para permitir ARP y Broadcast, lo que opte es por realizar el registro de la MAC del equipo destino en cada uno de los host (en h1 regisre la mac e ip de h2 y viceversa) con ello no fue necesario modificar el programa de p4.
- El registro de MAC lo realice al momento que se crea el escenario en VNX, ejm. en h1 `<exec seq="on_boot" type="verbatim" ostype="system"> arp -s 10.0.0.2 02:fd:00:00:01:01</exec>`


```python
  <vm name="h1" type="lxc" arch="x86_64">
    <filesystem type="cow">/usr/share/vnx/filesystems/rootfs_lxc_ubuntu64</filesystem>
    <if id="1" net="Net1">
      <ipv4>10.0.0.1/24</ipv4>          
    </if>
    <exec seq="on_boot" type="verbatim" ostype="system"> arp -s 10.0.0.2 02:fd:00:00:01:01</exec>    
  </vm>
```



El escenario se creará y veremos creados h1, h2, s1, s2, los switch también se han inicializado de forma automática por la instalacion tmux que permite tener una consola adicional para mantener activo el servicio del switch (se comenta lineas abajo)

```python
sudo vnx -f p4_vnx.xml -v --create

```
En esta vista se observa la creacion y ejecución de BMv2 en el switch s2, iniciado de forma automática.

```python
host>      Created new process 65407 for vm 's2'
Calling execute_cmd for vm 's2' with seq 'on_boot'...
lxc-execute_cmd-s2>  /usr/bin/rm -rf /root/.vnx/scenarios/p4_vnx/vms/s2/tmp/on_boot/filetree/1
lxc-execute_cmd-s2>  executing user defined exec command:
lxc-execute_cmd-s2>      sleep 3;
lxc-execute_cmd-s2>      tmux new-session -d -s switch2 /behavioral-model/targets/simple_switch_grpc/simple_switch_grpc --no-p4  -i 1@eth1 -i 2@eth2 --thrift-port 9091 --device-id 2;
lxc-execute_cmd-s2>      echo "Switch iniciado" >> /root/start_s2.log;
lxc-execute_cmd-s2>  /usr/bin/lxc-attach --clear-env -n s2 -- /bin/bash -l -c 'sleep 3;tmux new-session -d -s switch2 /behavioral-model/targets/simple_switch_grpc/simple_switch_grpc --no-p4  -i 1@eth1 -i 2@eth2 --thrift-port 9091 --device-id 2;\necho "Switch iniciado" >> /root/start_s2.log;\n'
...execute_cmd for vm 's2' with seq 'on_boot' returns OK
```

## Conexion GRPC

Luego de ello solo hace falta poblar las tablas, para ello utilizamos el archivo de python que se llama contrador.py que contiene la configuracion de IP, ID, puerto y tablas de cada switch y con ello de subirá la lógica de p4 (my_program) que se encuentra en los archivos compilados y son necesarios para esta tarea como se indica en el archivo controlador.py

```python
sudo python3 controlador.py 
```

Se trendrá una vista similar a la siguiente que indica que se han poblados las tablas en los switch 1 y 2


```python
ibdn@ibdn-VirtualBox:~/TFG_P4-main/TFG_P4-main/LXC-VNX-P4-BMv2-L2-forwarding$ sudo python3 controlador.py 
Adding entry to: dmac
match:
field_id: 1
exact {
  value: "\002\375\000\000\000\001"
}

action: forward
param_id: 1
value: "\000\001"

Adding entry to: dmac
match:
field_id: 1
exact {
  value: "\002\375\000\000\001\001"
}

action: forward
param_id: 1
value: "\000\002"

Adding default action to: dmac
Unknown action 'drop'
Adding entry to: dmac
match:
field_id: 1
exact {
  value: "\002\375\000\000\001\001"
}

action: forward
param_id: 1
value: "\000\001"

Adding entry to: dmac
match:
field_id: 1
exact {
  value: "\002\375\000\000\000\001"
}

action: forward
param_id: 1
value: "\000\002"

ibdn@ibdn-VirtualBox:~/TFG_P4-main/TFG_P4-main/LXC-VNX-P4-BMv2-L2-forwarding$ 

```

Luego realizamos pruebas de ping de h1 a h2 


```python
PING 10.1.0.2 (10.1.0.2) 56(84) bytes of data.
64 bytes from 10.1.0.2: icmp_seq=1 ttl=62 time=1.67 ms
64 bytes from 10.1.0.2: icmp_seq=2 ttl=62 time=1.20 ms
64 bytes from 10.1.0.2: icmp_seq=3 ttl=62 time=1.09 ms
64 bytes from 10.1.0.2: icmp_seq=4 ttl=62 time=1.93 ms
64 bytes from 10.1.0.2: icmp_seq=5 ttl=62 time=1.12 ms
64 bytes from 10.1.0.2: icmp_seq=6 ttl=62 time=0.860 ms
64 bytes from 10.1.0.2: icmp_seq=7 ttl=62 time=1.02 ms
```

Si se desea ver el procesamiento de tablas conectarse a tmux



Consideraciones para que el programa funcione correctamente.


## Compilar P4 L2

### Crear programa p4 en LXC my_programa.p4

Dado que el programa de p4 para capa 2 solo trabaja en funcion de la direcciones MAC es necesario compilar el codigo y genere los archivo que utilizara el archivo controlado.py (json, txt) ya que es la funcionalidad del switch.

Desde el host realizarlo en la ubicacion del proyecto de L2

```python
sudo p4c --target bmv2 --arch v1model --p4runtime-files my_program.p4rt.txt my_program.p4

```
Vista 

```python
ibdn@ibdn-VirtualBox:~/TFG_P4-main/TFG_P4-main/LXC-VNX-P4-BMv2-L2-forwarding$ sudo p4c --target bmv2 --arch v1model --p4runtime-files my_program.p4rt.txt my_program.p4
```



EN CONSOLA 2 de S1, abrir con el comando desde el host:

```python
ibdn@ibdn-VirtualBox:~/TFG_P4-main/TFG_P4-main$ sudo vnx -f p4_vnx.xml -v -console -M s1
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

```python
root@s1:~# netstat -tuln | grep 9559
tcp6       0      0 :::9559                 :::*                    ESCUCHAR   
root@s1:~# ip link show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: eth1@if42: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT group default qlen 1000
    link/ether 02:fd:00:00:02:01 brd ff:ff:ff:ff:ff:ff link-netnsid 0
3: eth2@if43: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT group default qlen 1000
    link/ether 02:fd:00:00:02:02 brd ff:ff:ff:ff:ff:ff link-netnsid 0
4: eth3@if44: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT group default qlen 1000
    link/ether 02:fd:00:00:02:03 brd ff:ff:ff:ff:ff:ff link-netnsid 0
root@s1:~# 

```

#### Inspección de Puertos y Servicios

```python
lsof -i -P -n | grep 9090
lsof -i -P -n | grep 9559
```
Verficando.
```python
root@s1:~# lsof -i -P -n | grep 9090
lsof -i -P -n | grep 9559
simple_sw 313            root   20u  IPv4 248252      0t0  TCP *:9090 (LISTEN)
simple_sw 313            root   13u  IPv6 248243      0t0  TCP *:9559 (LISTEN)
root@s1:~# 
```


** Abrir una segunda consola en s1
ibdn@ibdn-VirtualBox:~/TFG_P4-main/TFG_P4-main$ sudo vnx -f p4_vnx.xml -v -console -M s1

```
sudo vnx -f p4_vnx.xml -v -console -M s1
```
NOTAS:
Cuando se ejecuta un programa en background, el equipo se puede recuperar el ultimo comando que se ejecuta
fg = para traer un proceso background

sudo vnx -f p4_vnx.xml -M s1 --destroy  (maquina especifica)


sudo vnx -f p4_vnx.xml -M s1 --create


ver Ejecucion del Switch S1

```python
root@s1:~# lsof -i
COMMAND   PID            USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
systemd-r 104 systemd-resolve   13u  IPv4  58122      0t0  UDP localhost:domain 
systemd-r 104 systemd-resolve   14u  IPv4  58123      0t0  TCP localhost:domain (LISTEN)
sshd      183            root    3u  IPv4  59641      0t0  TCP *:ssh (LISTEN)
sshd      183            root    4u  IPv6  59643      0t0  TCP *:ssh (LISTEN)
simple_sw 246            root   13u  IPv6  65921      0t0  TCP *:9559 (LISTEN)
simple_sw 246            root   20u  IPv4  65929      0t0  TCP *:9090 (LISTEN)
root@s1:~# 

```

En caso de error se puede validar el proceso de ejecución del SW

```python
ps aux | grep simple_switch_grpc
```


#### Ver Topologia

```python
ibdn@ibdn-VirtualBox:~/TFG_P4-main/TFG_P4-main$ sudo vnx -f p4_vnx.xml -v --show-map 
```

![Topologia](Imagenes\Topologia.png)


COMPILAR
s```python
udo p4c --target bmv2 --arch v1model --p4runtime-files sdwan.p4rt.txt sdwan.p4
```


********************************


# OPCION 2
## USANDO CLI 

## INGRESO MEDIANTE LA CLI A LOS SWITCHS.

Para realizar los descartes de los problemas utilice este modo de ingreso a los Switch.
Ingrese a la consola de s1 y s2 y utilice el comando kill -9 <ID> para finalizar el proceso del switch e volverlo a iniciarlo con el script que tiene cada uno y cuenta con el parametro de `--log-console` con ello ver todos los mensajes que pasan por el switch.


### EN S1 

Se puede ingresar a la carpeta y luego ejecutar el comando o mediante un solo comando.


Inicar el Switch con el script `start_s1.sh` que se encuentra en la raiz del s1 y s2.


Abrir un nuevo terminal de s1 porque el anterior se quedara ocupado con los logs o en caso desear usar el mismo terminal al script añadir simbolo de "&" al finalizar el switch


```python
sudo vnx -f p4_vnx.xml -v -console -M s1
```
luego de inicar el switch conectarse mediante la CLI desde s1 root@s1:~# /behavioral-model/tools/runtime_CLI.py --thrift-port 9090

```python
/behavioral-model/tools/runtime_CLI.py --thrift-port 9090
```


Población de las tablas de reenvío para s1, aqui nos da un error, porque necesita que s1 tenga los archivos que son txt y json, para ello podemos comentar las lineas de poblar las tablas de s1 y s2 y utilizar la configuracion remota que nos brinda p4-utils y realizar la carga manualmente.

Vista de error.
```python
root@s1:~#/behavioral-model/tools/runtime_CLI.py --thrift-port 9090
Obtaining JSON from switch...
Done
Control utility for runtime P4 table manipulation
RuntimeCmd: table_add dmac forward 02:fd:00:00:00:01 => 1
Error: Invalid table name (dmac)
RuntimeCmd: table_add dmac forward 02:fd:00:00:01:01 => 2
Error: Invalid table name (dmac)
RuntimeCmd: 
```

Ahora realizamos la carga de los archivos con el archibvo `Notablas_controlador.py` que he comentado las lineas de poblar las tablas para facilitar la tarea. (iniciar BMv2 en s1 y s2 con scripts)


```python
ibdn@ibdn-VirtualBox:~/TFG_P4-main/TFG_P4-main/LXC-VNX-P4-BMv2-L2-forwarding$ sudo python3 notablas_controlador.py 

```




```python
sudo vnx -f p4_vnx.xml -v -console -M s1 s2
```
Conectarse a la CLI

root@s2:~# /behavioral-model/tools/runtime_CLI.py --thrift-port 9090
Obtaining JSON from switch...
Done
Control utility for runtime P4 table manipulation
RuntimeCmd: 




en s1

```python
table_add dmac forward 02:fd:00:00:00:01 => 1
table_add dmac forward 02:fd:00:00:01:01 => 2
```

Se deberia de visualizar del siguiente modo en la CLI


```python
rroot@s1:~# /behavioral-model/tools/runtime_CLI.py --thrift-port 9090
Obtaining JSON from switch...
Done
Control utility for runtime P4 table manipulation
RuntimeCmd: table_add dmac forward 02:fd:00:00:00:01 => 1
Adding entry to exact match table dmac
match key:           EXACT-02:fd:00:00:00:01
action:              forward
runtime data:        00:01
Entry has been added with handle 0
RuntimeCmd: table_add dmac forward 02:fd:00:00:01:01 => 2
Adding entry to exact match table dmac
match key:           EXACT-02:fd:00:00:01:01
action:              forward
runtime data:        00:02
Entry has been added with handle 1
RuntimeCmd: 
```



Verificar que las tablas se hayan ingresado correctamente con el siguiente comando. `table_dump MyIngress.dmac` (se completa tabulando)

```python
RuntimeCmd: table_dump MyIngress.dmac
==========
TABLE ENTRIES
**********
Dumping entry 0x0
Match key:
* ethernet.dstAddr    : EXACT     02fd00000001
Action entry: MyIngress.forward - 01
**********
Dumping entry 0x1
Match key:
* ethernet.dstAddr    : EXACT     02fd00000101
Action entry: MyIngress.forward - 02
==========
Dumping default entry
Action entry: NoAction - 
==========
RuntimeCmd: 

```




#### S2

Abrir segunda consola para s2

/behavioral-model/tools/runtime_CLI.py --thrift-port 9090

En consola 1, incializar el switch BMv2


```python
root@s2:~# /behavioral-model/tools/runtime_CLI.py --thrift-port 9090
Obtaining JSON from switch...
Done
Control utility for runtime P4 table manipulation
RuntimeCmd: table_add dmac forward 02:fd:00:00:00:01 => 2
Adding entry to exact match table dmac
match key:           EXACT-02:fd:00:00:00:01
action:              forward
runtime data:        00:02
Entry has been added with handle 0
RuntimeCmd: table_add dmac forward 02:fd:00:00:01:01 => 1
Adding entry to exact match table dmac
match key:           EXACT-02:fd:00:00:01:01
action:              forward
runtime data:        00:01
Entry has been added with handle 1
RuntimeCmd: table_dump MyIngress.dmac
==========
TABLE ENTRIES
**********
Dumping entry 0x0
Match key:
* ethernet.dstAddr    : EXACT     02fd00000001
Action entry: MyIngress.forward - 02
**********
Dumping entry 0x1
Match key:
* ethernet.dstAddr    : EXACT     02fd00000101
Action entry: MyIngress.forward - 01
==========
Dumping default entry
Action entry: NoAction - 
==========
RuntimeCmd: 

```


### Pruebas 
Ping entre h1 y h2: Después de poblar las tablas, verifica que se pueda hacer ping entre h1 y h2
ping 10.1.0.2  # Desde h1

```python
root@h1:~# ping 10.1.0.2
PING 10.1.0.2 (10.1.0.2) 56(84) bytes of data.
64 bytes from 10.1.0.2: icmp_seq=1 ttl=62 time=2.06 ms
64 bytes from 10.1.0.2: icmp_seq=2 ttl=62 time=1.81 ms
^C
--- 10.1.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1000ms
rtt min/avg/max/mdev = 1.805/1.931/2.058/0.126 ms
root@h1:~# 
```



En el terminal de los logs de s1 se puede observar como se realiza el tratamiento de los paquetes.


```python

[17:16:10.504] [bmv2] [D] [thread 338] [17.0] [cxt 0] Table 'MyIngress.dmac': hit with handle 0
[17:16:10.504] [bmv2] [D] [thread 338] [17.0] [cxt 0] Dumping entry 0
Match key:
* hdr.ethernet.dstAddr: EXACT     02fd00000001
Action entry: MyIngress.forward - 1,

[17:16:10.504] [bmv2] [D] [thread 338] [17.0] [cxt 0] Action entry is MyIngress.forward - 1,
[17:16:10.504] [bmv2] [T] [thread 338] [17.0] [cxt 0] Action MyIngress.forward
[17:16:10.504] [bmv2] [T] [thread 338] [17.0] [cxt 0] my_program.p4(67) Primitive standard_metadata.egress_spec = egress_port
[17:16:10.504] [bmv2] [D] [thread 338] [17.0] [cxt 0] Pipeline 'ingress': end
[17:16:10.504] [bmv2] [D] [thread 338] [17.0] [cxt 0] Egress port is 1
[17:16:10.504] [bmv2] [D] [thread 340] [17.0] [cxt 0] Pipeline 'egress': start
[17:16:10.504] [bmv2] [D] [thread 340] [17.0] [cxt 0] Pipeline 'egress': end
[17:16:10.504] [bmv2] [D] [thread 340] [17.0] [cxt 0] Deparser 'deparser': start
[17:16:10.504] [bmv2] [D] [thread 340] [17.0] [cxt 0] Deparsing header 'ethernet'
[17:16:10.504] [bmv2] [D] [thread 340] [17.0] [cxt 0] Deparser 'deparser': end
[17:16:10.504] [bmv2] [D] [thread 343] [17.0] [cxt 0] Transmitting packet of size 98 out of port 1


```




en el consola de s1 digitar lo siguiente:

```python
tcpdump -i eth1 -vv

```

Vista de paquetes en h2

```python
root@h2:~# tcpdump -i eth1 -vv
tcpdump: listening on eth1, link-type EN10MB (Ethernet), snapshot length 262144 bytes
17:18:52.301087 IP (tos 0x0, ttl 64, id 9185, offset 0, flags [DF], proto ICMP (1), length 84)
    10.0.0.1 > h2: ICMP echo request, id 12, seq 1, length 64
17:18:52.301105 IP (tos 0x0, ttl 64, id 61648, offset 0, flags [none], proto ICMP (1), length 84)
    h2 > 10.0.0.1: ICMP echo reply, id 12, seq 1, length 64
17:18:53.302798 IP (tos 0x0, ttl 64, id 9797, offset 0, flags [DF], proto ICMP (1), length 84)
    10.0.0.1 > h2: ICMP echo request, id 12, seq 2, length 64
17:18:53.302817 IP (tos 0x0, ttl 64, id 61826, offset 0, flags [none], proto ICMP (1), length 84)
    h2 > 10.0.0.1: ICMP echo reply, id 12, seq 2, length 64
17:18:54.304583 IP (tos 0x0, ttl 64, id 9862, offset 0, flags [DF], proto ICMP (1), length 84)
    10.0.0.1 > h2: ICMP echo request, id 12, seq 3, length 64
17:18:54.304619 IP (tos 0x0, ttl 64, id 61981, offset 0, flags [none], proto ICMP (1), length 84)
    h2 > 10.0.0.1: ICMP echo reply, id 12, seq 3, length 64
17:18:55.306083 IP (tos 0x0, ttl 64, id 10159, offset 0, flags [DF], proto ICMP (1), length 84)
    10.0.0.1 > h2: ICMP echo request, id 12, seq 4, length 64
17:18:55.306100 IP (tos 0x0, ttl 64, id 62895, offset 0, flags [none], proto ICMP (1), length 84)
    h2 > 10.0.0.1: ICMP echo reply, id 12, seq 4, length 64
17:18:56.307974 IP (tos 0x0, ttl 64, id 11112, offset 0, flags [DF], proto ICMP (1), length 84)
    10.0.0.1 > h2: ICMP echo request, id 12, seq 5, length 64
17:18:56.307996 IP (tos 0x0, ttl 64, id 62898, offset 0, flags [none], proto ICMP (1), length 84)


```


## Modificar imagen
Imagen tiene el Switch BMv2 y P4C.


```python
ibdn@ibdn-VirtualBox:/usr/share/vnx/filesystems$ sudo vnx --modify-rootfs rootfs_lxc_ubuntu64

Ubuntu 22.04.2 LTS vnxrootfslxcubuntu64-22.04-v025 console

vnxrootfslxcubuntu64-22 login: root
Contraseña: 
Welcome to Ubuntu 22.04.2 LTS (GNU/Linux 6.8.0-79-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

 * Introducing Expanded Security Maintenance for Applications.
   Receive updates to over 25,000 software packages with your
   Ubuntu Pro subscription. Free for personal use.

     https://ubuntu.com/pro
Último inicio de sesión: vie sep  5 17:23:27 UTC 2025 en console
root@vnxrootfslxcubuntu64-22:~# p4c --version
p4c 1.2.4.2 (SHA: 624c6be80 BUILD: RELEASE)
root@vnxrootfslxcubuntu64-22:~# 

```

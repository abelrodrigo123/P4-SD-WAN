
<p align="left">
  <img src="Imagenes/LogoUPM.png"  width="220" height="100"
</p>



# Escenario de Capa 2 con P4 y BMv2 en VNX

Este escenario valida el **reenvío Ethernet (Capa 2)** sobre **switches P4 BMv2** (`simple_switch_grpc`) desplegados en **LXC** y orquestados con **VNX**. Se centra en una topología mínima (**h1–s1–s2–h2**) con **plano de gestión** separado para control (gRPC/Thrift), y emplea **tmux** para mantener activos los switches sin bloquear el despliegue. La lógica L2 se implementa con una **tabla `dmac` de match exacto a MAC destino** y acción `forward`.

## Índice

- Diseño y Topología
- Instrucciones de despliegue
- Compilación del programa P4
- Inicialización de switches BMv2
- Configuración de tablas
- Pruebas de conectividad
- Depuración y CLI
- Conclusión

---

## Diseño y Topología

La topología diseñada está compuesta por cuatro nodos virtuales: dos hosts finales (h1 y h2) y dos switches BMv2 (s1 y s2), todos implementados como contenedores LXC gestionados por VNX.

Cada switch dispone de dos interfaces de datos (eth1 y eth2) y una interfaz adicional de gestión (eth3), utilizada para la comunicación con el controlador a través de la red de gestión (172.17.2.0/24)


![Diseño](Imagenes\DiseñoL2.drawio180.png)

---


## RESUMEN EJECUTIVO:

**Si solo quieres validar el escenario :**


1) Crear el escenario

```python
 sudo vnx -f p4_vnx.xml -v --create

```
 (El XML arranca BMv2 en tmux.)

2) Ejecutar el controlador y probar**

 ```python
 python3 controlador.py
 ```

 3) Realiza las pruebas mediante ping de h1 a h2:

  ```python
  ping 10.1.0.2
  ```
 
 4) Limpieza

```python
 sudo vnx -f p4_vnx.xml -v --destroy
 # sudo vnx --clean-host   # limpieza total (opcional)
 ```
---


Ahora se muestra a detalle el paso a paso:





## Instrucciones de despliegue

### Crear el escenario

```bash
sudo vnx -f p4_vnx.xml -v --create
```

Limpiar el escenario


```python
sudo vnx -f p4_vnx.xml -v --destroy

```

O alternativamente:

```python
sudo vnx --clean-host

```

#### Ver Topologia VNX.

```python
ibdn@ibdn-VirtualBox:~/TFG_P4-main/TFG_P4-main$ sudo vnx -f p4_vnx.xml -v --show-map 
```

![Topologia](Imagenes\Topologia.png)


## Compilación del programa P4

Desde el host, compilar el programa de Capa 2:

```python
sudo p4c --target bmv2 --arch v1model --p4runtime-files my_program.p4rt.txt my_program.p4

```


## Inicialización de switches BMv2

Los switches se inician automáticamente mediante Tmux:

```python
tmux new-session -d -s switch2 /behavioral-model/targets/simple_switch_grpc/simple_switch_grpc --no-p4 -i 1@eth1 -i 2@eth2 --thrift-port 9091 --device-id 2
```

Verificación de puertos:

```python
lsof -i -P -n | grep 9090
lsof -i -P -n | grep 9559
netstat -tuln | grep 9559

```
Verficando:

```python
root@s1:~# sudo lsof -i
COMMAND   PID            USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
systemd-r  95 systemd-resolve   13u  IPv4 237875      0t0  UDP localhost:domain 
systemd-r  95 systemd-resolve   14u  IPv4 237876      0t0  TCP localhost:domain (LISTEN)
sshd      190            root    3u  IPv4 239177      0t0  TCP *:ssh (LISTEN)
sshd      190            root    4u  IPv6 239179      0t0  TCP *:ssh (LISTEN)
simple_sw 313            root   13u  IPv6 248243      0t0  TCP *:9559 (LISTEN)
simple_sw 313            root   20u  IPv4 248252      0t0  TCP *:9090 (LISTEN)
root@s1
```


## Configuración de tablas

Utilizar el script controlador.py para poblar las tablas:

```python
sudo python3 controlador.py

```


Ejemplo de salida:

```python
Adding entry to: dmac
match: 02:fd:00:00:00:01 => port 1
match: 02:fd:00:00:01:01 => port 2
```

## Pruebas de conectividad

Desde h1:

```python
ping 10.1.0.2

```

Ejemplo de respuesta:

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


Captura de paquetes en h2:

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
```


## Depuración y CLI

Acceder a la CLI del switch:

```python
/behavioral-model/tools/runtime_CLI.py --thrift-port 9090

```


Poblar manualmente las tablas:

```python
table_add dmac forward 02:fd:00:00:00:01 => 1
table_add dmac forward 02:fd:00:00:01:01 => 2
```

Verificar contenido:

```python
table_dump MyIngress.dmac

```

## Conclusión

Este escenario demuestra la viabilidad técnica de implementar reenvío Ethernet en Capa 2 mediante P4 y BMv2 en entornos virtualizados con VNX y LXC. Se valida la conectividad entre hosts, la configuración dinámica del plano de datos y el uso de herramientas de depuración como CLI y tcpdump.


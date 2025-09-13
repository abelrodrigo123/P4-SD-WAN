
<p align="left">
  <img src="imagenes/LogoUPM.png"  width="220" height="100"
</p>



# Dockerfile P4 BMv2


Construir la imagen Docker:

```python
docker build -t bmv2_p4_v1 .

Construir contenedor con un archivo de dockerfile especifico. (version ligera)
docker build -t p4-bmv2:v2 -f Dockerfile3 .


```
Ejecutar el contenedor con red privilegiada (para interfaces virtuales):

```python
docker run --privileged -it bmv2_p4_v1

```

Ejecuta un nuevo terminal en el contenedor:

docker exec -it <ID_contenedor> bash

Este comando abrirá una nueva sesión interactiva de Bash dentro del mismo contenedo.




## Se creó un nuevo contenedor que incluye:


### Requisitos del Controlador

Para el correcto funcionamiento del controlador, son necesarios los siguientes componentes:

* **Python 3**: Un entorno de programación esencial para la ejecución de *scripts* y la automatización de tareas.
* **`p4-utils`**: Un conjunto de utilidades clave para la comunicación y el control de los *targets* de P4.
* **`p4c`**: El compilador **P4C** es fundamental para compilar los programas P4 en código ejecutable por el *switch*.

---

### Características Clave

* **Switch BMv2**: Incluye el repositorio `p4lang/behavioral-model` de P4, lo que facilita la simulación de redes definidas por software (**SDN**) y el desarrollo de nuevos protocolos de red.
* **Compilador `p4c`**: El compilador `p4c` está instalado y configurado para compilar programas P4 dirigidos al *target* BMv2.
* **`p4-utils`**: Se han instalado las utilidades **`p4-utils`** para facilitar el desarrollo, control y depuración de programas P4 y *targets* BMv2. Se incluyó el paquete **`help2man`** para asegurar que la instalación de `p4-utils` se completara sin errores, permitiendo la generación de las páginas de manual.
* **Herramientas de Red**: El entorno contiene herramientas esenciales para el análisis y la depuración de redes, como `net-tools`, `iperf`, `netcat`, `traceroute` y `hping3`.



El archivo Dockerfile fue compilado y subido al sitio de hub.docker.





---

## Iniciar el switch BMv2 desde el contenedor:


```python
init_switch.sh

```

Poblar las tablas desde el contenedor:

```python
populate_tables.sh
```


```python
docker exec -it bmv2_p4_v1 /bin/bash
```

Detener contenedor por id
```python
docker stop <nombre_contenedor>

Ejemplo:
docker stop 7de83a7ce770
```


Eliminar una imagen:

docker rmi <id_imagen>


Eliminar todas las imágenes:

docker rmi $(docker images -q)

Limpiar el entorno de pruebas (esto incluye detener y eliminar todos los contenedores, imágenes, volúmenes y redes no utilizados):


```python
docker system prune -a

```

Asegúrate de que simple_switch_grpc está habilitado
./configure --with-thrift --with-pi --enable-debugger


/behavioral-model/targets/simple_switch_grpc/simple_switch_grpc --version



Construir contenedor con un archivo de dockerfile especifico. 
docker build -t p4-bmv2:v2-f Dockerfile3 .



Al ejecutar el contenedor e intentar conectarse al switch dara un error, pues el contenedor solo tiene una interface de red
y para el escenario de prueba requerimos al menos 3, aqui una vista de lo indicado.

Comandos:

docker run -it bmv2:v2 /bin/bash
Como el workdir esta establecido en la ruta `/behavioral-model/targets/simple_switch_grpc` solo sera necesario ejecutar los comandos para inicar el switch_grpc

```python
simple_switch_grpc \
  -i 1@eth1 -i 2@eth2 -i 3@eth3 \
  --log-console \
  --thrift-port 9090 \
  --device-id 1 \
  ./my_program.json

```

```python
ibdn@ibdn-VirtualBox:~/TFG_P4-main/TFG_P4-main/Dockerfile-P4-BMv2$ docker run -it bmv2:v2 /bin/bash
root@7de83a7ce770:/behavioral-model/targets/simple_switch_grpc# 
root@7de83a7ce770:/behavioral-model/targets/simple_switch_grpc# ls
my_program.json  my_program.p4  my_program.p4i  my_program.p4rt.txt
root@7de83a7ce770:/behavioral-model/targets/simple_switch_grpc# pwd
/behavioral-model/targets/simple_switch_grpc
root@7de83a7ce770:/behavioral-model/targets/simple_switch_grpc# lsof -i
root@7de83a7ce770:/behavioral-model/targets/simple_switch_grpc# sudo lsof -i
root@7de83a7ce770:/behavioral-model/targets/simple_switch_grpc# ls
my_program.json  my_program.p4  my_program.p4i  my_program.p4rt.txt
root@7de83a7ce770:/behavioral-model/targets/simple_switch_grpc# simple_switch_grpc \
  -i 1@eth1 -i 2@eth2 -i 3@eth3 \
  --log-console \
  --thrift-port 9090 \
  --device-id 1 \
  ./my_program.json
Calling target program-options parser
[12:10:18.476] [bmv2] [D] [thread 18] Set default default entry for table 'MyIngress.ipv4_lpm': MyIngress.drop - 
Adding interface eth1 as port 1
[12:10:18.476] [bmv2] [D] [thread 18] Adding interface eth1 as port 1
[12:10:18.481] [bmv2] [E] [thread 18] Add port operation failed
Adding interface eth2 as port 2
[12:10:18.481] [bmv2] [D] [thread 18] Adding interface eth2 as port 2
[12:10:18.485] [bmv2] [E] [thread 18] Add port operation failed
Adding interface eth3 as port 3
[12:10:18.486] [bmv2] [D] [thread 18] Adding interface eth3 as port 3
[12:10:18.489] [bmv2] [E] [thread 18] Add port operation failed
Server listening on 0.0.0.0:9559
[12:10:18.499] [bmv2] [I] [thread 18] Starting Thrift server on port 9090
[12:10:18.500] [bmv2] [I] [thread 18] Thrift server was started
^C
root@7de83a7ce770:/behavioral-model/targets/simple_switch_grpc# ifconfig
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 172.17.0.2  netmask 255.255.0.0  broadcast 172.17.255.255
        ether 26:59:cb:2d:8f:de  txqueuelen 0  (Ethernet)
        RX packets 52  bytes 4661 (4.6 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 3  bytes 126 (126.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

root@7de83a7ce770:/behavioral-model/targets/simple_switch_grpc# 
```


Solución: Agregar Interfaces con Docker

Paso 1: Crear Interfaces Virtuales en el Host
Crea interfaces virtuales en el host y enlázalas al contenedor usando veth pares.

```python
sudo ip link add eth1_host type veth peer name eth1
sudo ip link add eth2_host type veth peer name eth2
sudo ip link add eth3_host type veth peer name eth3
sudo ip link set eth1_host up
sudo ip link set eth2_host up
sudo ip link set eth3_host up
```

Paso 2: Conectar las Interfaces al Contenedor
Usa docker network connect o directamente configura las interfaces en el contenedor.

Conectar manualmente usando ip link:

Asocia las interfaces creadas al contenedor.

```python
CONTAINER_ID=$(docker ps -q -l)
sudo ip link set eth1 netns $(docker inspect --format '{{.State.Pid}}' $CONTAINER_ID)
sudo ip link set eth2 netns $(docker inspect --format '{{.State.Pid}}' $CONTAINER_ID)
sudo ip link set eth3 netns $(docker inspect --format '{{.State.Pid}}' $CONTAINER_ID)
Agregar las interfaces al contenedor:
```

Dentro del contenedor, habilita las interfaces y asígnales direcciones IP.


```python
docker exec -it $CONTAINER_ID bash
ip link set eth1 up
ip link set eth2 up
ip link set eth3 up
```


Abrimos otro terminal del contenedor para ejecutar pruebas en contenedor `bmv2:v2`

```python
docker run -it bmv2:v2 /bin/bash
```


Crear las redes Docker

```python
docker network create red1
docker network create red2
docker network create red3

```
Verficar redes creadas:

```python
docker network ls

```

Con el contenedor ya creado, al ejecutar el contenedor p4-bmv2-without-p4c, utilizaremos la opción --network para conectarlo a la primera red y la opción --network-alias para darle un nombre dentro de esa red.

--network red1: Conecta el contenedor a la red Docker llamada red1.
--network-alias eth1: Asigna el alias eth1 a la interfaz de red del contenedor dentro de la red red1.


```python
docker run --name BMv2_p4 --network red1 --network-alias eth1 --network red2 --network-alias eth2 --network red3 --network-alias eth3 -it p4-bmv2-without-p4c:v1
```

















## Codigo para construir contenedor pero pesa 7.32 GB

```python
# Dockerfile
FROM ubuntu:22.04

# Desactivar interactividad (evitar preguntas durante instalación)
ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependencias básicas y configurar el entorno
RUN apt-get update && apt-get install -y \
    curl gnupg software-properties-common sudo iproute2 iputils-ping \
    nano lsof net-tools python3 python3-pip graphviz \
    git build-essential libboost-dev libevent-dev sudo \
    automake cmake libgmp-dev \
    libpcap-dev libboost-test-dev libboost-program-options-dev \
    libboost-system-dev libboost-filesystem-dev libboost-thread-dev \
    libevent-dev libtool flex bison pkg-config g++ libssl-dev \
    lcov vim thrift-compiler libthrift-dev libboost-all-dev \
    && rm -rf /var/lib/apt/lists/*  
    
   
# Añadir repositorios para BMv2 y P4C
RUN . /etc/os-release && \
    echo "deb http://download.opensuse.org/repositories/home:/p4lang/xUbuntu_${VERSION_ID}/ /" | tee /etc/apt/sources.list.d/home:p4lang.list && \
    curl -fsSL "https://download.opensuse.org/repositories/home:p4lang/xUbuntu_${VERSION_ID}/Release.key" | gpg --dearmor | tee /etc/apt/trusted.gpg.d/home_p4lang.gpg > /dev/null && \
    apt-get update && \
    apt-get install -y p4lang-bmv2 p4lang-p4c && \
    rm -rf /var/lib/apt/lists/*


# Instalar BMv2 desde el repositorio de GitHub
RUN git clone https://github.com/p4lang/behavioral-model.git && \
    cd behavioral-model && \
    ./install_deps_ubuntu_22.04.sh && \
    ./autogen.sh && \
    ./configure && \
    make && \
    make install &&\
    make -j4

# Instalar p4runtime-shell y dependencias de gRPC
RUN pip3 install grpcio==1.44.0 grpcio-tools p4runtime-shell

# Configuración del directorio de trabajo
WORKDIR /behavioral-model/targets/simple_switch_grpc

# Copiar archivos necesarios para ejecutar el programa P4
COPY my_program.p4 ./
RUN p4c --target bmv2 --arch v1model --p4runtime-files my_program.p4rt.txt my_program.p4

# Copiar scripts
COPY init_switch.sh /usr/local/bin/init_switch.sh
COPY populate_tables.sh /usr/local/bin/populate_tables.sh
RUN chmod +x /usr/local/bin/init_switch.sh /usr/local/bin/populate_tables.sh

# Exponer puertos necesarios
EXPOSE 9090
EXPOSE 9559

# Comando por defecto
CMD ["/bin/bash"]
# CMD ["simple_switch", "--help"]
```






```python
# Versión mas compacta con P4c
FROM debian:11-slim

# Configurar entorno no interactivo
ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependencias mínimas, tmux para iniciar bmv2 en un nuevo terminal. #libboost-all-dev thrift-compiler && \tcpdump
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl gnupg software-properties-common sudo iproute2 iputils-ping graphviz \
    python3 python3-pip git nano lsof net-tools iperf netcat traceroute hping3 \
    tmux  help2man  
    

# Añadir repositorio y clave de P4lang para instalar compilador P4C
RUN echo 'deb http://download.opensuse.org/repositories/home:/p4lang/Debian_11/ /' | tee /etc/apt/sources.list.d/home_p4lang.list && \
    curl -fsSL https://download.opensuse.org/repositories/home:p4lang/Debian_11/Release.key | gpg --dearmor | tee /etc/apt/trusted.gpg.d/home_p4lang.gpg > /dev/null && \
    apt-get update && apt-get install -y --no-install-recommends p4lang-p4c
    

# Limpiar la caché de apt
RUN rm -rf /var/lib/apt/lists/*

# Instalar p4-utils
RUN git clone https://github.com/nsg-ethz/p4-utils.git /root/p4-utils && \
    cd /root/p4-utils && \
    pip3 install .


# Clonar repositorio de p4lang
RUN git clone https://github.com/p4lang/behavioral-model.git

# Configurar el directorio de trabajo
WORKDIR /behavioral-model/targets/simple_switch_grpc

# Copiar scripts
COPY start_s1.sh /root/
COPY start_s2.sh /root/
# RUN chmod +x /root/start_s1.sh /root/start_s2.sh 

# Exponer puertos necesarios
# EXPOSE 9090 9559

# Comando predeterminado
CMD ["/bin/bash"]

```

<p align="left">
  <img src="../imagenes/LogoUPM.png"  width="220" height="100"
</p>


# MATERIAL P4

### PROCEDIMIENTO PARA INSTALAR P4 EN UBUNTU 22.04 con codigo Fuente

### P4

Usar el repositorio correcto para Ubuntu 22.04

```
sudo nano /etc/apt/sources.list.d/home_p4lang_jammy.list


deb http://download.opensuse.org/repositories/home:/p4lang/xUbuntu_22.04/ /
```


Importa la clave GPG:
```
curl -fsSL "https://download.opensuse.org/repositories/home:/p4lang/xUbuntu_22.04/Release.key" | sudo gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/home_p4lang.gpg > /dev/null
```

actualizar repositorios

```
sudo apt update
```

## Instalar BMv2
Una vez que hayas agregado el repositorio adecuado, instala BMv2 con:
```
sudo apt install p4lang-bmv2
```

Instalar P4C
compilador oficial para programas P4, desarrollado por la comunidad P4 (P4 Language Consortium).
Transforma los programas P4 (escritos en el lenguaje de alto nivel) en configuraciones específicas para switches compatibles.
Archivo JSON: Contiene la lógica del plano de datos para ser cargada en un switch como BMv2.
```
sudo apt install p4lang-p4c 
```

Archivo P4Info: Describe las entidades P4 (tablas, acciones, etc.) para interactuar con el plano de control.

##  Graphviz
Graphviz es una herramienta para la visualización de gráficos y diagramas, utilizada para representar estructuras de datos como grafos.
Algunas herramientas y scripts de P4 generan representaciones gráficas de programas P4, como los flujos de procesamiento de paquetes o diagramas de estados del parser
Facilita la comprensión visual de la estructura de un programa P4 y su pipeline.
Necesario para:
Generar diagramas útiles en tareas de depuración y documentación del flujo de paquetes en P4.

```
sudo apt install graphviz
```

## Descarga del respositorio ‘P4-Utils’
Este repositorio incluye herramientas útiles para trabajar con P4 en Mininet. Estas herramientas simplifican la creación de topologías y el manejo de programas P4 en un entorno virtual.

```
git clone https://github.com/nsg-ethz/p4-utils.git
```

##  instalación de P4 Utils.

```
cd p4-utils/
sudo ./install.sh 
```

ibdn@ibdn-VirtualBox:~$ cd p4-utils/
ibdn@ibdn-VirtualBox:~/p4-utils$ sudo ./
docs/          examples/      install.sh     p4utils/       utils/
docsrc/        .git/          install-tools/ uninstall.sh   vm/
ibdn@ibdn-VirtualBox:~/p4-utils$ sudo ./install.sh 


## paquetes adicionales
help2man es necesario para generar las páginas de manual que el script intentó crear. Instálalo con:

```
sudo apt install help2man
```

instalar xterm para poder abrir ventanas de equipos desde mininet 
```
sudo apt install xterm
```
## instalar Wireshark

```
sudo apt install 
sudo wireshark &
```

```
p4c --target bmv2 --arch v1model --p4runtime-files basic.p4info basic.p4
```
hacen lo siguiente:

`--target bmv2`: Indica que el programa está dirigido al Behavioral Model v2 (BMv2).

`--arch v1model`: Usa el modelo de arquitectura v1model, un modelo genérico para conmutadores programables.

`--p4runtime-files basic.p4info`: Genera un archivo para ser usado con P4Runtime, que contiene la descripción de las tablas y acciones definidas en el programa P4.


## NOTAS

3. ¿Qué es gRPC y por qué cada switch tiene un puerto distinto?
gRPC (Remote Procedure Call):

Es un protocolo de comunicación que permite al controlador enviar comandos a los switches para configurar sus tablas.

Los switches BMv2 con P4Runtime exponen un puerto gRPC (como 9559, 9560) para recibir estas configuraciones.

Puertos diferentes por switch:

Cada switch debe tener un puerto único para evitar conflictos. Esto asegura que el controlador pueda identificar y comunicarse con cada switch de forma independiente.



# Iniciar
Se ejecuta el script de Python basico.py para iniciar la red en Mininet. 

```
sudo python3 basico.py
```

comprobar en mininet con los comandos.

mininet> nodes  
mininet> net  
mininet> links  





# 4.1.2. DESPLIEGUE Y CONFIGURACIÓN 

Una vez expuesto y conocido el programa con el que se va a trabajar, hay que desplegar un entorno y 
configurarlo con las herramientas expuestas anteriormente para comprobar el funcionamiento de dicho 
programa y familiarizarse con las herramientas. 
En primer lugar, en la ruta donde se encuentra el archivo del programa P4 (que como se ha comentado 
antes, se ha utilizado el directorio de p4-utils) se debe crear un archivo Python que sirva para definir y 
lanzar nuestra red en Mininet. En este caso se ha llamado basico.py. 
Posteriormente, una vez se haya creado la red en Mininet, se crea otro archivo Python en la misma ruta 
que basico.py y el programa P4. Este archivo va a servir de controlador para configurar los switches 
que componen la red y sus tablas match-action. En este caso se ha llamado controlador.py.   

## 4.1.2.1. BASICO.PY 
Este archivo se ha creado tomando de base el archivo network.py definido en el ejemplo de 
‘ip_forwarding’4 de P4-Learning. Se ha utilizado el mismo fichero base (network.py) pero con 
modificaciones para obviar funciones que no eran de interés, manteniendo la topología que se utiliza en 
el ejemplo de referencia.  

Se define la topología y se lanza una red Mininet que tiene switches que usan el programa P4 explicado 
antes. Para ello, se hace uso de la Network API perteneciente a P4 Utils y explicada en el apartado 
3.2.5.1. Con el objetivo de explicar de una manera más entendible el código, se describen los elementos 
que son necesarios para desplegar la red por pasos: 

1. Se importa la Network API. 
from p4utils.mininetlib.network_API import NetworkAPI 
2. Se declara un objeto del tipo NetworkAPI(). Emula al objeto Mininet(). 
net = NetworkAPI() 
3. Sabiendo que se implementa la posibilidad de establecer el nivel de detalle de los ‘log’, se 
establece el nivel ‘info’ que en este caso nos va a resultar de interés.  
net.setLogLevel('info') 
4. La topología utilizada está representada en la Figura 18. 
4https://github.com/nsg-ethz/p4-learning/blob/master/examples/ip_forwarding/network.py 


Partiendo de la topología de este escenario, se añaden los nodos a la red y sus conexiones. En 
este caso, como se quiere trabajar con P4Runtime, se definen P4RuntimeSwitches. Además, 
las IPs asignadas se corresponden con el método de autoasignado mixed(), es decir, las 
direcciones de los hosts se asignan de forma que pertenecen a la misma subred del switch al 
que están conectados. 
Para añadir los switches se hace uso del método addP4RuntimeSwitch(‘sX’). Ejemplo: 
net.addP4RuntimeSwitch('s1') 
Para añadir los hosts se hace uso del método addHost (‘hX’). Ejemplo: 
net.addHost ('h1') 
Para añadir los links se utiliza el método addLink (‘nX,nY’), para un enlace entre los nodos nX 
y nY (que pueden ser hosts o switches). El puerto (interfaz de red) de cada nodo se asigna de 
menor a mayor (1<2<3…) conforme se declaran los enlaces. Ejemplo: 
net.addLink('h1', 's1') 
Para establecer el autoasignado se llama al método mixed(): 
net.mixed() 
5. Se habilita en todos los switches de la red la creación de logs y la captura de los paquetes de 
red y su almacenamiento en archivos ‘.pcap’. 
net.enablePcapDumpAll() 
net.enableLogAll() 
6. Por último, queda habilitar el CLI (Command Line Interface) de Mininet e iniciar la red. 
net.enableCli() 
net.startNetwork() 






# Reference

* [p4.org - P4_16 Spec - v1.0.0](https://p4.org/p4-spec/docs/P4-16-v1.0.0-spec.html)
* [p4.org - P4 PSA Spec - v1.0.0](https://p4.org/p4-spec/docs/PSA-v1.0.0.html)
    * [v1model.p4](https://github.com/p4lang/p4c/blob/master/p4include/v1model.p4)
    * [psa.p4](https://github.com/p4lang/p4c/blob/master/p4include/psa.p4)
* [p4.org - P4Runtime Spec - v1.0.0](https://p4.org/p4-spec/docs/P4Runtime-v1.0.0.pdf)
    * [v1/p4runtime.proto](https://github.com/p4lang/p4runtime/blob/master/proto/p4/v1/p4runtime.proto)
    * [v1/p4data.proto](https://github.com/p4lang/p4runtime/blob/master/proto/p4/v1/p4data.proto)
    * [config/v1/p4info.proto](https://github.com/p4lang/p4runtime/blob/master/proto/p4/config/v1/p4info.proto)
    * [config/v1/p4types.proto](https://github.com/p4lang/p4runtime/blob/master/proto/p4/config/v1/p4types.proto)
* [p4.org - In-band Network Telemetry(INT) Dataplane Specification](https://github.com/p4lang/p4-applications/blob/master/docs/INT.pdf)
* [p4.org - Telemetry Report Format Specification](https://github.com/p4lang/p4-applications/blob/master/docs/telemetry_report.pdf)
* [p4lang/tutorials](https://github.com/p4lang/tutorials)
* [p4lang/p4factory/apps/int](https://github.com/p4lang/p4factory/tree/master/apps/int)

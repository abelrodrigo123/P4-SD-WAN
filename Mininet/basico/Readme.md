# Instrucciones


Basicamente solo se requiere de 3 pasos.
- Crear escenario:  sudo python3 basico.py 
- Poblar tablas: sudo python3 controlador.py 
- Realizar pruebas de conectividad.


1. Se ejecuta el script de Python basico.py para iniciar la red en Mininet. 

```python
sudo python3 basico.py 

```
Tras ejecutar en el terminal el comando, aparecen unos mensajes de seguimiento de la creación 
y configuración de la red establecida en basico.py. Tras ellos, aparece el cliente de Mininet que 
permite trabajar en el entorno creado. Además, se comprueba la ruta sobre la que se ha trabajado 
y se ha generado un archivo ‘topology.json’ en el que se recoge la topología creada.

```python
mininet> nodes  
mininet> net  
mininet> links  
```
3. Ya con el entorno iniciado y en el cliente de Mininet, se comprueba el comportamiento de la 
red al iniciar un pingall, comando que realiza un ping desde cada host a todos los demás hosts 
en la red, verificando si pueden alcanzarse mutuamente.

```python
mininet> pingall 

```
El resultado obtenido en este punto es que ninguno de los hosts es alcanzable por ningún otro 
tal y como se muestra.

Con el objetivo de hacer llegar los paquetes a su destino, se carga el programa P4 basico.p4 y se rellenan 
las tablas de flujo de los switches. Para ello, se hace uso del script de Python descrito anteriormente: 
controlador.py. Sin embargo, antes de ejecutar el script es necesario obtener el archivo P4Info y el de 
configuración del target. Estos archivos se obtienen mediante la compilación del programa P4. 
4. Se compila el programa. Desde un nuevo terminal en la ruta donde se encuentran el programa 
P4 y los scripts desarrollados previamente, el programa se ha compilado con la herramienta 
P4C mediante el comando: 

```python
 p4c --target bmv2 --arch v1model --p4runtime-files basico_p4rt.txt basico.p4

```

Se pasan como argumentos el target bmv2, el modelo de arquitectura V1Model y se habilita la 
opción de generar el archivo P4Info, llamándolo basico_p4rt.txt. Es importante que el nombre 
del archivo P4Info generado sea el mismo que el establecido en la declaración del controlador 
en controlador.py. Los archivos generados se guardan en la misma ruta tal y como se observa 
en la Figura 10, expuesta anteriormente en el apartado 3.2.4. 
5. Se inicia en Wireshark una captura de tráfico en la interfaz de ‘Loopback’ y posteriormente se 
ejecuta el script de Python controlador.py para configurar el plano de datos. 

```python
sudo python3 controlador.py
```

Tras esto, el programa se ha cargado en los switches y las tablas de flujos se han rellenado con 
las normas definidas. En la salida de la ejecución del script se ve las entradas que se introducen 
en los switches (un extracto se muestra en la Figura 21). 


6. Se comprueba que ahora los hosts se alcanzan unos a otros: 

```python
mininet> pingall 

```
El resultado ahora, como se observa en la Figura 23, es que no se pierde ningún paquete y hay 
conectividad entre todos los hosts. 

También se comprueba la conectividad mediante el comando netcat a través de una conexión 
TCP. Para ello, primero se lanzaron dos consolas de dos hosts, por ejemplo, ‘h1’ y ‘h2’. 

```python
mininet> xterm h1 h2 

```
Una vez se han desplegado las dos consolas, en la consola de ‘h2’ se arrancó un servidor en 
escucha (-l) y se establece un puerto (-p). 

```python
(h2) root@mario-VirtualBOX:~/basico# nc -l -p 12345 

```
Con el servidor en ‘h2’ en escucha, en la consola de ‘h1’ se manda un mensaje hacia ‘h2’. 

```python
(h1) root@mario-VirtualBOX:~/basico# echo “Esto es una prueba” | nc 10.0.2.2 13245 

```
El resultado es el observado en la Figura 24: el mensaje enviado “Esto es una prueba” aparece 
en la consola de ‘h2’, verificando la conexión entre ambos hosts. Se podría realizar el mismo 
procedimiento para cada par de hosts o usar otras aplicaciones entre ellos. 

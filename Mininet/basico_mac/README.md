# P4 BMv2 y creación de MAC manual.


Se creó las direccion MAC de forma manual y asignadas al host, Sw y enlace de tal forma que se pueda utilizar en el enrutamiento.

Se tiene que definir en la creación de la red, ello se tiene que definir al momento de crear la red y también aplica para la modificación de hoy ya creados.
Es importante mencionar que cada nodo que se crea (host, sw) obtiene un ID correlativo que se usa para determinar su dirección MAC mediante el método elegido.
Para crear un nodo con un ID específico, es necesario indicarlo al momento de crearlo



```python
# Asignar dirección MAC a h21 después de crearlo
#MAC DE H21
net.setIntfMac('h21', 's21', '00:00:00:00:21:01')
# MAC en s21 conectada a h21 
net.setIntfMac('s21', 'h21', '00:00:0a:00:21:00')

# MAC en s21 para el enlace a s3
net.setIntfMac('s21', 's3', '00:00:0a:03:21:00') 
```



##Crear Sw y cambiar su ID de forma manual, de lo contratrio es correlativo el orden.

```
net.addP4RuntimeSwitch('s21', device_id=21)
```
Luego esta información debera de guardar correlación con el archivo controlador.py que se encarga de la configuracion de los Sw.


```python
#### S21 #####
controller = SimpleSwitchP4RuntimeAPI(device_id=21, grpc_port=9562,
                                      p4rt_path='basico_p4rt.txt',
                                      json_path='basico.json')

#controller.table_clear('ipv4_lpm')
controller.table_set_default('ipv4_lpm','drop')
controller.table_add('ipv4_lpm', 'ipv4_forward',['10.0.21.1/24'], ['00:00:00:00:21:01','1'])
controller.table_add('ipv4_lpm', 'ipv4_forward',['10.0.3.0/24'], ['00:00:0a:03:21:00','2'])

```

## Importante
- Revisar que este escrito correctamente, ya que un error de digitación de un comando puede hacer fallar y no se muestra en el despliegue.
- Una vez añadidos los registros de las tablas con network.py, no se puede volver a ejecutar para realizar una modificacion y ello se debe a que tiene el comando `table_add` y se tiene que cambiar por `table_modify_match`, por ello se creó un nuevo archivo para actualizar las tablas sin necesidad de destruir todo el escenario de mininet y volver a ejecutar todos los comandos.
- La máscara para los host se tiene que establecer en /32, porque si se usa /24, solo el primer equipo responde y los demas no tienen comunicacion, en mi caso cree h21 y h22 con /24 y solo h21 tenia comunicación por la mask.
- host /32
- Red destino /24



```python
#controller.table_clear('ipv4_lpm')
controller.table_set_default('ipv4_lpm','drop')
controller.table_add('ipv4_lpm', 'ipv4_forward',['10.0.21.21/32'], ['00:00:00:00:21:01','1'])
controller.table_add('ipv4_lpm', 'ipv4_forward',['10.0.21.22/32'], ['00:00:00:00:21:02','2'])
controller.table_add('ipv4_lpm', 'ipv4_forward',['10.0.3.0/24'], ['00:00:0a:03:21:00','3'])
controller.table_add('ipv4_lpm', 'ipv4_forward',['10.0.1.0/24'],['00:00:0a:03:21:00', '3'])
#controller.table_add('ipv4_lpm', 'ipv4_forward',['10.0.1.0/24'], ['00:00:0a:00:03:00','3']) tiene error de MAC y funciona.


```

Al revisar los logs en s1 de la comunicacion entre h1 y h22, se observa un campo de la direccion ip en hexadecimal.

La referencia `hdr.ipv4.dstAddr : 0a001516` en los logs de red se refiere a la dirección de destino IPv4 del paquete que está siendo procesado. Aquí tienes una explicación detallada:

Desglose de hdr.ipv4.dstAddr : 0a001516
`hdr.ipv4.dstAddr`:

Este campo representa la dirección de destino IPv4 del paquete. En el contexto de los logs, hdr se refiere al encabezado del paquete, ipv4 indica que es un paquete IPv4, y dstAddr es la dirección de destino.
`0a001516`:

Este valor es la dirección IPv4 de destino en formato hexadecimal. Para convertirlo a una dirección IPv4 legible, puedes dividirlo en octetos y convertir cada parte de hexadecimal a decimal.
Conversión de Hexadecimal a Decimal
Para convertir 0a001516 a una dirección IPv4 legible:

Dividir en octetos:

- 0a -> 10
- 00 -> 0
- 15 -> 21
- 16 -> 22

La dirección IPv4 correspondiente es 10.0.21.22.

Contexto en los Logs

En los logs, este campo se utiliza para buscar coincidencias en las tablas de flujo y determinar la acción a tomar para el paquete. 


```python
[13:59:07.741] [bmv2] [D] [thread 26206] [42.0] [cxt 0] Looking up key:
* hdr.ipv4.dstAddr    : 0a001516
El switch está buscando la dirección de destino 10.0.21.22 en la tabla de flujo MyIngress.ipv4_lpm para determinar la acción a tomar.

```
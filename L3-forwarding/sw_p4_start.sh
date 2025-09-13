#!/bin/bash
#Ejecutar proceso de inicio de los Switch de forma remota.
#En en VNX se define la copia del script para ejecutarlo de forma remota.
#s1 y s2 son los nombres definidos en VNX

# lxc-attach -n s1 -- /root/start_s1.sh
# lxc-attach -n s2 -- /root/start_s2.sh


#!/bin/bash
#Ejecutar proceso de inicio de los Switch de forma remota.
#En en VNX se define la copia del script para ejecutarlo de forma remota.
#s1 y s2 son los nombres definidos en VNX


# brindar permisos de ejecucion al script en cada switch
sudo lxc-attach -n s1 -- chmod +x /root/start_s1.sh
sudo lxc-attach -n s2 -- chmod +x /root/start_s2.sh

#inicar la sesion en cada switch.
sudo lxc-attach -n s2 -- tmux new-session -d -s switch1 "/root/start_s2.sh"
sudo lxc-attach -n s1 -- tmux new-session -d -s switch2 "/root/start_s1.sh"

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

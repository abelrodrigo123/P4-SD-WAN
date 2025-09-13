
<p align="left">
  <img src="imagenes/LogoUPM.png"  width="220" height="100"
</p>



# Diseño e integración de un plano de datos programable mediante P4 para servicios SD-WAN

Este repositorio contiene el desarrollo completo del Trabajo Fin de Máster (TFM) presentado en la **Escuela Técnica Superior de Ingenieros de Telecomunicación** de la **Universidad Politécnica de Madrid (UPM)**, en el marco del **Máster Universitario en Ingeniería de Redes y Servicios Telemáticos (MUIRST)**.

El trabajo aborda la instalación, configuración e integración de BMv2 en contenedores LXC, incluyendo la modificación de imágenes rootfs, el uso de herramientas como tmux, y la interacción con controladores basados en P4Runtime y p4-utils, que se ejecutan directamente en el host. Además, se realiza una comparativa técnica entre el uso de imágenes LXC y Docker para BMv2, justificando la elección de LXC en función de la compatibilidad con VNX y la eficiencia en entornos virtualizados.

El TFM incluye el diseño de varios escenarios de red programables, como capa 2, encaminamiento L3, selección de caminos basada en puertos TCP, y pruebas de conectividad entre hosts, todo ello documentado con scripts, topologías en formato XML y JSON, y programas P4 personalizados. También se ha reorganizado el contenido para facilitar la comprensión, trasladando secciones como Mininet al anexo y centrando el capítulo principal en la integración de BMv2 con VNX y LXC.

Este repositorio está pensado como guía práctica y técnica para estudiantes e investigadores interesados en redes definidas por software (SDN), y el uso de P4 en entornos académicos y experimentales.



---

## 🎯 Objetivos del proyecto

- Validar la viabilidad técnica de construir escenarios funcionales de red programables.
- Implementar reenvío de paquetes en Capa 2 (Ethernet), Capa 3 (IP) y lógica de selección de rutas en SD-WAN.
- Automatizar el despliegue de switches BMv2 en contenedores LXC integrados con VNX.
- Configurar dinámicamente el plano de datos mediante **P4Runtime** y scripts en Python.
- Comparar métodos de instalación de BMv2 (repositorio, compilación, Docker).
- Documentar el entorno experimental para su reutilización académica.

---

## 🧰 Tecnologías utilizadas

- **P4** — Lenguaje para programación del plano de datos.
- **BMv2** — Behavioral Model v2, switch software compatible con P4.
- **VNX** — Virtual Network eXperimenter para definición de topologías.
- **LXC** — Contenedores Linux para virtualización ligera.
- **P4Runtime** — API para configuración dinámica del plano de datos.
- **tmux** — Multiplexor de terminal para automatización.
- **Mininet** — Plataforma de emulación utilizada en fases exploratorias.

---

## 📁 Estructura del repositorio

Haz clic en cada carpeta para acceder a su contenido específico:

- [**behavioral-model**](behavioral-model) — Código fuente de BMv2
- [**Dockerfile**](Dockerfile-P4-BMv2) — Dockerfile para BMv2 (comparativa)
- [**L2-forwarding**](L2-forwarding) — Escenario de Capa 2
- [**L3-forwarding**](L3-forwarding) — Escenario de Capa 3
- [**L4-SDWAN**](L4-SDWAN) — Escenario SD-WAN (Capa 4)
- [**Mininet**](Mininet) — Escenario exploratorio con Mininet


---

## 🖥️ Escenarios implementados

Cada carpeta contiene su propio `README.md` con:

- Descripción del escenario
- Topología utilizada
- Programa P4 implementado
- Scripts de arranque y configuración
- Pruebas realizadas y resultados

---

## 📄 Resumen técnico

Este TFM propone una arquitectura modular y reproducible para redes programables, basada en:

- Instalación de BMv2 en contenedores LXC.
- Definición de topologías en VNX mediante XML.
- Automatización con tmux y scripts de inicialización.
- Programas P4 para reenvío Ethernet, IP y selección de rutas por puerto TCP/UDP.
- Validación con herramientas como ping, tcpdump, CLI de BMv2 y análisis de logs.

---




## 👨‍🏫 Tutor académico

**Luis Bellido Triana**

---



## 🎓 Autor

**Abel Hammer Rodrigo Saavedra**  
*Universidad Politécnica de Madrid*  
✉️ [abel.rodrigo@alumnos.upm.es](mailto:abel.rodrigo@alumnos.upm.es)


---


## 📅 Año académico

**2025**

---

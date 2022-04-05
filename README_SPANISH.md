# Pandora Box

Pandora Box es una aplicación escrita en Python 3 para penetrar en redes inalámbricas y recolectar información sobre dispositivos conectados. Esta aplicación se puede utilizar por sí misma o como parte de un sistema de tres aplicaciones.

## Requerimientos
Este software fue desarrollado para Kali Linux 2020.
### Hardware
Se necesitarán de dos a tres interfaces de red. Una para llevar a cabo ataques a la red, otra para deautenticar cuando se lleva a cabo un ataque Evil Twin y la tercera para conectarse a internet. 

- Tarjeta de red inalámbrica con modo Monitor e inyección de paquetes para llevar a cabo ataques en la red inalámbrica.
- Tarjeta de red inalámbrica con modo Master para establecer un punto de acceso para el ataque de Evil Twin.
- Cualquier interfaz de red con coneción a internet excepto tarjeta de red inalámbrica (puede ser cableada, módulo 3G, etc)

### Software
- python >3.6
- iwconfig
- ifconfig
- iptables
- aircrack-ng
- dsniff
- cowpatty
- tshark
- nmap
- dnsmasq
- reaver
- hostapd

### Dependencias de Python
- schedule==0.6.0
- Flask==1.1.2

## Instalación
Para instalar el software y sus dependencias primero es necesario iniciar sesión como usuario root.

Clonar el repositorio.
```sh
git clone https://gitlab.com/acolazo/pi169
```

Se pueden instalar las dependencias de software manualmente via apt o usando el script automatizado.
```bash
chmod +x install.sh
./install.sh
```

Luego, correr el siguinte script el cuál configurará archivos necesarios en el directorio. 
```sh
chmod +x quickstart.sh
./quickstart.sh
```

Finalmente, usar el administrador de paquetes [pip](https://pip.pypa.io/en/stable/) para instalar las dependencias de Python.
```sh
pip install -r requirements.txt
```

## Configuración
Antes de ejecutar el software es necesario configurar algunos parámetros. Estos parámetros pueden ser encontrados en el archivo pandora/config.py.
El archivo tiene comentarios que guiarán al usuario en la configuración de estos parámetros.

## Uso
NOTA: Para usar esta aplicación hay que estar usando el usuario root.

### Modo Discovery
Este modo escaneará pasivamente. Escaneará las redes y estaciones cercanas y guardará estos datos.

```sh
python -m pandora -m discovery wlan0
```
Esta etapa se ejecutará hasta que el usuario interrumpa la ejecución. Se generarán archivos de forma periódica que se guardrán en la carpeta "logs/airodump". 
Si el parámetro UPLOAD es True estos archivos serán cargados al servidor (ver SAD) y luego borrados del sistema de archivos.

### Modo Intrusion
Este modo es para obtener la contraseña de una red inalámbrica protegida.
Hay tres comandos posibles para ejecutar.

El primer comando es para llevar un ataque automatizado que detectará el protocolo de seguridad de la red y elegirá el ataque adecuado de acuerdo con esta información.

Los ataques posibles son:
- WPS Pixie Dust
- WEP Fake Auth
- WPA Handshake y Cracking en línea usando [Online Hash Crack](https://www.onlinehashcrack.com/)

```bash
python -m pandora -m intrusion wlan0
```

El segundo comando ejecuta un Evil Twin.
```sh
python -m pandora -m intrusion wlan0 -et
```

El tercer comando ejecuta un Evil Twin y un ataque de deautenticación al punto de acceso que se replica.
```sh
python -m pandora -m intrusion wlan0 -et -it2 wlan1
```

El progama terminará cuando haya obtenido o fallado en obtener la contraseña. En caso de ser exitoso la contraseña será guardada en la carpeta "passwords"

### Modo Recollect
Para este modo el dispositivo debe estar conectado a la red. Lleva a cabo detección de sistema operativo y un ataque de hombre en el medio para interceptar tráfico.

```sh
python -m pandora -m recollect wlan0
```
Esta etapa se ejecutará hasta que el usuario interrumpa la ejecución.
Una vez detectado el sistema operativo de los objetivos se guardarán los archivos correspondientes en la carpeta "logs/nmap".
La información de los paquetes interceptados del objetivo se guardará en varios archivos en la carpeta "logs/httpreqs".
Si el parámetro UPLOAD es True estos archivos serán cargados al servidor (ver SAD) y luego borrados del sistema de archivos.

### Modo Deauth 
Para este modo el dispositivo no necesta conexión a la red objetivo.
Lleva a cabo un ataque de deautenticación a un punto de acceso en un momento particular, el cuál es pasado como argumento.
```sh
python -m pandora -m deauth wlan0 -tmac AA:AA:AA:AA:AA:AA -dt 31/12/20-18:00
```
No se generan archivos.

## Cargar los archivos a un servidor distinto.
Se puede modificar el archivo upload.py para cargar los datos a un servidor con distinta API o usar protocolos distintos.
La única función requerida es upload() la cuál es llamada desde el main.

## Usar un servicio de cracking en línea distinto
Puede modificar el método online_wpa_crack de la clase Aircrack (que se encuentra en el archivo aircrack.py) para utilizar un servicio distinto.

## See also

**SAD**

**SAVI**

## Disclaimer
Pandora Box ha sido hecho para asistir en penetration testing e investigaciones judiciales. Esta desarrollado para ser utilizado en un marco legal por personal autorizado. No somos responsables por el mal uso o el uso ilegal de este software.

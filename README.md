# Pandora Box

Pandora Box is an application written on Python 3 for intruding networks and recollecting information on connected devices. You can use this application alone but it is part of a system formed with three applications.

## Requirements
This software was developed for Kali Linux 2020.
### Hardware
You will need from two to three network interfaces. One to perform network attacks, one to deauthenticate when performing an Evil Twin attack and the third one to upload data to the server.

- A wireless card with Monitor Mode and packet injection for performing wireless attacks.
- A wireless card with Master Mode to establish an access point for the Evil Twin attack. 
- Any network interface with internet connection except wifi (wired, 3G).

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

### Required Python packages
- schedule==0.6.0
- Flask==1.1.2

## Installation
For installing the software and dependencies first log in as root.

Clone the repository.
```sh
git clone https://gitlab.com/acolazo/pi169
```

You can install software dependencies manually via apt or use the automated script.
```bash
chmod +x install.sh
./install.sh
```

Then run the next script which will configure files in the directory.
```sh
chmod +x quickstart.sh
./quickstart.sh
```

Finally, use the package manager [pip](https://pip.pypa.io/en/stable/) to install python dependencies.

```sh
pip install -r requirements.txt
```

## Configuration
Before running the software it is required to configure some parameters. Those parameters can be found in the file pandora/config.py.
The file has comments that will guide you in configuring the parameters.

## Usage
NOTE: To use this application you must be logged in as root.

### Mode Discovery
This mode will passively scan. It will scan nearby networks and stations and save this data.
If the parameter UPLOAD is True the data will be sent to the server.

```sh
python -m pandora -m discovery wlan0
```
### Mode Intrusion
This mode is for performing a cracking attack on a wireless access point.
There are 3 possible commands in this mode.

The first command will perform an automated attack that will detect the network protocol and choose an attack according to this information.

The possible attacks are:
- WPS Pixie Dust
- WEP Fake Auth
- WPA Handshake and Online Cracking with [Online Hash Crack](https://www.onlinehashcrack.com/)

```bash
python -m pandora -m intrusion wlan0
```

 The second command performs an Evil Twin.
```sh
python -m pandora -m intrusion wlan0 -et
```

The third command performs an Evil Twin and Deauth attack.
```sh
python -m pandora -m intrusion wlan0 -et -it2 wlan1
```

### Mode Recollect
For this mode the device has to be connected to the network. It performs OS detection and a MITM attack to intercept traffic.
If the parameter UPLOAD is True the data will be sent to the server.
```sh
python -m pandora -m recollect wlan0
```

### Mode Deauth
For this mode the device doesn't need connection to the target network.
It performs a deauth attack to an access point at a particular time that is passed as an argument.
```sh
python -m pandora -m deauth wlan0 -tmac AA:AA:AA:AA:AA:AA -dt 31/12/20-18:00
```
## Uploading files to a different server
You can modify the file upload.py to suit your needs.
The only required function is upload() which is called by the main.

## Using a different cracking online service
You can modify the method online_wpa_crack of the class Aircrack in the file aircrack.py to suit your needs.

## See also

**SAD**

**SAVI**

## Disclaimer
Pandora is created to assist in penetration testing and legal investigations. It is meant to be used in a legal frame. We are not responsible for any misuse.

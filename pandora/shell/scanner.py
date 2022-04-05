# import os
# import time
# from subprocess import Popen, PIPE, STDOUT
# import subprocess

import nmap
#import types

class Scanner:
    def __init__(self):
        self.portscanner = nmap.PortScanner()

    def scan_hosts(self, network, sudo=False):
        self.portscanner.scan(hosts=network, arguments='-sN', sudo=sudo)

    def get_hosts(self):
        # try:
        #     targets.remove(get_ip_address)
        # except ValueError:
        #     pass
        return self.portscanner.all_hosts()

    def scan_open_ports(self, target_ip, target_ports, sudo=False):
        if target_ports is None:
            target_ports = '-'
        self.portscanner.scan(target_ip, ports=target_ports, arguments='', sudo=sudo)

    def get_open_ports(self, target_ip):
        # ports = types.SimpleNamespace()
        # ports.tcp = nm[target_ip].all_tcp()
        # ports.udp = nm[target_ip].all_udp()
        all_tcp = self.portscanner[target_ip].all_tcp()
        all_udp = self.portscanner[target_ip].all_udp()
        open_ports = {'tcp': all_tcp, 'udp': all_udp}
        return open_ports

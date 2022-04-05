import re
import os
from pandora.utils.program import ProgramBase
from pandora.definitions import NMAP_PATH

class Nmap(ProgramBase):
    program = 'nmap'
    def __init__(self, dirpath=NMAP_PATH):
        super().__init__()
        self.dirpath = dirpath
        self.prefix = 'nmapos'

    def discover_hosts(self, subnet, ifname):
        """Subnet parameter should be ipv4/mask. Returns dict {ipv4: mac} for all IP addresses detected in a subnetwork. If the MAC address cant be detected the entry is {ipv4: None}"""
        ip_mac_dict = {}
        ip_with_no_mac = False
        command = [self.program, '-sP', '--disable-arp-ping', subnet, '-e', ifname]
        output = self.__execute_nmap(command)
        #parse output
        pattern = re.compile(r'(\d+\.\d+\.\d+\.\d+)|(..:..:..:..:..:..)')
        ip_pattern = re.compile(r'\d+\.\d+\.\d+\.\d+')
        mac_pattern = re.compile(r'..:..:..:..:..:..')
        matches = pattern.finditer(output)
        for match in matches:
            string = match.group(0)
            if ip_pattern.match(string):
                if ip_with_no_mac:
                    ip_mac_dict.update({ipv4: None})
                ipv4 = string
                ip_with_no_mac = True
            elif mac_pattern.match(string):
                mac = string
                ip_mac_dict.update({ipv4: mac})
                ip_with_no_mac = False
        #For last element.
        if ip_with_no_mac:
            ip_mac_dict.update({ipv4: None})
        return ip_mac_dict

    def discover_hosts_key_mac(self, subnet, ifname):
        """Subnet parameter should be ipv4/mask. Return dict {mac: ipv4} for all hosts detected in a subnetwork."""
        command = [self.program, '-sP', '--disable-arp-ping', subnet, '-e', ifname]
        output = self.__execute_nmap(command)
        return self._parse_key_mac(output)
        
    def _parse_key_mac(self, output):
        mac_ip_dict = {}
        pattern = re.compile(r'(\d+\.\d+\.\d+\.\d+)|(..:..:..:..:..:..)')
        ip_pattern = re.compile(r'\d+\.\d+\.\d+\.\d+')
        mac_pattern = re.compile(r'..:..:..:..:..:..')
        matches = pattern.finditer(output)
        for match in matches:
            string = match.group(0)
            if ip_pattern.match(string):
                ipv4 = string
            elif mac_pattern.match(string):
                mac = string
                mac_ip_dict.update({mac: ipv4})
        return mac_ip_dict



    def __execute_nmap(self, command):
        outerr = self.pcaller.runread(command)
        return outerr[0]

    def save_os(self, host, ifname):
        verbosity = '-vv'
        filename = self.prefix + host
        filepath = os.path.join(self.dirpath, filename)
        cmd = [self.program, '-O', host, '-oX', filepath, verbosity, '-e', ifname]
        self.pcaller.runwait(cmd)

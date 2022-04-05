import csv
import re
import os
from pandora.definitions import TEMP_PATH
from pandora.utils.program import ProgramBase
from pandora.utils.exceptions import TargetAPNotFoundError

class Airodump(ProgramBase):
    program = 'airodump-ng'
    def __init__(self, prefix='temp_airodump', dirpath=TEMP_PATH):
        super().__init__()
        self.prefix = prefix
        self.dirpath = dirpath
        self.accps = None
        self.stations = None

    def clean_directory(self):
        pattern = re.compile(self.prefix + r'(-\d+)?.(csv|ivs)')
        filenames = os.listdir(self.dirpath)
        filenames = ' '.join(filenames)
        matches = pattern.finditer(filenames)
        for match in matches:
            absolute_path = os.path.join(self.dirpath, match.group(0))
            if os.path.exists(absolute_path):
                os.remove(absolute_path)
                print(f"Deleting file {absolute_path}")

    def parse_csv(self):
        #Create data structures with the first file that matched if it exists, else return empty lists
        keys = []
        accp = {}
        station = {}
        stations = []
        accps = []
        #files = []
        #Find files in directory and filter with prefix pattern.
        pattern = re.compile(self.prefix + r'(-\d+)?.csv')
        filenames = os.listdir(self.dirpath)
        filenames = ' '.join(filenames)
        matches = pattern.finditer(filenames)
        for match in matches:
            if os.path.isfile(os.path.join(self.dirpath, match.group(0))):
                filename = match.group(0)
                break
                #files.append(match.group(0))

        #Create data structures with the first file that matched if it exists, else return empty lists
        if filename:
            filename = os.path.join(self.dirpath, filename)
            with open(filename, mode='r', newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',', skipinitialspace=True)
                for row in reader:
                    if len(row) <= 1:
                        continue

                    elif row[0] == 'BSSID':
                        for element in row:
                            keys.append(element.strip())
                    elif row[0] == 'Station MAC':
                        keys.clear()
                        for element in row:
                            keys.append(element.strip())
                    elif keys[0] == 'BSSID':
                        #15
                        accp = {}
                        row_essid = row[13:-1]
                        row_key = row[-1]
                        row_rest = row[0:13]
                        for idx, element in enumerate(row_rest):
                            accp.update({keys[idx]: element.strip()})
                        accp.update({keys[13]: ",".join(row_essid).strip()})
                        accp.update({keys[14]: row_key})
                        accps.append(accp)
                    else: #iterating stations
                        #7
                        station = {}
                        row_essid = row[6:]
                        row_rest = row[0:6]
                        for idx, element in enumerate(row_rest):
                            station.update({keys[idx]: element.strip()})
                        station.update({keys[6]: ",".join(row_essid).strip()})
                        stations.append(station)
        return (accps, stations)

    def set_accps(self, accps):
        self.accps = accps
    
    def set_stations(self, stations):
        self.stations = stations

    def save_airodump(self, interface, timeout):
        file_path = os.path.join(self.dirpath, self.prefix)
        #command = f'timeout 10 {self.program_call} -i {interface} --write {self.prefix} --output-format csv --write-interval 1'
        cmd = [Airodump.program, '-i', interface, '--write', file_path, '--output-format', 'csv', '--write-interval', '1']
        print(f"Running {cmd}")
        self.pcaller.runwait(cmd, timeout=timeout)

    def get_airodump(self, interface, timeout):
        self.clean_directory()
        self.save_airodump(interface, timeout)
        access_points, stations = self.parse_csv()
        self.set_accps(access_points)
        self.set_stations(stations)
        return access_points, stations

    def capture_airodump_network(self, interface, network, filename):
        file_path = os.path.join(self.dirpath, filename)
        cmd = [Airodump.program, '-c', network.get('channel'), '--bssid', network.get('BSSID'), '-o', 'pcap', '-w', file_path, interface]
        proc = self.pcaller.executeretnull(cmd)
        return proc

    # def save_pcap_handshake(self, interface, timeout, network):
    #     pid = self.capture_airodump_network(interface, network, 'nico')
    #     time.sleep(timeout)
    #     pid.kill()

    def get_target_ap_by_bssid(self, target_bssid):
        target_ap = None
        for access_point in self.accps:
            target_ap = access_point if access_point.get('BSSID') == target_bssid else target_ap
        if target_ap is None:
            raise TargetAPNotFoundError
        return target_ap

    def get_target_ap(self, target_ssid):
        target_ap = None
        power = float('-inf')
        if target_ssid == '':
            for access_point in self.accps:
                if access_point.get("Power") > power:
                    target_ap = access_point
                    power = access_point.get("Power")
        else:
            for access_point in self.accps:
                target_ap = access_point if access_point.get('ESSID') == target_ssid else target_ap
        if target_ap is None:
            raise TargetAPNotFoundError
        return target_ap

    def get_connected_hosts(self, target_bssid):
        connected_hosts = []
        for host in self.stations:
            print(host)
            if host.get('BSSID') == target_bssid:
                connected_hosts.append(host)
        return connected_hosts

    def get_ap_channel(self, target_ap_bssid):
        accp = self.get_target_ap_by_bssid(target_ap_bssid)
        if accp:
            return accp.get('channel')


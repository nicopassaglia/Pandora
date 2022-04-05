import os
from pandora.utils.program import ProgramBase


class Iptables(ProgramBase):
    program = 'iptables'

    def command_for_twin(self, interface):
        print("Executing IP TABLES commands")
        os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
        os.system("sudo iptables --flush")
        os.system("sudo iptables --append FORWARD --in-interface "+interface+" -j ACCEPT")
        os.system("sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination 10.0.0.1:80")
        os.system("sudo iptables -t nat -A POSTROUTING -j MASQUERADE")

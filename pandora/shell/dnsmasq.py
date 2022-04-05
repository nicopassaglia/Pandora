import os
from pandora.utils.program import ProgramBase
from pandora.definitions import CONF_PATH


class Dnsmasq(ProgramBase):
    program = 'dnsmasq'
    conf_file_path = os.path.join(CONF_PATH, 'dnsmasq.conf')

    def create_conf_file(self, interface):
        conf_file = open(self.conf_file_path, 'w+')
        conf_file.write("interface=" + interface+"\n")
        conf_file.write("dhcp-range=10.0.0.10,10.0.0.250,255.255.255.0,12h"+"\n")
        conf_file.write("dhcp-option=3,10.0.0.1"+"\n")  # 3 is code for default gateway
        conf_file.write("dhcp-option=6,10.0.0.1"+"\n")  # 6 for DNS Server
        conf_file.write("server=8.8.8.8"+"\n")
        conf_file.write("log-queries"+"\n")
        conf_file.write("listen-address=127.0.0.1"+"\n")
        conf_file.close()

    def start(self, interface):
        Dnsmasq.create_conf_file(self, interface)

        os.system("ifconfig "+interface+" up 10.0.0.1 netmask 255.255.255.0")
        os.system("route add -net 10.0.0.0 netmask 255.255.255.0 gw 10.0.0.1")
        os.system("a2enmod rewrite")
        os.system("chmod -R 775 /var/www/html/")
        os.system("service apache2 restart")

        cmd = [Dnsmasq.program, "-C", self.conf_file_path, "-d"]  # -d: daemon

        return self.pcaller.executeret(cmd)

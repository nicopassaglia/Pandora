from pandora.utils.program import ProgramBase
from pandora.config import TARGET_SSID

class Airbase(ProgramBase):
    program = 'airbase-ng'

    def start(self, interface):
        cmd = [self.program, '-e', TARGET_SSID+'-Update2', '-c', '6', interface ]
        return self.pcaller.executeret(cmd)
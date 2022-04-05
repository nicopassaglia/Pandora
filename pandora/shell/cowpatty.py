from pandora.utils.program import ProgramBase


class Cowpatty(ProgramBase):
    program = 'cowpatty'

    def check_wpa_handshake(self, file_path):
        cmd = [self.program, '-c', '-r', file_path]
        out = self.pcaller.runread(cmd, None)
        return out[0]

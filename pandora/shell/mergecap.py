import os
from pandora.utils.program import ProgramBase
from pandora.utils.httpreq import post
from pandora.definitions import TEMP_PATH
from pandora.config import TIMEOUT_WPA, TIMEOUT_WEP, WPA_ONLINE_MAIL


class Mergecap(ProgramBase):
    program = 'mergecap'

    def concatenate(self, outfile, infile1):
        cmd = [self.program, infile1, '-w', outfile]

        outerr = self.pcaller.runread(cmd)
        return outerr[0]

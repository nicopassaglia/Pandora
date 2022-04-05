import os
from pandora.utils.program import ProgramBase
from pandora.config import TIMEOUT_WASH
class Wash(ProgramBase):
    program = 'wash'

    def get_wps_info(self, interface, timeout=TIMEOUT_WASH):
        os.system("killall -s SIGKILL wash")
        cmd = [self.program, '-i', interface]
        outerr = self.pcaller.runread(cmd, timeout)
        out = outerr[0]
        #Parse out
        wps_list = []
        if out:
            wps_list = parse_wps_output(out)
        os.system("killall -s SIGKILL wash")
        return wps_list

def parse_wps_output(out):
    wps_list = []
    keys_values = out.split('--------------------------------------------------------------------------------')
    keys = keys_values[0].split() if keys_values[0] else None
    lines = keys_values[1].splitlines() if keys_values[1] else None
    if lines:
        lines = list(filter(None, lines))
        for line in lines:
            wps_dict = {}
            values = line.split()
            for idx, key in enumerate(keys):
                if idx == 6:
                    wps_dict.update({key: ' '.join(values[idx:])})
                else:
                    wps_dict.update({key: values[idx]})
            wps_list.append(wps_dict)
    return wps_list

from pandora.utils.program import ProgramBase


class Airmon(ProgramBase):
    program = 'airmon-ng'

    def switch_mode(self, interface, mode):
        #If mode is 'Monitor' then switch to monitor, if mode is 'Managed' then switch to managed.
        if mode == 'Monitor':
            monitor = 'start'
        elif mode == 'Managed':
            monitor = 'stop'
        cmd = [Airmon.program, monitor, interface]
        outerr = self.pcaller.runread(cmd)
        return outerr[0]

    def check_kill(self):
        cmd = [Airmon.program, 'check', 'kill']
        outerr = self.pcaller.runread(cmd)
        return outerr[0]

    def get_interfaces(self):
        """Returns a list of tuples (PHY, Interface)"""
        cmd = [Airmon.program]
        outerr = self.pcaller.runread(cmd)
        outstr = outerr[0]
        return self._parse_get_interfaces(outstr)
        
    def _parse_get_interfaces(self, outstr):
        out = list(filter(None, outstr.split('\n')))
        #header = out[0].split()
        data = out[1:]
        interfaces = []
        for element in data:
            aux = element.split()
            interfaces.append((aux[0], aux[1]))
        return interfaces



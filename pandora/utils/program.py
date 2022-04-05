#from abc import ABC, abstractmethod
from shutil import which
from pandora.utils.processcaller import ProcessCaller
from pandora.utils.exceptions import ProgramNotFoundError

class ProgramBase():
    program = ''
    def __init__(self):
        self.pcaller = ProcessCaller()

    def __init_subclass__(cls):
        if not cls.is_program():
            raise ProgramNotFoundError(f"Dependency {cls.program} is missing.")

    @classmethod
    def is_program(cls):
        return True if which(cls.program) else False

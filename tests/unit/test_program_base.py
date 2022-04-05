from pandora.utils.program import ProgramBase
from pandora.utils.exceptions import ProgramNotFoundError

def test_programbase_exception():
    try:
        class ImpossibleProgram(ProgramBase):
            program='thereisnowaythisconsolecommandexists'
        assert False
    except ProgramNotFoundError:
        assert True

def test_normalclass():
    try:
        class NormalClass():
            program='thereisnowaythisconsolecommandexists'
        assert True
    except ProgramNotFoundError:
        assert False
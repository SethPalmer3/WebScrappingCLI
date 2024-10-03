from enum import Enum

class MessageTypes(Enum):
    COMMAND = 'command'
    COMMAND_RESULT = 'command_result'
    STOP = 'stop'
    STOPPED = 'stopped'
    OK = 'ok'
    ERROR = 'error'

    def __repr__(self) -> str:
        return super().__repr__()

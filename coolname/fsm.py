from enum import Enum, IntEnum

class FSM(Enum):
    def next(self):
        states = list(self.__class__)
        return states[(states.index(self) + 1) % len(states)]


class InputFSM(FSM):
    NONE = 1
    SOME = 2
    ALL = 3


class OutputFSM(FSM):
    FREE = 1
    BUSY = 2


class DataFSM(FSM):
    NONE = 1
    INITIATED = 2
    COMPLETED = 3
    TRANSMITTED = 4
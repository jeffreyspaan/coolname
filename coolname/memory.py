from .config import *

class MemorySimulator():
    def load(self, addr, indices=None):
        """
        Must return (value, latency, error) pair.
        """
        raise NotImplementedError

    def store(self, val, addr, indices=None):
        """
        Must return (latency, error) pair.
        """
        raise NotImplementedError

    def dump(self):
        """
        Outputs all values currently in memory.
        """
        raise NotImplementedError


class DefaultMemorySimulator(MemorySimulator):
    def __init__(self):
        self.load_latency = Config.Latency.mem_load
        self.store_latency = Config.Latency.mem_store
        self.load_energy = Config.Energy.mem_load
        self.store_energy = Config.Energy.mem_store

        self.memory = dict()

    def load(self, addr, indices=None):
        mem_val = self.memory.get(addr)

        if mem_val is None:
            return None, None, None, True, 'No value is stored on this address'
        elif isinstance(mem_val, dict):
            if indices is None:
                return None, None, None, True, 'Attempted to get primtive from array, forgot indices?'

            array_val = mem_val.get(tuple(indices))

            if array_val is None:
                return None, None, None, True, 'No value is stored on this array element address'

            return array_val, self.load_latency, self.load_energy, False, None
        else: # primitive value
            if indices:
                return None, None, None, True, 'Attempted to get array element from primitive, why indices?'

            return mem_val, self.load_latency, self.load_energy, False, None

    def store(self, val, addr, indices=None):
        mem_val = self.memory.get(addr)

        if mem_val is None:
            if indices:
                self.memory[addr] = dict()
                self.memory[addr][tuple(indices)] = val
            else:
                self.memory[addr] = val

            return self.store_latency, self.store_energy, False, None
        elif isinstance(mem_val, dict):
            if indices is None:
                return None, None, True, 'Attempted to store primtive as array, forgot indices?'

            self.memory[addr][tuple(indices)] = val
            return self.store_latency, self.store_energy, False, None
        else:
            if indices:
                return None, None, True, 'Attempted to store array element as primitive, why indices?'

            self.memory[addr] = val
            return self.store_latency, self.store_energy, False, None

        print('UNCHARTED WATERS: abort')
        exit()

    def dump(self):
        print('MEMORY DUMP:')
        print()

        for addr, val in self.memory.items():
            if isinstance(val, dict):
                print(f'\'{addr}\'')
                print('type=array')
                for arr_indices, arr_val in val.items():
                    print(f'value{list(arr_indices)}={arr_val}')
            else:
                print(f'\'{addr}\'')
                print('type=primitive')
                print(f'value={val}')

            print()
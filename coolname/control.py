import time

from .config import *
from .logger import *

class Simulation:
    mem = None
    logger = None

    cycle = 0

    def __init__(self, graph=None, mem=None, logger=None):
        self.graph = graph

        Simulation.mem = mem
        Simulation.logger = logger

        self.stop_after = None
        self.halt_now = False

        self.busy_counter = 0
        self.start_time = 0
        self.end_time = 0

        self.ipc = []

    def run(self):
        self.start_time = time.time()

        while not (self.soft_stop() or self.hard_stop()):
            self.step()

        if self.soft_stop():
            # Account for soft stop extra unnecessary cycles.
            Simulation.cycle -= Config.Latency.communication
            self.ipc = self.ipc[:-Config.Latency.communication]

        self.end_time = time.time()

    def step(self):
        Simulation.cycle += 1

        for node in self.graph.nodes:
            node.step()

        self.was_busy()
        self.calc_ipc()

    def was_busy(self):
        if any([n.is_busy() for n in self.graph.nodes]):
            self.busy_counter = 0
        else:
            self.busy_counter += 1

    def hard_stop(self):
        if self.halt_now:
            return True

        if self.stop_after:
            if Simulation.cycle == self.stop_after:
                return True

        return False

    def soft_stop(self):
        return self.busy_counter == Config.Latency.communication

    def reset(self):
        Simulation.cycle = 0
        self.halt_now = False
        self.busy_counter = 0
        self.start_time = 0
        self.end_time = 0
        self.ipc = []

        for node in self.graph.nodes:
            node.reset()

        for wire in self.graph.wires:
            wire.reset()

    def calc_ipc(self):
        self.ipc.append(sum([n.in_computation for n in self.graph.nodes]))

    def get_ipc_series(self):
        return self.ipc

    def get_end_statistics(self):
        # Total cycle count:
        total_cycle_count = Simulation.cycle

        # Total energy consumption:
        total_energy = sum([n.energy for n in self.graph.nodes])

        # Average utilization percentage:
        utilizations = [n.utilization/total_cycle_count for n in self.graph.nodes if n.utilization > 0]
        avg_utilization = (sum(utilizations)/len(self.graph.nodes))*100 if len(self.graph.nodes) > 0 else 0

        # Simulator run-time:
        runtime = self.end_time - self.start_time

        return (total_cycle_count, total_energy, avg_utilization, runtime)
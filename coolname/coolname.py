from coolname.gui import GUI
from coolname.control import Simulation
from coolname.logger import Logger
from coolname.memory import DefaultMemorySimulator

def main():
    my_mem = DefaultMemorySimulator()
    my_gui = GUI()
    my_logger = Logger(my_gui)
    my_sim = Simulation(mem=my_mem, logger=my_logger)

    my_gui.simulation = my_sim
    my_gui.build()
    my_gui.start()
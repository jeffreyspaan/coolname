To run the GUI: 
python3 coolname_gui.py


To interact in code:

from gui import *
from control import *
from logger import *
from memory import *
from nodes import *


# Construct graph
graph = IR.from_DOT('mygraph.dot')

# Setup 
mem = DefaultMemorySimulator()
logger = Logger()
sim = Simulation(mem=mem, logger=logger)

# Optionally interact with memory:
mem.store(2, 'a')
mem.store(True, 'b', [0,0])

# Start
sim.run()
#sim.step()
#sim.reset()

# Statistics:
sim.get_ipc_series()
sim.get_end_statistics()

# \<CoolName\>: a dataflow simulator.

Abstract from thesis:
> In recent developments, dataflow graphs are used to design highly parallel application-specific hardware (ASH). However, prototyping and optimizing these graphs - and the techniques used to construct them - is difficult as constructing and testing hardware circuits directly is expensive, both in time as cost. Currently, no model or tool exists to compare these graphs in terms of latency, energy and utilization.

> In this thesis, we present \<CoolName\>, a cycle-accurate, application-level static dataflow simulator, which can be used for analyzing high-level synthesis for application-specific hardware. Furthermore, we present and analyze several techniques and strategies to convert control dataflow graphs to pure dataflow graphs, and outline the possible challenges and limitations of this process. We validate the simulator - in terms of correctness and compliance to the static dataflow model - using controlled experiments in which we compare the execution of a dataflow graph using \<CoolName\>, the execution of a conventional reference program and a manual simulation of the dataflow graph.

> \<CoolName\> can be used as a tool to compare and optimize dataflow graphs for application-specific hardware by reporting performance metrics such as latency, energy and utilization. For ease of use, we also provide a GUI for the simulator, where the user can set input parameters, control the execution and gather performance results.


### Installation

---

Tested for Python 3.8.
```
pip3 install -r requirements.txt
```

### Usage

---

From the GUI:
```
python3 run.py
```

Directly:
```
from coolname.gui import GUI
from coolname.control import Simulation
from coolname.logger import Logger
from coolname.memory import DefaultMemorySimulator
from coolname.nodes import IR

# Load graph
graph = IR.from_DOT('mygraph.dot')

# Setup 
mem = DefaultMemorySimulator()
logger = Logger()
sim = Simulation(mem=mem, logger=logger)

# Interact with memory:
mem.store(2, 'a')
mem.store(True, 'b', [0,0])

# Start
sim.run()
# or
# sim.step()
# or
# sim.reset()

# Statistics:
sim.get_ipc_series()
sim.get_end_statistics()
```

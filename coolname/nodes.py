from enum import Enum, IntEnum
import re
import math
import pydot

from .operator_ import *
from .config import *
from .control import *
from .fsm import *

class Input:
    value_types = IntEnum('Types', 'DATA PREDICATE TOKEN')

    def read(self, consume=True):
        raise NotImplementedError

    def send(self, data, latency=None):
        raise NotImplementedError

    def acknowledge(self, latency=None):
        raise NotImplementedError

    def is_ready(self):
        raise NotImplementedError

    def is_acknowledged(self):
        raise NotImplementedError


class IntegratedConstant(Input):
    def __init__(self, data, value_type, name='ICONST'):
        self.data = data
        self.name = name
        self.value_type = value_type

    def read(self, consume=True):
        return self.data

    def acknowledge(self, latency=None):
        return

    def is_ready(self):
        return True


class Wire(Input):
    def __init__(self, input_, output_, value_type, name='WIRE'):
        assert isinstance(input_, Node), 'Input node class is unknown'
        self.input_ = input_

        assert isinstance(output_, Node), 'Output node class is unknown'
        self.output_ = output_

        input_.add_output(self)
        output_.add_input(self)

        self.name = name

        assert isinstance(value_type, Input.value_types), 'Wire value type is unknown'
        self.value_type = value_type

        self.data = None
        self.data_ready = -1
        self.acknowledged = -1

    def reset(self):
        self.data = None
        self.data_ready = -1
        self.acknowledged = -1

    def read(self, consume=True):
        data = self.data

        if consume:
            self.data = None
            self.data_ready = -1

        return data

    def send(self, data, latency=None):
        if self.is_ready():
            Simulation.logger.log_error(Simulation.cycle, self,
                f'cannot send, [{self.data}] already in wire {self.name}: [{self.input_.name}] -> [{self.output_.name}]')
        else:
            Simulation.logger.log_send(Simulation.cycle, self, data)

            if not latency:
                latency = Config.Latency.communication

            self.acknowledged = -1
            self.data = data
            self.data_ready = Simulation.cycle + latency

    def acknowledge(self, latency=None):
        if not latency:
            latency = Config.Latency.communication

        self.acknowledged = Simulation.cycle + latency

    def is_ready(self):
        return self.data_ready >= 0 and \
               self.data_ready <= Simulation.cycle

    def is_acknowledged(self):
        return self.acknowledged >= 0 and \
               self.acknowledged <= Simulation.cycle


class Node:
    name = "UNNAMED"

    def __init__(self):
        self.inputs = []
        self.outputs = []

        # Default FSM states.
        self.input_state = InputFSM.NONE
        self.output_state = OutputFSM.FREE
        self.data_state = DataFSM.NONE

        self.default_data_ready = -1
        self.data_ready = self.default_data_ready

        self.energy = 0
        self.utilization = 0

        self.busy = False
        self.in_computation = False

    @staticmethod
    def generate_dummy_data(type_):
        if type_ is int:
            return 1
        if type_ is float:
            return 1.0
        if type_ is bool:
            return True
        else:
            Simulation.logger.log_error(Simulation.cycle, self,
                f'cannot generate dummy value, type [{type_}] is unknown')

    def add_input(self, i):
        self.inputs.append(i)

    def add_output(self, o):
        self.outputs.append(o)

    def get_data_inputs(self):
        return [i for i in self.inputs if i.value_type == Input.value_types.DATA]

    def get_predicate_inputs(self):
        return [i for i in self.inputs if i.value_type == Input.value_types.PREDICATE]

    def get_token_input(self):
        return [i for i in self.inputs if i.value_type == Input.value_types.TOKEN]

    def get_matching_inputs(self):
        matches = []
        names = set([i.name for i in self.inputs])

        for name in names:
            matches.append(sorted([i for i in self.inputs if i.name == name],
                                  key=lambda i: i.value_type))

        return matches

    def step(self):
        self.busy = False
        self.in_computation = False

        self.process_inputs()
        self.process_outputs()
        self.process_data()

    def reset(self):
        self.input_state = InputFSM.NONE
        self.output_state = OutputFSM.FREE
        self.data_state = DataFSM.NONE

        self.busy = False
        self.in_computation = False

        self.data_ready = self.default_data_ready

        self.energy = 0
        self.utilization = 0

    ################
    ## Input FSM ##
    ################

    def process_inputs(self):
        if self.input_state == InputFSM.NONE:
            self.process_inputs_NONE()

        if self.input_state == InputFSM.SOME:
            self.process_inputs_SOME()

    def process_inputs_NONE(self):
        inputs_ready = [i.is_ready() for i in self.inputs]

        if sum(inputs_ready) > 0:
            Simulation.logger.log_inputFSM_transition(Simulation.cycle, self)
            self.input_state = InputFSM.SOME

    def process_inputs_SOME(self):
        inputs_ready = [i.is_ready() for i in self.inputs]

        if all(inputs_ready):
            Simulation.logger.log_inputFSM_transition(Simulation.cycle, self)
            self.input_state = InputFSM.ALL


    ################
    ## Output FSM ##
    ################

    def process_outputs(self):
        if self.output_state == OutputFSM.BUSY:
            self.process_outputs_BUSY()

    def process_outputs_BUSY(self):
        if all([o.is_acknowledged() for o in self.outputs]):
            Simulation.logger.log_outputFSM_transition(Simulation.cycle, self)
            self.output_state = OutputFSM.FREE

    ################
    ## Data FSM ##
    ################

    def is_busy(self):
        return self.busy or self.in_computation

    def data_is_ready(self):
        return self.data_ready >= 0 and \
               self.data_ready <= Simulation.cycle

    def reset_data_ready(self):
        self.data_ready = self.default_data_ready

    def process_data(self):
        if self.data_state == DataFSM.NONE:
            self.process_data_NONE()

        if self.data_state == DataFSM.INITIATED:
            self.process_data_INITIATED()

        if self.data_state == DataFSM.COMPLETED:
            self.process_data_COMPLETED()

        if self.data_state == DataFSM.TRANSMITTED:
            self.process_data_TRANSMITTED()

    def process_data_NONE(self):
        raise NotImplementedError

    def process_data_INITIATED(self):
        self.in_computation = True

        if self.data_is_ready():
            self.in_computation = False
            self.busy = True

            self.reset_data_ready()

            Simulation.logger.log_dataFSM_transition(Simulation.cycle, self)
            self.data_state = DataFSM.COMPLETED

    def process_data_COMPLETED(self):
        if self.output_state == OutputFSM.FREE:
            self.busy = True

            # Transmit the data on all output wires.
            for o in self.outputs:
                o.send(self.data)

            Simulation.logger.log_dataFSM_transition(Simulation.cycle, self)
            self.data_state = DataFSM.TRANSMITTED

            Simulation.logger.log_outputFSM_transition(Simulation.cycle, self)
            self.output_state = OutputFSM.BUSY

    def process_data_TRANSMITTED(self):
        self.busy = True

        if self.inputs:
            # Send acknowledgements to all inputs.
            for i in self.inputs:
                i.acknowledge()

            Simulation.logger.log_inputFSM_transition(Simulation.cycle, self)
            self.input_state = InputFSM.NONE

        Simulation.logger.log_dataFSM_transition(Simulation.cycle, self)
        self.data_state = DataFSM.NONE


class Computation(Node):
    ctr = 1

    def __init__(self, operator, type_=None, name=None):
        super().__init__()

        if name is None:
            self.name = 'COMP' + str(Computation.ctr)
            Computation.ctr += 1
        else:
            self.name = name

        self.operator = operator
        self.type_ = type_

    def process_data_NONE(self):
        if self.input_state == InputFSM.ALL:
            self.busy = True

            pred = self.get_predicate_inputs()[0].read()
            data_inputs = {i.name:i.read() for i in self.get_data_inputs()}

            if pred:
                self.data = self.operator.compute(data_inputs)
                self.data_ready = Simulation.cycle \
                                + Config.Latency.computation[self.operator]

                self.energy += Config.Energy.computation[self.operator]
                self.utilization += Config.Latency.computation[self.operator]
            else:
                self.data = self.generate_dummy_data(self.type_)
                self.data_ready = Simulation.cycle

            Simulation.logger.log_dataFSM_transition(Simulation.cycle, self)
            self.data_state = DataFSM.INITIATED


class ContinualConstant(Node):
    ctr = 1

    def __init__(self, data, name=None):
        super().__init__()

        if name is None:
            self.name = 'CC' + str(ContinualConstant.ctr)
            ContinualConstant.ctr += 1
        else:
            self.name = name

        self.data = data

    def process_data_NONE(self):
        self.busy = True

        # Constants always have zero latency.
        self.data_ready = Simulation.cycle

        Simulation.logger.log_dataFSM_transition(Simulation.cycle, self)
        self.data_state = DataFSM.INITIATED


class OnetimeConstant(Node):
    ctr = 1

    def __init__(self, data, name=None):
        super().__init__()

        if name is None:
            self.name = 'OTC' + str(OnetimeConstant.ctr)
            OnetimeConstant.ctr += 1
        else:
            self.name = name

        self.data = data
        self.has_fired = False

    def reset(self):
        super().reset()
        self.has_fired = False

    def process_data_NONE(self):
        if not self.has_fired:
            self.has_fired = True
            self.busy = True

            # Constants always have zero latency.
            self.data_ready = Simulation.cycle

            Simulation.logger.log_dataFSM_transition(Simulation.cycle, self)
            self.data_state = DataFSM.INITIATED


class Mu(Node):
    ctr = 1

    def __init__(self, name=None):
        super().__init__()

        if name is None:
            self.name = 'MU' + str(Mu.ctr)
            Mu.ctr += 1
        else:
            self.name = name

        self.data = None
        self.data_carrying_input = None

    def reset(self):
        super().reset()
        self.data_carrying_input = None

    def check(self):
        inputs_ready = [i.is_ready() for i in self.inputs]
        assert sum(inputs_ready) <= 1, 'Mu node "{}" has multiple inputs to choose from'.format(self.name)

    def process_data_NONE(self):
        if self.input_state == InputFSM.SOME or \
          (self.input_state == InputFSM.ALL and len(self.inputs) == 1):
            self.busy = True

            # Determine which input has sent something and read the data.
            self.data_carrying_input = None
            self.data = None

            for i in self.inputs:
                if i.is_ready():
                    self.data_carrying_input = i
                    self.data = i.read()

            self.data_ready = Simulation.cycle \
                            + math.ceil(Config.Latency.mu(len(self.inputs)))

            self.energy += Config.Energy.mu(len(self.inputs))
            self.utilization += math.ceil(Config.Latency.mu(len(self.inputs)))

            Simulation.logger.log_dataFSM_transition(Simulation.cycle, self)
            self.data_state = DataFSM.INITIATED

        elif self.input_state == InputFSM.ALL and len(self.inputs) > 1:
            Simulation.logger.log_error(Simulation.cycle, self,
                f'mu [{self.name}] has multiple input values to choose from')

    def process_data_TRANSMITTED(self):
        self.busy = True

        # Send acknowledgements to the input which has sent something.
        self.data_carrying_input.acknowledge()

        # Note that the input FSM advances to NONE from SOME,
        # skipping ALL because if more than one input is ready,
        # the graph is incorrect.
        Simulation.logger.log_inputFSM_transition(Simulation.cycle, self, specific=InputFSM.NONE)
        self.input_state = InputFSM.NONE

        Simulation.logger.log_dataFSM_transition(Simulation.cycle, self)
        self.data_state = DataFSM.NONE


class ETA(Node):
    ctr = 1

    def __init__(self, name=None):
        super().__init__()

        if name is None:
            self.name = 'ETA' + str(ETA.ctr)
            ETA.ctr += 1
        else:
            self.name = name

        self.data = None

    def check(self):
        assert len(self.inputs) == 2

    def data_is_ready(self):
        return self.data_ready >= 0 and \
               self.data_ready <= Simulation.cycle

    def process_data_NONE(self):
        if self.input_state == InputFSM.ALL:
            self.busy = True

            data = self.get_data_inputs()[0].read()
            pred = self.get_predicate_inputs()[0].read()

            if pred:
                self.data = data
                self.data_ready = Simulation.cycle \
                                + Config.Latency.eta

                self.energy += Config.Energy.eta
                self.utilization += Config.Latency.eta

                Simulation.logger.log_dataFSM_transition(Simulation.cycle, self)
                self.data_state = DataFSM.INITIATED
            else:
                # The predicate is false, so the data must be discarded
                # and the inputs acknowledged.
                for i in self.inputs:
                    i.acknowledge()

                Simulation.logger.log_inputFSM_transition(Simulation.cycle, self)
                self.input_state = InputFSM.NONE

                Simulation.logger.log_dataFSM_transition(Simulation.cycle, self, specific=DataFSM.NONE)
                self.data_state = DataFSM.NONE


class Mux(Node):
    ctr = 1

    def __init__(self, name=None):
        super().__init__()

        if name is None:
            self.name = 'MUX' + str(Mux.ctr)
            Mux.ctr += 1
        else:
            self.name = name

        self.data = None

    def process_data_NONE(self):
        if self.input_state != InputFSM.NONE:
            for i_data, i_pred in self.get_matching_inputs():
                if i_data.is_ready() and i_pred.is_ready():
                    if i_pred.read(consume=False):
                        self.busy = True

                        self.data = i_data.read(consume=False)
                        self.data_ready = Simulation.cycle \
                                        + math.ceil(Config.Latency.mux(len(self.inputs)))

                        self.energy += Config.Energy.mux(len(self.inputs))
                        self.utilization += math.ceil(Config.Latency.mux(len(self.inputs)))

                        Simulation.logger.log_dataFSM_transition(Simulation.cycle, self)
                        self.data_state = DataFSM.INITIATED
        elif self.input_state == InputFSM.ALL:
            pass
            # TODO: what to do if all predicates are False: send dummy output? send nothing?

    def process_data_TRANSMITTED(self):
        if self.input_state == InputFSM.ALL:
            self.busy = True

            # Send acknowledgements to all inputs, which is only done after
            # inputs are ready (but might be done x cycles after data is sent).
            for i in self.inputs:
                # Consume unneeded data.
                if i.is_ready():
                    i.read()

                i.acknowledge()

            Simulation.logger.log_inputFSM_transition(Simulation.cycle, self)
            self.input_state = InputFSM.NONE

            Simulation.logger.log_dataFSM_transition(Simulation.cycle, self)
            self.data_state = DataFSM.NONE


class MemoryLoad(Node):
    ctr = 1

    def __init__(self, addr, type_, name=None):
        super().__init__()

        if name is None:
            self.name = 'MEML' + str(MemoryLoad.ctr)
            MemoryLoad.ctr += 1
        else:
            self.name = name

        self.addr = addr
        self.type_ = type_
        self.data = None

    def process_data_NONE(self):
        if self.input_state == InputFSM.ALL:
            self.busy = True
            indices = []

            if len(self.get_data_inputs()) > 0:
                indices_pairs = [(i.name, i.read()) for i in self.get_data_inputs()]
                indices = sorted(indices_pairs, key=(lambda a: int(a[0][1:-1:])))
                indices = [value for _,value in indices]

            pred = self.get_predicate_inputs()[0].read()

            if pred:
                self.data, load_latency, load_energy, error, error_msg = Simulation.mem.load(self.addr, indices=indices)

                if error:
                    mem_str = self.addr + '[' + ']['.join(map(str,indices)) + ']' if indices else self.addr
                    Simulation.logger.log_error(Simulation.cycle, self, f'memory load {mem_str} failed: {error_msg}')

                self.data_ready = Simulation.cycle \
                                + load_latency

                self.energy += load_energy
                self.utilization += load_latency
            else:
                # The predicate is false, so no memory value is retrieved
                # and dummy data is used. The data is set to be ready
                # this cycle (to immediatly be transmitted).
                self.data = self.generate_dummy_data(self.type_)
                self.data_ready = Simulation.cycle

            Simulation.logger.log_dataFSM_transition(Simulation.cycle, self)
            self.data_state = DataFSM.INITIATED

    def process_data_COMPLETED(self):
        if self.output_state == OutputFSM.FREE:
            self.busy = True

            # Transmit the data on all output wires.
            for o in self.outputs:
                if o.value_type == Input.value_types.DATA:
                    o.send(self.data)
                elif o.value_type == Input.value_types.PREDICATE:
                    o.send(True)

            Simulation.logger.log_dataFSM_transition(Simulation.cycle, self)
            self.data_state = DataFSM.TRANSMITTED

            Simulation.logger.log_outputFSM_transition(Simulation.cycle, self)
            self.output_state = OutputFSM.BUSY


class MemoryStore(Node):
    ctr = 1

    def __init__(self, addr, type_=None, name=None):
        super().__init__()

        if name is None:
            self.name = 'MEMS' + str(MemoryStore.ctr)
            MemoryStore.ctr += 1
        else:
            self.name = name

        self.addr = addr
        self.data = None

    def process_data_NONE(self):
        if self.input_state == InputFSM.ALL:
            self.busy = True
            indices_pairs = []
            val = None

            for i in self.get_data_inputs():
                indice_re = re.findall('\[.*\]', i.name)

                if indice_re:
                    indices_pairs.append((indice_re[0], i.read()))
                else:
                    val = i.read()

            indices = sorted(indices_pairs, key=(lambda a: a[0]))
            indices = [value for _,value in indices]

            pred = self.get_predicate_inputs()[0].read()

            if pred:
                Simulation.logger.log_mem_store(val, self.addr, indices)
                store_latency, store_energy, error, error_msg = Simulation.mem.store(val, self.addr, indices=indices)

                if error:
                    mem_str = self.addr + '[' + ']['.join(map(str,indices)) + ']' if indices else self.addr
                    Simulation.logger.log_error(Simulation.cycle, self, f'memory store {mem_str} failed: {error_msg}')

                self.data = True
                self.data_ready = Simulation.cycle \
                                + store_latency

                self.energy += store_energy
                self.utilization += store_latency
            else:
                self.data = False
                self.data_ready = Simulation.cycle

            Simulation.logger.log_dataFSM_transition(Simulation.cycle, self)
            self.data_state = DataFSM.INITIATED


class Combine(Node):
    ctr = 1

    def __init__(self, name=None):
        super().__init__()

        if name is None:
            self.name = 'COMBINE' + str(Combine.ctr)
            Combine.ctr += 1
        else:
            self.name = name

        self.data = None

    def process_data_NONE(self):
        if self.input_state != InputFSM.NONE:
            self.busy = True

            ready_input_values = [i.read(consume=False) for i in self.inputs if i.is_ready()]

            if False in ready_input_values:
                # If some or all inputs are ready and one or more is False,
                # the combine will send a False signal.
                self.data = False
            elif len(ready_input_values) == len(self.inputs):
                # No input has sent a False signal and all inputs are ready,
                # so the combine will send a True signal.
                self.data = True
            else:
                # If all inputs are True but not all inputs have arrived, a
                # False input might still arrive in the future, thus, we do not
                # send a value yet.
                return

            self.data_ready = Simulation.cycle \
                            + math.ceil(Config.Latency.combine(len(self.inputs)))

            self.energy += Config.Energy.combine(len(self.inputs))
            self.utilization += math.ceil(Config.Latency.combine(len(self.inputs)))

            Simulation.logger.log_dataFSM_transition(Simulation.cycle, self)
            self.data_state = DataFSM.INITIATED

    def process_data_TRANSMITTED(self):
        if self.input_state == InputFSM.ALL:
            self.busy = True

            # Send acknowledgements to all inputs, which is only done after
            # inputs are ready (but might be done x cycles after data is sent).
            for i in self.inputs:
                # Consume unneeded data.
                if i.is_ready():
                    i.read()

                i.acknowledge()

            Simulation.logger.log_inputFSM_transition(Simulation.cycle, self)
            self.input_state = InputFSM.NONE

            Simulation.logger.log_dataFSM_transition(Simulation.cycle, self)
            self.data_state = DataFSM.NONE


class XOR(Node):
    ctr = 1

    def __init__(self, name=None):
        super().__init__()

        if name is None:
            self.name = 'XOR' + str(XOR.ctr)
            XOR.ctr += 1
        else:
            self.name = name

        self.data = None

    def process_data_NONE(self):
        if self.input_state != InputFSM.NONE:
            self.busy = True

            ready_input_values = [i.read(consume=False) for i in self.inputs if i.is_ready()]

            if True in ready_input_values:
                # If some or all inputs are ready and one or more is True, the xor
                # will send a True signal.
                self.data = True
            elif len(ready_input_values) == len(self.inputs):
                # No input has sent a True signal and all inputs are ready,
                # so the xor will send a False signal.
                self.data = False
            else:
                # If all inputs are False but not all inputs have arrived, a
                # False input might still arrive in the future, thus, we do not
                # send a value yet.
                return

            self.data_ready = Simulation.cycle \
                            + math.ceil(Config.Latency.xor(len(self.inputs)))

            self.energy += Config.Energy.xor(len(self.inputs))
            self.utilization += math.ceil(Config.Latency.xor(len(self.inputs)))

            Simulation.logger.log_dataFSM_transition(Simulation.cycle, self)
            self.data_state = DataFSM.INITIATED

    def process_data_TRANSMITTED(self):
        if self.input_state == InputFSM.ALL:
            self.busy = True

            # Send acknowledgements to all inputs, which is only done after
            # inputs are ready (but might be done x cycles after data is sent).
            for i in self.inputs:
                # Consume unneeded data.
                if i.is_ready():
                    i.read()

                i.acknowledge()

            Simulation.logger.log_inputFSM_transition(Simulation.cycle, self)
            self.input_state = InputFSM.NONE

            Simulation.logger.log_dataFSM_transition(Simulation.cycle, self)
            self.data_state = DataFSM.NONE


class Drain(Node):
    def __init__(self, name='DRAIN'):
        super().__init__()

        self.name = name

    def process_data(self):
        for i in self.inputs:
            if i.is_ready():

                print('{} RESULT: {}'.format(self.name, i.read()))
                i.acknowledge()


class IR:
    node_mapping = {
        # DOT shape : IR Node
        'box': Computation,
        'doublecircle': OnetimeConstant,
        'circle': ContinualConstant,
        'diamond': Mu,
        'parallelogram': ETA,
        'invtrapezium': Mux,
        'invtriangle': MemoryLoad,
        'triangle': MemoryStore,
        'house': Combine,
        'hexagon': XOR,
        'star': Drain
    }

    sign_mapping = {
        # IR operator: DOT label
        Operator.ADD: '+',
        Operator.SUB: '-',
        Operator.MUL: '*',
        Operator.DIV: '/',
        Operator.MOD: '%',
        Operator.LT: '\<',
        Operator.LE: '\<=',
        Operator.GT: '\>',
        Operator.GE: '\>=',
        Operator.EQ: '==',
        Operator.NE: '!=',
        Operator.NEG: '-',
        Operator.NOT: '!'
    }

    operator_mapping = {
        # DOT operator: IR operator
        'ADD': Operator.ADD,
        'SUB': Operator.SUB,
        'MUL': Operator.MUL,
        'DIV': Operator.DIV,
        'MOD': Operator.MOD,
        'LT': Operator.LT,
        'LE': Operator.LE,
        'GT': Operator.GT,
        'GE': Operator.GE,
        'EQ': Operator.EQ,
        'NE': Operator.NE,
        'NEG': Operator.NEG,
        'NOT': Operator.NOT
    }

    # Removes the need for a pointless eval().
    type_mapping = {
        # DOT type: IR type
        'int': int,
        'float': float,
        'bool': bool
    }

    def __init__(self, blocks=None, wires=None):
        # The first block inside the blocks list is the global 'block'.

        self.blocks = blocks
        self.nodes = [n for b in blocks for n in b] if blocks else None
        self.wires = wires

    @classmethod
    def from_DOT(cls, filename):
        # Notes:
        # All edges must be 'global', in-block edges are not registered.

        a = pydot.graph_from_dot_file(filename)

        DOT_g = pydot.graph_from_dot_file(filename)[0]
        g = IR()

        all_nodes = dict()
        blocks = []
        wires = []

        def strip_quotation(s):
            if s:
                return s[1:-1] if (s[0] == '"' and s[-1] == '"') else s

        def create_IR_node(DOT_n):
            DOT_n_name = strip_quotation(DOT_n.get_name())
            DOT_n_label = strip_quotation(DOT_n.get('label'))

            if DOT_n_name == 'node' or DOT_n_name == 'edge' or DOT_n_name == 'graph':
                return

            node_kwargs = {}

            if DOT_n_label and \
                (cls.node_mapping[DOT_n.get('shape')] is OnetimeConstant or \
                 cls.node_mapping[DOT_n.get('shape')] is ContinualConstant or \
                 cls.node_mapping[DOT_n.get('shape')] is MemoryLoad or \
                 cls.node_mapping[DOT_n.get('shape')] is MemoryStore):

                if DOT_n_label == 'T' or DOT_n_label == 'True' or DOT_n_label == 'true':
                    # Constant with True value.
                    node_kwargs['data'] = True
                elif DOT_n_label == 'F' or DOT_n_label == 'False' or DOT_n_label == 'false':
                    # Constant with False value.
                    node_kwargs['data'] = False
                elif DOT_n_label.isidentifier():
                    # Memory node with address.
                    node_kwargs['addr'] = DOT_n_label
                else:
                    # Constant with int or float value.
                    node_kwargs['data'] = eval(DOT_n_label)

            if DOT_n.get('operator'):
                node_kwargs['operator'] = cls.operator_mapping[strip_quotation(DOT_n.get('operator'))]

            if DOT_n.get('type'):
                node_kwargs['type_'] = cls.type_mapping[strip_quotation(DOT_n.get('type'))]

            n = cls.node_mapping[DOT_n.get('shape')](name=DOT_n_name, **node_kwargs)
            return n

        # Add global nodes.
        global_nodelist = []

        for DOT_n in DOT_g.get_nodes():
            n = create_IR_node(DOT_n)
            if n is not None:
                all_nodes[n.name] = n
                global_nodelist.append(n)

        blocks.append(global_nodelist)

        # Add in-block nodes.
        for sg in DOT_g.get_subgraphs():
            sg_nodelist = []

            for DOT_n in sg.get_nodes():
                n = create_IR_node(DOT_n)
                if n is not None:
                    all_nodes[n.name] = n
                    sg_nodelist.append(n)

            blocks.append(sg_nodelist)

        # Add wires.
        for DOT_w in DOT_g.get_edges():
            wire_kwargs = {}

            if DOT_w.get('style') and strip_quotation(DOT_w.get('style')) == 'dotted':
                wire_kwargs['value_type'] = Input.value_types.PREDICATE
            else:
                wire_kwargs['value_type'] = Input.value_types.DATA

            if DOT_w.get('label'):
                wire_kwargs['name'] = strip_quotation(DOT_w.get('label'))

            w = Wire(input_=all_nodes[DOT_w.get_source()], output_=all_nodes[DOT_w.get_destination()], **wire_kwargs)
            wires.append(w)

        g.nodes = list(all_nodes.values())
        g.blocks = blocks
        g.wires = wires
        return g

    def to_DOT(self, theme='Dark 2'):
        def add_node_to_DOT(g, n):
            node_kwargs = {}

            if n.is_busy():
                if theme == 'Light':
                    node_kwargs['fillcolor'] = '#aaccf4'
                elif theme == 'Dark':
                    node_kwargs['fillcolor'] = '#009600'
                elif theme == 'Dark 2':
                    node_kwargs['fillcolor'] = '#009600'

            if n.in_computation:
                # Might override 'busy' color, but is accepted as all
                # 'in computation' nodes are by definition also busy.
                if theme == 'Light':
                    node_kwargs['fillcolor'] = '#960000'
                elif theme == 'Dark':
                    node_kwargs['fillcolor'] = '#960000'
                elif theme == 'Dark 2':
                    node_kwargs['fillcolor'] = '#960000'

            if hasattr(n, 'type_') and n.type_ is not None:
                for DOT_type, type_ in self.type_mapping.items():
                    if type_ is n.type_:
                        node_kwargs['type'] = DOT_type

            if isinstance(n, Computation):
                g.add_node(pydot.Node(n.name, label=f'"{n.operator.sign()}"', shape='box', operator=n.operator.name, **node_kwargs))
            elif isinstance(n, OnetimeConstant):
                g.add_node(pydot.Node(n.name, label=(('"T"' if n.data else '"F"') if isinstance(n.data, bool) else str(n.data)), shape='doublecircle', **node_kwargs))
            elif isinstance(n, ContinualConstant):
                g.add_node(pydot.Node(n.name, label=(('"T"' if n.data else '"F"') if isinstance(n.data, bool) else str(n.data)), shape='circle', **node_kwargs))
            elif isinstance(n, Mu):
                g.add_node(pydot.Node(n.name, label='"MU"', shape='diamond', **node_kwargs))
            elif isinstance(n, ETA):
                g.add_node(pydot.Node(n.name, label='"ETA"', shape='parallelogram', **node_kwargs))
            elif isinstance(n, Mux):
                g.add_node(pydot.Node(n.name, label='"MUX"', shape='invtrapezium', **node_kwargs))
            elif isinstance(n, MemoryLoad):
                g.add_node(pydot.Node(n.name, label=f'"{n.addr}"', shape='invtriangle', **node_kwargs))
            elif isinstance(n, MemoryStore):
                g.add_node(pydot.Node(n.name, label=f'"{n.addr}"', shape='triangle', **node_kwargs))
            elif isinstance(n, Combine):
                g.add_node(pydot.Node(n.name, label='"COMBINE"', shape='house', **node_kwargs))
            elif isinstance(n, XOR):
                g.add_node(pydot.Node(n.name, label='"XOR"', shape='hexagon', **node_kwargs))
            else:
                g.add_node(pydot.Node(n.name, label=f'"{n.name}"', shape='star', **node_kwargs))

        g = pydot.Dot('IR', graph_type='digraph')
        g.set_graph_defaults(bgcolor='transparent', ratio='0.5545')

        if theme == 'Light':
            g.set_node_defaults(fillcolor='#d4f3fd', style='filled', color='#aaccf4')
        if theme == 'Dark':
            g.set_node_defaults(fillcolor='#1d2f49', style='filled', fontcolor='white', color='#aaccf4')
            g.set_edge_defaults(color='white', fontcolor='white')
        if theme == 'Dark 2':
            g.set_node_defaults(fillcolor='#1d2f49', style='filled', fontcolor='white', color='#aaccf4')
            g.set_edge_defaults(color='white', fontcolor='white')


        # Add global nodes.
        for n in self.blocks[0]:
            add_node_to_DOT(g, n)

        # Add in-block nodes.
        cluster_ctr = 1

        for b in self.blocks[1:]:
            cluster_ctr += 1

            sg = pydot.Subgraph(f'cluster_{str(cluster_ctr)}', color='#aaccf4', penwidth='2')
            g.add_subgraph(sg)

            for n in b:
                add_node_to_DOT(sg, n)

        # Add wires.
        for w in self.wires:
            wire_kwargs = {}

            if w.value_type == Input.value_types.PREDICATE:
                wire_kwargs['style'] = 'dotted'

            if w.name != 'WIRE':
                wire_kwargs['label'] = f'"{w.name}"'

            g.add_edge(pydot.Edge(w.input_.name, w.output_.name, **wire_kwargs))

        return g

    def to_DOTfile(self, filename):
        g = self.to_DOT()
        g.write_raw(filename)

    def to_stylizedPNGfile(self, filename):
        g = self.to_DOT()
        g.write_png(filename)

        return filename
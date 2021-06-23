class Logger:

    def __init__(self, gui=None):
        self.gui = gui

    def log_inputFSM_transition(self, cycle, node, specific=None):
        if specific:
            msg = f'[{node.name}] input: {node.input_state.name} -> {specific.name}'
        else:
            msg = f'[{node.name}] input: {node.input_state.name} -> {node.input_state.next().name}'

        self._report(cycle, 'trace', msg)

    def log_outputFSM_transition(self, cycle, node, specific=None):
        if specific:
            msg = f'[{node.name}] output: {node.output_state.name} -> {specific.name}'
        else:
            msg = f'[{node.name}] output: {node.output_state.name} -> {node.output_state.next().name}'

        self._report(cycle, 'trace', msg)

    def log_dataFSM_transition(self, cycle, node, specific=None):
        if specific:
            msg = f'[{node.name}] data: {node.data_state.name} -> {specific.name}'
        else:
            msg = f'[{node.name}] data: {node.data_state.name} -> {node.data_state.next().name}'

        self._report(cycle, 'trace', msg)

    def log_send(self, cycle, wire, data):
        msg = f'[{wire.input_.name}] sending [{data}] to [{wire.output_.name}] on wire [{wire.name}]'
        self._report(cycle, 'debug', msg)

    def log_error(self, cycle, node, error):
        msg = f'[{node.name}]: {error}'
        self._report(cycle, 'error', msg)

    def _report(self, cycle, level, msg):
        if self.gui:
            self.gui.log(cycle, level, msg)
        else:
            print(f'{cycle}| {msg}')

    def log_mem_store(self, value, identifier, indices=None):
        if self.gui:
            self.gui.log_mem(value, identifier, indices)
        else:
            print(f'Memory store: {identifier}{indices if indices else ""} = {value}')
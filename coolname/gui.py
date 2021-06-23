from dearpygui.core import *
from dearpygui.simple import *
import os
import json

from .config import *
from .operator_ import *
from .control import *
from .nodes import *

class GUI:
    def __init__(self):
        self.simulation = None
        self.animation_ctr = 1

        self.mem_table_rows = 0
        self.mem_table_data = []

    def build(self):
        set_main_window_size(1650, 915)
        set_main_window_title('<CoolName> simulator')
        add_additional_font("coolname/fonts/JetBrainsMono-Regular.ttf", 15)
        set_exit_callback(self.stop)

        set_theme('Dark 2')
        set_theme_item(mvGuiCol_Text, 235, 235, 235, 230)
        set_theme_item(mvGuiCol_Tab, 0, 121, 0, 255)
        set_theme_item(mvGuiCol_TabHovered, 0, 175, 0, 255)
        set_theme_item(mvGuiCol_TabActive, 0, 175, 0, 255)
        set_theme_item(mvGuiCol_ButtonActive, 45, 105, 200, 173)
        set_theme_item(mvGuiCol_WindowBg, 23, 23, 38, 240)


        self.create_config_window()
        self.create_memory_window()
        self.create_graph_window()
        self.create_editor_window()
        self.create_control_window()
        self.create_logger_window()
        self.create_performance_window()

    def start(self):
        start_dearpygui(primary_window='graph_window')

    def stop(self, sender, data):
        if self.animation_ctr > 1:
            os.remove(f'IR{self.animation_ctr-1}.png')

    def reset(self):
        # Reset results and log:
        clear_log(logger='logger_window##logger')
        set_table_item('performance_window##table', 0, 1, '...')
        set_table_item('performance_window##table', 1, 1, '...')
        set_table_item('performance_window##table', 2, 1, '...')
        set_table_item('performance_window##table', 3, 1, '...')
        add_stem_series('performance_window##plot', 'IPC', [0.0], [0.0])
        set_value('performance_window##ipc_data', '...')

    def create_config_window(self):
        with window('config_window', label='Config', x_pos=0, y_pos=0, width=400, height=640):
            add_text('Graph')
            add_button("config_window##load_ir_button", label='Select IR file', callback=(lambda s, d: open_file_dialog(self.cb_config_load_dot, ".dot,.DOT")))

            add_same_line(spacing=20)
            add_text('config_window##count1', default_value='0', color=[0,255,0])
            add_same_line(spacing=5)
            add_text('blocks')
            add_same_line(spacing=20)
            add_text('config_window##count2', default_value='0', color=[0,255,0])
            add_same_line(spacing=5)
            add_text('nodes')
            add_same_line(spacing=20)
            add_text('config_window##count3', default_value='0', color=[0,255,0])
            add_same_line(spacing=5)
            add_text('wires')

            add_spacing(count=2)
            add_separator()
            add_spacing(count=2)

            add_text('Parameters')

            with tab_bar('parameter_tabs'):
                with tab('parameter_tab_latency', label='Latency'):
                    add_text('parameter_tab_latency##group1', default_value='Communication')
                    with child('parameter_tab_latency##child1', border=True, autosize_x=True, height=90):
                        add_input_int('parameter_l_com',    width=200,  min_value=0,    default_value=Config.Latency.communication, callback=self.cb_parameter_latency, callback_data='communication',  label='wire')
                        add_input_int('parameter_l_meml',   width=200,  min_value=0,    default_value=Config.Latency.mem_load,      callback=self.cb_parameter_latency, callback_data='mem_load',       label='Memory load')
                        add_input_int('parameter_l_mems',   width=200,  min_value=0,    default_value=Config.Latency.mem_store,     callback=self.cb_parameter_latency, callback_data='mem_store',      label='Memory store')

                    add_spacing(count=3)
                    add_text('parameter_tab_latency##group2', default_value='Operations')
                    with child('parameter_tab_latency##child2', border=True, autosize_x=True, height=155):

                        add_text('parameter_tab_latency##text3', default_value='Latency')
                        add_same_line(xoffset=210)
                        add_text('parameter_tab_latency##text4', default_value='Operator')

                        add_input_int('parameter_l_plus',   width=200,  min_value=0,    default_value=Config.Latency.computation[Operator.ADD], callback=self.cb_parameter_latency_comp,    callback_data=Operator.ADD,    label='+ (add)')
                        add_input_int('parameter_l_sub',    width=200,  min_value=0,    default_value=Config.Latency.computation[Operator.SUB], callback=self.cb_parameter_latency_comp,    callback_data=Operator.SUB,    label='- (subtract)')
                        add_input_int('parameter_l_mul',    width=200,  min_value=0,    default_value=Config.Latency.computation[Operator.MUL], callback=self.cb_parameter_latency_comp,    callback_data=Operator.MUL,    label='* (multiply)')
                        add_input_int('parameter_l_div',    width=200,  min_value=0,    default_value=Config.Latency.computation[Operator.DIV], callback=self.cb_parameter_latency_comp,    callback_data=Operator.DIV,    label='/ (divide)')
                        add_input_int('parameter_l_mod',    width=200,  min_value=0,    default_value=Config.Latency.computation[Operator.MOD], callback=self.cb_parameter_latency_comp,    callback_data=Operator.MOD,    label='% (modulo)')
                        add_input_int('parameter_l_lt',     width=200,  min_value=0,    default_value=Config.Latency.computation[Operator.LT],  callback=self.cb_parameter_latency_comp,    callback_data=Operator.LT,     label='< (less than)')
                        add_input_int('parameter_l_le',     width=200,  min_value=0,    default_value=Config.Latency.computation[Operator.LE],  callback=self.cb_parameter_latency_comp,    callback_data=Operator.LE,     label='<= (less or equal)')
                        add_input_int('parameter_l_gt',     width=200,  min_value=0,    default_value=Config.Latency.computation[Operator.GT],  callback=self.cb_parameter_latency_comp,    callback_data=Operator.GT,     label='> (greater than)')
                        add_input_int('parameter_l_ge',     width=200,  min_value=0,    default_value=Config.Latency.computation[Operator.GE],  callback=self.cb_parameter_latency_comp,    callback_data=Operator.GE,     label='>= (greater or equal)')
                        add_input_int('parameter_l_eq',     width=200,  min_value=0,    default_value=Config.Latency.computation[Operator.EQ],  callback=self.cb_parameter_latency_comp,    callback_data=Operator.EQ,     label='== (equal to)')
                        add_input_int('parameter_l_ne',     width=200,  min_value=0,    default_value=Config.Latency.computation[Operator.NE],  callback=self.cb_parameter_latency_comp,    callback_data=Operator.NE,     label='!= (not equal to)')
                        add_input_int('parameter_l_neg',    width=200,  min_value=0,    default_value=Config.Latency.computation[Operator.NEG], callback=self.cb_parameter_latency_comp,    callback_data=Operator.NEG,    label='- (negation)')
                        add_input_int('parameter_l_not',    width=200,  min_value=0,    default_value=Config.Latency.computation[Operator.NOT], callback=self.cb_parameter_latency_comp,    callback_data=Operator.NOT,    label='! (not)')

                    add_spacing(count=3)
                    add_text('parameter_tab_latency##group3', default_value='Nodes')
                    with child('parameter_tab_latency##child3', border=True, autosize_x=True, height=160):

                        add_text('parameter_tab_latency##text5', default_value='Latency')
                        add_same_line(xoffset=210)
                        add_text('parameter_tab_latency##text6', default_value='Node')

                        add_input_int('parameter_l_eta',        width=200,  default_value=Config.Latency.eta,            callback=self.cb_parameter_latency,     callback_data='eta',       label='ETA',        min_value=0)
                        add_input_text('parameter_l_mu',        width=200,  default_value=Config.Latency.mu_str,         callback=self.cb_parameter_latency_f,   callback_data='mu',        label='Mu',         tip='n: amount of inputs')
                        add_input_text('parameter_l_mux',       width=200,  default_value=Config.Latency.mux_str,        callback=self.cb_parameter_latency_f,   callback_data='mux',       label='Mux',        tip='n: amount of inputs')
                        add_input_text('parameter_l_combine',   width=200,  default_value=Config.Latency.combine_str,    callback=self.cb_parameter_latency_f,   callback_data='combine',   label='Combine',    tip='n: amount of inputs')
                        add_input_text('parameter_l_xor',       width=200,  default_value=Config.Latency.xor_str,        callback=self.cb_parameter_latency_f,   callback_data='xor',       label='XOR',        tip='n: amount of inputs')


                with tab('parameter_tab_energy', label='Energy'):
                    add_text('parameter_tab_energy##group1', default_value='Communication')
                    with child('parameter_tab_energy##child1', border=True, autosize_x=True, height=90):
                        add_input_int('parameter_e_com',    width=200,  min_value=0,    default_value=Config.Energy.communication, callback=self.cb_parameter_energy, callback_data='communication',  label='wire')
                        add_input_int('parameter_e_meml',   width=200,  min_value=0,    default_value=Config.Energy.mem_load,      callback=self.cb_parameter_energy, callback_data='mem_load',       label='Memory load')
                        add_input_int('parameter_e_mems',   width=200,  min_value=0,    default_value=Config.Energy.mem_store,     callback=self.cb_parameter_energy, callback_data='mem_store',      label='Memory store')

                    add_spacing(count=3)
                    add_text('parameter_tab_energy##group2', default_value='Operations')
                    with child('parameter_tab_energy##child2', border=True, autosize_x=True, height=155):

                        add_text('parameter_tab_energy##text3', default_value='Energy (pJ)')
                        add_same_line(xoffset=210)
                        add_text('parameter_tab_energy##text4', default_value='Operator')

                        add_input_int('parameter_e_plus',   width=200,  min_value=0,    default_value=Config.Energy.computation[Operator.ADD], callback=self.cb_parameter_energy_comp,    callback_data=Operator.ADD,    label='+ (add)')
                        add_input_int('parameter_e_sub',    width=200,  min_value=0,    default_value=Config.Energy.computation[Operator.SUB], callback=self.cb_parameter_energy_comp,    callback_data=Operator.SUB,    label='- (subtract)')
                        add_input_int('parameter_e_mul',    width=200,  min_value=0,    default_value=Config.Energy.computation[Operator.MUL], callback=self.cb_parameter_energy_comp,    callback_data=Operator.MUL,    label='* (multiply)')
                        add_input_int('parameter_e_div',    width=200,  min_value=0,    default_value=Config.Energy.computation[Operator.DIV], callback=self.cb_parameter_energy_comp,    callback_data=Operator.DIV,    label='/ (divide)')
                        add_input_int('parameter_e_mod',    width=200,  min_value=0,    default_value=Config.Energy.computation[Operator.MOD], callback=self.cb_parameter_energy_comp,    callback_data=Operator.MOD,    label='% (modulo)')
                        add_input_int('parameter_e_lt',     width=200,  min_value=0,    default_value=Config.Energy.computation[Operator.LT],  callback=self.cb_parameter_energy_comp,    callback_data=Operator.LT,     label='< (less than)')
                        add_input_int('parameter_e_le',     width=200,  min_value=0,    default_value=Config.Energy.computation[Operator.LE],  callback=self.cb_parameter_energy_comp,    callback_data=Operator.LE,     label='<= (less or equal)')
                        add_input_int('parameter_e_gt',     width=200,  min_value=0,    default_value=Config.Energy.computation[Operator.GT],  callback=self.cb_parameter_energy_comp,    callback_data=Operator.GT,     label='> (greater than)')
                        add_input_int('parameter_e_ge',     width=200,  min_value=0,    default_value=Config.Energy.computation[Operator.GE],  callback=self.cb_parameter_energy_comp,    callback_data=Operator.GE,     label='>= (greater or equal)')
                        add_input_int('parameter_e_eq',     width=200,  min_value=0,    default_value=Config.Energy.computation[Operator.EQ],  callback=self.cb_parameter_energy_comp,    callback_data=Operator.EQ,     label='== (equal to)')
                        add_input_int('parameter_e_ne',     width=200,  min_value=0,    default_value=Config.Energy.computation[Operator.NE],  callback=self.cb_parameter_energy_comp,    callback_data=Operator.NE,     label='!= (not equal to)')
                        add_input_int('parameter_e_neg',    width=200,  min_value=0,    default_value=Config.Energy.computation[Operator.NEG], callback=self.cb_parameter_energy_comp,    callback_data=Operator.NEG,    label='- (negation)')
                        add_input_int('parameter_e_not',    width=200,  min_value=0,    default_value=Config.Energy.computation[Operator.NOT], callback=self.cb_parameter_energy_comp,    callback_data=Operator.NOT,    label='! (not)')

                    add_spacing(count=3)
                    add_text('parameter_tab_energy##group3', default_value='Nodes')
                    with child('parameter_tab_energy##child3', border=True, autosize_x=True, height=160):

                        add_text('parameter_tab_energy##text5', default_value='Energy (pJ)')
                        add_same_line(xoffset=210)
                        add_text('parameter_tab_energy##text6', default_value='Node')

                        add_input_int('parameter_e_eta',        width=200,  default_value=Config.Energy.communication,  callback=self.cb_parameter_energy,     callback_data='eta',       label='ETA',        min_value=0,)
                        add_input_text('parameter_e_mu',        width=200,  default_value=Config.Energy.mu_str,         callback=self.cb_parameter_energy_f,   callback_data='mu',        label='Mu',         tip='n: amount of inputs')
                        add_input_text('parameter_e_mux',       width=200,  default_value=Config.Energy.mux_str,        callback=self.cb_parameter_energy_f,   callback_data='mux',       label='Mux',        tip='n: amount of inputs')
                        add_input_text('parameter_e_combine',   width=200,  default_value=Config.Energy.combine_str,    callback=self.cb_parameter_energy_f,   callback_data='combine',   label='Combine',    tip='n: amount of inputs')
                        add_input_text('parameter_e_xor',       width=200,  default_value=Config.Energy.xor_str,        callback=self.cb_parameter_energy_f,   callback_data='xor',       label='XOR',        tip='n: amount of inputs')

    def create_memory_window(self):
        with window('memory_window', label='Memory', x_pos=0, y_pos=650, width=400, height=265):
            add_button('memory_window##load', label='Load JSON', callback=(lambda s,d: open_file_dialog(self.cb_memory_table_load, ".json,.*")))

            add_same_line(xoffset=200)
            add_button('memory_window##save', callback=self.cb_memory_table_save, label='Save state')
            add_same_line()
            add_button('memory_window##revert', callback=self.cb_memory_table_revert, label='Revert state')

            add_spacing(count=3)

            with child('memory_window##table', border=False, autosize_x=True, height=165):
                with managed_columns('memory_window##table_head', 3):
                    add_text('Identifier')
                    add_text('Indices')
                    add_text('Value')

            add_dummy()
            add_same_line(spacing=8)
            add_button('memory_window##add_row', small=True, callback=self.cb_memory_table_add_row, label='Add row')

    def memory_table_add_row(self, identifier='', indices='', value=''):
        configure_item('memory_window', label='Memory (not saved)')


        self.mem_table_data.append([identifier, indices, value])
        row_str = str(self.mem_table_rows)

        with managed_columns(f'memory_window##table_row{row_str}', 3, parent='memory_window##table'):
            add_input_text(f"##memory_window##table_row{row_str}_0", callback=self.cb_memory_table_update, default_value=identifier, width=-1)
            add_input_text(f"##memory_window##table_row{row_str}_1", callback=self.cb_memory_table_update, default_value=indices, width=-1)
            add_input_text(f"##memory_window##table_row{row_str}_2", callback=self.cb_memory_table_update, default_value=value, width=-1)

        self.mem_table_rows += 1

    def cb_memory_table_update(self, sender, data):
        configure_item('memory_window', label='Memory (not saved)')

    def cb_memory_table_add_row(self, sender, data):
        self.memory_table_add_row()

    def cb_memory_table_load(self, sender, data):
        configure_item('memory_window', label='Memory (not saved)')
        dir_, file_ = data

        with open(f'{dir_}/{file_}') as f:
            # We expect a json array with each memory item an array consisting of
            # an identifier, indices (can be []) and a value. For example:
            # [a, [], 123]
            # [b, [1,2], true]
            json_mem = json.load(f)

            for identifier, indices, value in json_mem:
                self.log_mem(value, identifier, indices)

        self.cb_memory_table_save(None, None)


    def cb_memory_table_save(self, sender, data):
        try:
            for r in range(self.mem_table_rows):
                identifier = get_value(f"##memory_window##table_row{r}_0")
                indices = get_value(f"##memory_window##table_row{r}_1")
                value = get_value(f"##memory_window##table_row{r}_2")

                self.mem_table_data[r][0] = identifier
                self.mem_table_data[r][1] = indices
                self.mem_table_data[r][2] = value

                # print('save', identifier)
                self.simulation.mem.store(eval(value), identifier, eval(indices) if indices else None)

            # print('DUMP')
            # print(self.mem_table_data)
            # self.simulation.mem.dump()

            configure_item('memory_window', label='Memory (saved)')
        except SyntaxError:
            log_error('Memory could not be saved (SyntaxError)', logger='logger_window##logger')

    def cb_memory_table_revert(self, sender, data):
        configure_item('memory_window', label='Memory (not saved)')

        for r in range(self.mem_table_rows):
            set_value(f"##memory_window##table_row{r}_0", self.mem_table_data[r][0])
            set_value(f"##memory_window##table_row{r}_1", self.mem_table_data[r][1])
            set_value(f"##memory_window##table_row{r}_2", self.mem_table_data[r][2])


    def log_mem(self, value, identifier, indices=None):
        for i,r in enumerate(self.mem_table_data):
            if r[0] == identifier:
                if indices:
                    if indices == eval(r[1]):
                        set_value(f"##memory_window##table_row{i}_2", str(value))
                        return
                else:
                    set_value(f"##memory_window##table_row{i}_2", str(value))
                    return

        # Memory table was not updated, so a new entry must be inserted.
        self.memory_table_add_row(str(identifier), str(indices) if indices else '', str(value))

    def create_graph_window(self):
        with window('graph_window', label='Intermediate Representation'):
            add_plot("graph_window##plot", no_legend=True, equal_aspects=True, anti_aliased=True, no_mouse_pos=True, yaxis_no_tick_labels=True, yaxis_no_tick_marks=True, xaxis_no_tick_labels=True, xaxis_no_tick_marks=True, label='Intermediate representation  (green=busy, red=computing)')
            self.update_graph()


    def create_editor_window(self):
        pass

    def create_control_window(self):
        with window('control_window', label='Control', x_pos=1150, y_pos=0, width=500, height=145):

            add_text('Exit condition')

            add_checkbox('control_window##stop_after_check', default_value=False, callback=self.cb_control_stop_after, label='stop after')
            add_same_line()
            add_input_int('control_window##stop_after_cycles', width=100, min_value=1, default_value=100, callback=self.cb_control_stop_after_cycles, enabled=False, label='cycles')

            add_same_line(spacing=20)
            add_checkbox('control_window##animation_check', default_value=True, label='Animate graph')

            add_spacing(count=2)
            add_separator()
            add_spacing(count=2)

            add_text('Control')

            add_button('control_window_button##run', callback=self.cb_control_run, label='Run')
            add_same_line()
            add_button('control_window_button##step', callback=self.cb_control_step, label='Step')
            add_same_line()
            add_button('control_window_button##halt', callback=self.cb_control_halt, label='Halt')
            set_item_color('control_window_button##halt', mvGuiCol_Button, [150,0,0])
            set_item_color('control_window_button##halt', mvGuiCol_ButtonHovered, [200,0,0])
            set_item_color('control_window_button##halt', mvGuiCol_ButtonActive, [255,0,0])
            add_same_line()
            add_button('control_window_button##reset', callback=self.cb_control_reset, label='Reset')
            set_item_color('control_window_button##reset', mvGuiCol_Button, [0,150,0])
            set_item_color('control_window_button##reset', mvGuiCol_ButtonHovered, [0,200,0])
            set_item_color('control_window_button##reset', mvGuiCol_ButtonActive, [0,255,0])


    def create_logger_window(self):
        with window('logger_window', label='Logging', x_pos=1150, y_pos=155, width=500, height=385):
            with group('logger_window##group2'):
                add_text('Only show log type ...')
                add_same_line()

                logger_help_msg = 'and logs of higher importance'
                add_text('(?)'+logger_help_msg, color=[150, 150, 150], default_value='(?)')
                add_tooltip('(?)'+logger_help_msg, logger_help_msg + 'tip')
                add_text(logger_help_msg)
                end()

                add_radio_button('logger_window##log_type', horizontal=True, items=('Trace', 'Debug', 'Info', 'Warning', 'Error', 'Off'), callback=self.cb_logger_type)

            add_spacing(count=2)
            add_separator()
            add_spacing(count=2)

            add_logger('logger_window##logger', log_level=0, autosize_x=True, height=230, auto_scroll=True)
            clear_log(logger='logger_window##logger')

    def create_performance_window(self):
        with window('performance_window', label='Performance', x_pos=1150, y_pos=550, width=500, height=365):
            add_table('performance_window##table', ['Metric', 'Result'], height=105)
            add_row('performance_window##table', ['Total cycle count', '...'])
            add_row('performance_window##table', ['Total enery consumption (pJ)', '...'])
            add_row('performance_window##table', ['Average utilization (%)', '...'])
            add_row('performance_window##table', ['Simulator run-time (s)', '...'])

            add_plot('performance_window##plot', height=190, label='Instructions Per Cycle (IPC)', no_legend=True)

            add_text('Raw:')
            add_same_line()
            add_input_text('performance_window##ipc_data', width=-2, readonly=True, default_value='...', label='')

            # add_button('performance_window##button', label='Raw IPC data')
            # with popup('performance_window##button', 'IPC data##modal', modal=True, mousebutton=0, width=500):
                    # add_input_text('performance_window##ipc_data',  multiline=True, readonly=True, height=20, default_value='...')
                    # add_button("performance_window##close_button", callback=self.cb_performance_close_modal, label='Close')

    def cb_config_load_dot(self, sender, data):
        dir_, file_ = data
        self.simulation.graph = IR.from_DOT(f'{dir_}/{file_}')
        set_value('config_window##count1', str(len(self.simulation.graph.blocks)-1))
        set_value('config_window##count2', str(len(self.simulation.graph.nodes)))
        set_value('config_window##count3', str(len(self.simulation.graph.wires)))

        self.reset()
        self.update_graph()

    def cb_parameter_latency(self, sender, data):
        setattr(Config.Latency, data, int(get_value(sender)))

    def cb_parameter_latency_comp(self, sender, data):
        Config.Latency.computation[data] = int(get_value(sender))

    def cb_parameter_latency_f(self, sender, data):
        try:
            setattr(Config.Latency, data, eval(get_value(sender)))
        except SyntaxError:
            pass


    def cb_parameter_energy(self, sender, data):
        setattr(Config.Energy, data, int(get_value(sender)))

    def cb_parameter_energy_comp(self, sender, data):
        Config.Energy.computation[data] = int(get_value(sender))

    def cb_parameter_energy_f(self, sender, data):
        setattr(Config.Energy, data, eval(get_value(sender)))



    def cb_control_stop_after(self, sender, data):
        if not get_value(sender):
            self.simulation.stop_after = None

        configure_item('control_window##stop_after_cycles', enabled=get_value(sender))

    def cb_control_stop_after_cycles(self, sender, data):
        self.simulation.stop_after = get_value(sender)

    def cb_control_run(self, sender, data):
        if self.simulation.graph is not None:
            self.simulation.run()
            self.show_statistics()
            self.show_IPC()

    def cb_control_step(self, sender, data):
        if self.simulation.graph is not None:
            self.simulation.step()
            self.show_statistics()
            self.show_IPC()
            self.update_graph()

    def cb_control_halt(self, sender, data):
        self.simulation.halt_now = True

    def cb_control_reset(self, sender, data):
        if self.simulation.graph is not None:
            # Reset GUI (except graph, which depends on the simulator reset)
            self.reset()

            # Reset sim:
            self.simulation.reset()

            # Reset graph explorer:
            self.update_graph()

    def cb_logger_type(self, sender, data):
        set_log_level(get_value(sender), logger='logger_window##logger')

    def log(self, cycle, level, msg):
        msg = f'[{cycle}] {msg}'

        if level == 'trace':
            log(msg, logger='logger_window##logger')
        elif level == 'debug':
            log_debug(msg, logger='logger_window##logger')
        elif level == 'info':
            log_info(msg, logger='logger_window##logger')
        elif level == 'warning':
            log_warning(msg, logger='logger_window##logger')
        elif level == 'error':
            log_error(msg, logger='logger_window##logger')


    def cb_performance_close_modal(self, sender, data):
        close_popup("IPC data##modal")

    def show_IPC(self):
        ipc_series = self.simulation.get_ipc_series()
        plot_x = [float(x) for x in range(1,len(ipc_series)+1)]
        plot_y = [float(y) for y in ipc_series]

        add_stem_series('performance_window##plot', 'IPC', plot_x, plot_y, update_bounds=True)

        set_value('performance_window##ipc_data', str(ipc_series))

    def show_statistics(self):
        (total_cycle_count, total_energy, avg_utilization, runtime) = self.simulation.get_end_statistics()

        set_table_item('performance_window##table', 0, 1, str(total_cycle_count))
        set_table_item('performance_window##table', 1, 1, str(total_energy))
        set_table_item('performance_window##table', 2, 1, str(avg_utilization))
        set_table_item('performance_window##table', 3, 1, str(runtime))

    def update_graph(self):
        if get_value('control_window##animation_check'):
            filename = self.simulation.graph.to_stylizedPNGfile(f'IR{self.animation_ctr}.png')
            series_name = 'graph_window##plot_graph' + str(self.animation_ctr)

            if self.animation_ctr == 1:
                add_image_series('graph_window##plot', series_name, filename, bounds_min=[0,0], bounds_max=get_main_window_size())
            else:
                add_image_series('graph_window##plot', series_name, filename, bounds_min=[0,0], bounds_max=get_main_window_size(), update_bounds=False)
                os.remove(f'IR{self.animation_ctr-1}.png')

            self.animation_ctr += 1


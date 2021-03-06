import tkinter as tk
from gui.table import Table
from utils.patterns.observable import Observable
from input.window import DEFAULT_SIZE_X

class MasterGUI(tk.Tk, Observable):
    def __init__(self):
        tk.Tk.__init__(self)
        Observable.__init__(self)
        self.geometry(f"800x700+{DEFAULT_SIZE_X + 20}+0")
        self.resizable(0, 0)
        self.observers = []

        tk.Label(self, text="Actions", width=20).grid(column=0, row=0, columnspan=3, sticky="n")
        # tk.Label(self, text="GameMapStatus").grid(column=1, row=0)
        self.player_infos = []
        for i in range(10):
            label = tk.Label(self, text="-", borderwidth=0, width=20)
            label.grid(row=(1 + i), column=0, padx=0, rowspan=1, columnspan=3, sticky="n")
            self.player_infos.append(label)

        self.fighting_state = tk.Label(self, text="Not fighting", background='green', borderwidth=0, width=10)
        self.fighting_state.grid(row=(1 + 10 + 1), column=0, sticky="n", padx=0, rowspan=2, columnspan=3)
        self.set_config_buttons()

        self.table = None
        self.player = None
        self.init_table(32, 32)

    def set_fighting_state(self, state):
        if state:
            self.fighting_state.configure(text="Fighting", background='yellow')
        else:
            self.fighting_state.configure(text="Not Fighting", background='green')

    def update_player_info(self, entity):
        i = 0
        for key in entity.__dict__.keys():
            if i < len(self.player_infos):
                text = '{}: {}'.format(key, entity.__dict__[key])
                self.player_infos[i].configure(text=text)
            i += 1

    def set_config_buttons(self):
        button = tk.Button(self, text="Searching Mob: False", borderwidth=0, width=20)
        button.grid(row=15, column=0, sticky="nw", padx=0)
        button.bind("<Button-1>", lambda e: self.dispatch({"ref": button}, "flag_search_mob"))

        button_graph = tk.Button(self, text="Debug Graph: False", borderwidth=0, width=20)
        button_graph.grid(row=16, column=0, sticky="nw", padx=0)
        button_graph.bind("<Button-1>", lambda e: self.dispatch({"ref": button_graph}, "flag_debug_graph"))

        button_sight = tk.Button(self, text="Debug Sight: False", borderwidth=0, width=20)
        button_sight.grid(row=17, column=0, sticky="nw", padx=0)
        button_sight.bind("<Button-1>", lambda e: self.dispatch({"ref": button_sight}, "flag_debug_sight"))

    def init_table(self, width, height):
        if self.table:
            self.table.pack_forget()
            self.table.destroy()
        self.table = Table(self, rows=height, columns=width)
        self.table.grid(row=1, column=3, rowspan=height)

    def onAfter(self):
        # self.grid(sticky=tk.N+tk.S)
        # self.pack_slaves()
        pass

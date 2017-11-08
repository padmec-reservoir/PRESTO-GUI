import pint
from sys import exit
from configobj import ConfigObj
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtGui import QIcon
from MyAction import MyAction
from MyTableWidget import MyTableWidget


class MyWindow(QMainWindow):
    def __init__(self, parameter_list, fluids, mesh):
        super(MyWindow, self).__init__()
        self.parameter_list = parameter_list
        self.fluids = fluids
        self.mesh = mesh
        self.setGeometry(50, 50, 700, 500)
        self.setWindowTitle("PRESTO - Python Reservoir Simulation Toolbox")
        self.setWindowIcon(QIcon('presto-logo2.png'))
        self.ureg = pint.UnitRegistry()
        # Menubar
        self.main_menu = self.menuBar()
        self.file_menu = self.main_menu.addMenu("&File")
        self.file_menu.addAction(
            MyAction(
                self,
                "&Exit",
                "Ctrl+Q",
                "Leave the app",
                exit))
        self.file_menu.addAction(
            MyAction(
                self,
                "&Open File",
                "Ctrl+O",
                "Open existing paramter file",
                self.open_file))
        self.file_menu.addAction(
            MyAction(
                self,
                "&Save File",
                "Ctrl+S",
                "Save current parameters",
                self.save_file))

        # Statusbar
        self.statusBar()

        # Tabs
        self.table = MyTableWidget(self, self.parameter_list,
                                   self.fluids, self.mesh)
        self.setCentralWidget(self.table)

    def open_file(self):
        name = QFileDialog.getOpenFileName(self, 'Open File')
        if not name[0]:
            return
        config_file = ConfigObj(name[0])
        self.table.checked_units.clear()
        for x in config_file["systems"]:
            self.table.checked_units.add(int(x))
        for x in self.parameter_list:
            self.table.tab1.value[x[0]] = config_file["tab1"]["values"][x[0]]
            self.table.tab1.unit[x[0]] = config_file["tab1"]["units"][x[0]]
        for x in self.fluids:
            self.table.tab2.oil.value[x[0]] = config_file["tab2"]["oil"]["values"][x[0]]
            self.table.tab2.oil.unit[x[0]] = config_file["tab2"]["oil"]["units"][x[0]]
            self.table.tab2.water.value[x[0]] = config_file["tab2"]["water"]["values"][x[0]]
            self.table.tab2.water.unit[x[0]] = config_file["tab2"]["water"]["units"][x[0]]
        for x in self.mesh:
            self.table.tab5.value[x[0]] = config_file["tab5"]["values"][x[0]]
            self.table.tab5.unit[x[0]] = config_file["tab5"]["units"][x[0]]
        self.table.update_parameters()
        self.table.update_wells(config_file["tab4"])

    def save_file(self):
        # Need data validation on values and units
        name = QFileDialog.getSaveFileName(self, 'Save File')
        if not name[0]:
            return
        config_file = ConfigObj(name[0])
        config_file["systems"] = []
        config_file["tab1"] = {}
        config_file["tab1"]["values"] = {}
        config_file["tab1"]["units"] = {}
        config_file["tab2"] = {}
        config_file["tab2"]["oil"] = {}
        config_file["tab2"]["oil"]["values"] = {}
        config_file["tab2"]["oil"]["units"] = {}
        config_file["tab2"]["water"] = {}
        config_file["tab2"]["water"]["values"] = {}
        config_file["tab2"]["water"]["units"] = {}
        config_file["tab4"] = {}
        config_file["tab4"]["inpos"] = {}
        config_file["tab4"]["outpos"] = {}
        config_file["tab5"] = {}
        config_file["tab5"]["values"] = {}
        config_file["tab5"]["units"] = {}
        for x in self.table.checked_units:
            config_file["systems"].append(x)
        for x in self.parameter_list:
            config_file["tab1"]["values"][x[0]] = self.table.tab1.value[x[0]]
            config_file["tab1"]["units"][x[0]] = self.table.tab1.unit[x[0]]
        for x in self.fluids:
            config_file["tab2"]["oil"]["values"][x[0]] = self.table.tab2.oil.value[x[0]]
            config_file["tab2"]["oil"]["units"][x[0]] = self.table.tab2.oil.unit[x[0]]
            config_file["tab2"]["water"]["values"][x[0]] = self.table.tab2.water.value[x[0]]
            config_file["tab2"]["water"]["units"][x[0]] = self.table.tab2.water.unit[x[0]]
        for x in self.table.tab4.inpos:
            config_file["tab4"]["inpos"][x] = self.table.tab4.inpos[x]
        for x in self.table.tab4.outpos:
            config_file["tab4"]["outpos"][x] = self.table.tab4.outpos[x]
        for x in self.mesh:
            config_file["tab5"]["values"][x[0]] = self.table.tab5.value[x[0]]
            config_file["tab5"]["units"][x[0]] = self.table.tab5.unit[x[0]]
        config_file.write()

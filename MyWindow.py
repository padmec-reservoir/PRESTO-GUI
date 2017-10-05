import pint
from sys import exit
from configobj import ConfigObj
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtGui import QIcon
from MyAction import MyAction
from MyTableWidget import MyTableWidget


class MyWindow(QMainWindow):
    def __init__(self, parameter_list):
        super(MyWindow, self).__init__()
        self.parameter_list = parameter_list
        self.value = dict((x[0], 0) for x in self.parameter_list)
        self.unit = dict((x[0], "") for x in self.parameter_list)
        self.setGeometry(50, 50, 700, 500)
        self.setWindowTitle("PRESTO - Python Reservoir Simulation Toolbox")
        self.setWindowIcon(QIcon('presto-logo.png'))
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
        self.table_widget = MyTableWidget(self, self.parameter_list)
        self.setCentralWidget(self.table_widget)

    def open_file(self):
        name = QFileDialog.getOpenFileName(self, 'Open File')
        config_file = ConfigObj(name[0])
        for x in self.parameter_list:
            self.value[x[0]] = config_file["values"][x[0]]
            self.unit[x[0]] = config_file["units"][x[0]]
        self.table_widget.update_parameters()

    def save_file(self):
        # Need data validation on values and units
        name = QFileDialog.getSaveFileName(self, 'Save File')
        config_file = ConfigObj(name[0])
        config_file["values"] = {}
        config_file["units"] = {}
        for x in self.parameter_list:
            config_file["values"][x[0]] = self.value[x[0]]
            config_file["units"][x[0]] = self.unit[x[0]]
        config_file.write()

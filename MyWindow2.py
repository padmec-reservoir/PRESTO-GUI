from sys import exit
from configobj import ConfigObj
from parameters import (si_units, imperial_units, field_units, units_systems,
                        start_unit, parameter_list, fluids, mesh, fields,
                        permcamp)
from MyAction import MyAction
from MyTree import MyTree
from PyQt5.QtWidgets import (QMainWindow, QWidget, QGridLayout)
from PyQt5.QtGui import QIcon
'''
Problem
    Dimensionality
Physical/Mathematical Model
    Reservoir
Geometry
    Mesh
Wells (Geometry)
Physical Properties
    Rock (K, Φ)
    Fluid
    Rock (Flux, ρ, k)
Analisys Interval
Initial Conditions
Boundary Conditions
    Injection/Producer
    Aquifer
Numerical Methods
Output Configuration
    Interval
    Variables
'''

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(50, 50, 1000, 500)
        self.setWindowTitle("PRESTO - Python Reservoir Simulation Toolbox")
        self.setWindowIcon(QIcon('presto-logo2.png'))
        self.main_menu = self.menuBar()
        self.file_menu = self.main_menu.addMenu("&File")
        self.file_menu.addAction(
            MyAction(
                self,
                "&Exit",
                "Ctrl+Q",
                "Leave the app",
                exit))
        self.statusBar()
        self.main_widget = QWidget(self)
        self.main_widget.layout = QGridLayout(self.main_widget)
        self.tree = MyTree(self, "PRESTO GUI")
        self.main_widget.layout.addWidget(self.tree, 1, 1)
        self.setCentralWidget(self.main_widget)

from sys import exit
from configobj import ConfigObj
from MyAction import MyAction
from MyTree import MyTree
from PyQt5.QtWidgets import (QMainWindow, QWidget, QGridLayout, QFileDialog)
from PyQt5.QtGui import QIcon


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
        self.file_menu.addAction(
            MyAction(
                self,
                "&Save File...",
                "Ctrl+S",
                "Save current parameters",
                self.save_file))
        self.file_menu.addAction(
            MyAction(
                self,
                "&Open File...",
                "Ctrl+O",
                "Open existing parameter file",
                self.open_file))
        self.statusBar()
        self.main_widget = QWidget(self)
        self.main_widget.layout = QGridLayout(self.main_widget)
        self.tree = MyTree(self, "PRESTO GUI")
        self.main_widget.layout.addWidget(self.tree, 1, 1)
        self.setCentralWidget(self.main_widget)

    def save_file(self):
        name = QFileDialog.getSaveFileName(self, 'Save File')
        if not name[0]:
            return
        arq = ConfigObj(name[0])
        arq["Units"] = self.tree.get_units()
        for x in self.tree.roots:
            cur = self.tree.roots[x]
            arq[x] = {}
            values, units = cur.get_data()
            arq[x]["values"] = values
            arq[x]["units"] = units
            for y in cur.itens:
                arq[x][y] = {}
                values, units = cur.itens[y].get_data()
                arq[x][y]["values"] = values
                arq[x][y]["units"] = units
        arq.write()

    def open_file(self):
        name = QFileDialog.getOpenFileName(self, 'Open File')
        if not name[0]:
            return
        arq = ConfigObj(name[0])
        self.tree.load_units(arq["Units"])
        del(arq["Units"])
        for x in arq:
            cur = self.tree.roots[x]
            values = arq[x]["values"]
            units = arq[x]["units"]
            cur.set_data(values, units)
            sub = [k for k in arq[x] if (k != "values" and k != "units")]
            for y in sub:
                if (x == "Wells (Geometry)"):
                    self.tree.make_well(None, y)
                values = arq[x][y]["values"]
                units = arq[x][y]["units"]
                cur.itens[y].set_data(values, units)

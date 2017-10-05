import sys
import pint
from PyQt5.QtCore import *
from PyQt5.QtWidgets import (QMainWindow, QApplication, QAction, QGridLayout,
                             QFileDialog, QTabWidget, QComboBox, QLabel,
                             QLineEdit, QTreeWidget, QTreeWidgetItem, QWidget)
from PyQt5.QtGui import QIcon
from configobj import ConfigObj
from parameters import *


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.value = dict((x[0], 0) for x in parameter_list)
        self.unit = dict((x[0], "") for x in parameter_list)
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
                sys.exit))
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
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

        # Show
        self.show()

    def open_file(self):
        name = QFileDialog.getOpenFileName(self, 'Open File')
        config_file = ConfigObj(name[0])
        for x in parameter_list:
            self.value[x[0]] = config_file["values"][x[0]]
            self.unit[x[0]] = config_file["units"][x[0]]
        self.table_widget.update_parameters()

    def save_file(self):
        # Need data validation on values and units
        name = QFileDialog.getSaveFileName(self, 'Save File')
        config_file = ConfigObj(name[0])
        config_file["values"] = {}
        config_file["units"] = {}
        for x in parameter_list:
            config_file["values"][x[0]] = self.value[x[0]]
            config_file["units"][x[0]] = self.unit[x[0]]
        config_file.write()


class MyAction(QAction):
    def __init__(self, parent, name, shortcut, status, function):
        super(MyAction, self).__init__(name, parent)
        self.setShortcut(shortcut)
        self.setStatusTip(status)
        self.triggered.connect(function)


class MyTableWidget(QTabWidget):
    def __init__(self, parent):
        super(MyTableWidget, self).__init__(parent)
        self.parent = parent
        # Define layout
        self.layout = QGridLayout(self)
        # Make first tab
        self.tab1 = QWidget(self)
        # Define layout of tab 1
        self.tab1.layout = self.make_tab1_layout()
        # Make second tab
        self.tab2 = QWidget(self)
        # Define layout of tab 2
        self.tab2.tree_view = self.make_tab2_tree(self.tab2)
        # Add tabs to tab screen
        self.addTab(self.tab1, "Tab 1")
        self.addTab(self.tab2, "Tab 2")

    def make_labels(self, parent):
        labels = {}
        for x in parameter_list:
            labels[x[0]] = QLabel(x[0], parent)
        return labels

    def make_inputs(self, parent):
        inputs = {}
        for x in parameter_list:
            inputs[x[0]] = QLineEdit(parent)
            inputs[x[0]].textEdited.connect(self.get_value)
        return inputs

    def make_dropdowns(self, parent):
        boxes = {}
        unit_system = start_unit
        for x in parameter_list:
            boxes[x[0]] = MyComboBox(parent, unit_system, x[1])
            boxes[x[0]].currentTextChanged.connect(self.get_unit)
        return boxes

    def make_tab1_layout(self):
        layout = QGridLayout(self.tab1)
        layout.labels = self.make_labels(self.tab1)
        layout.inputs = self.make_inputs(self.tab1)
        layout.boxes = self.make_dropdowns(self.tab1)
        i = 0
        j = 1
        for x in parameter_list:
            layout.addWidget(layout.labels[x[0]], (i % 6) + 1, j)
            layout.addWidget(layout.inputs[x[0]], (i % 6) + 1, j + 1)
            layout.addWidget(layout.boxes[x[0]], (i % 6) + 1, j + 2)
            i = i + 1
            if i >= 6:
                j = 4
        return layout

    def make_tab2_tree(self, parent):
        tree_widget = QTreeWidget(parent)
        tree_widget.setHeaderLabel("Options")
        tree_widget.itemClicked.connect(self.update_units)
        tree_widget.units = QTreeWidgetItem(tree_widget, ["Unit Systems"])
        for x in units_systems:
            child = QTreeWidgetItem(tree_widget.units, [x])
            child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
            child.setCheckState(0, Qt.Unchecked)
            tree_widget.units.addChild(child)
        tree_widget.addTopLevelItem(tree_widget.units)
        return tree_widget

    def get_value(self, text):
        for x in parameter_list:
            try:
                cur = float(self.tab1.layout.inputs[x[0]].text())
            except ValueError:
                cur = 0.0
            self.parent.value[x] = cur

    def get_unit(self, text):
        for x in parameter_list:
            self.parent.unit[x[0]] = self.tab1.layout.boxes[x[0]].currentText()

    def update_parameters(self):
        old_state = {}
        for x in self.tab1.layout.boxes:
            old_state[x] = self.tab1.layout.boxes[x].blockSignals(True)
        for x in parameter_list:
            self.tab1.layout.inputs[x[0]].setText(self.parent.value[x[0]])
            self.tab1.layout.boxes[x[0]].setCurrentText(self.parent.unit[x[0]])
        for x in self.tab1.layout.boxes:
            self.tab1.layout.boxes[x[0]].blockSignals(old_state[x[0]])

    def update_units(self, item, col):
        for x in parameter_list:
            while self.tab1.layout.boxes[x[0]].count() > 1:
                self.tab1.layout.boxes[x[0]].removeItem(1)
        unit_list = [si_units, imperial_units, field_units]
        for x in range(self.tab2.tree_view.units.childCount()):
            if (self.tab2.tree_view.units.child(x).checkState(0) & Qt.Checked):
                y = unit_list[x]
                for p in parameter_list:
                    for k in y[p[1]]:
                        self.tab1.layout.boxes[p[0]].addItem(k)


class MyComboBox(QComboBox):
    def __init__(self, parent, unit_system, dimension):
        super(MyComboBox, self).__init__(parent)
        self.addItem("-- Choose Unit")
        for x in unit_system[dimension]:
            self.addItem(x)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = Window()
    app.exec_()
    sys.exit()

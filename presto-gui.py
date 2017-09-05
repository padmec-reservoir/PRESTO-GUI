import sys
import pint
from PyQt5 import QtWidgets, QtGui
from configobj import ConfigObj

# Create list of parameters
parameter_list = ["Pressao inicial", "Pressao barometrica", "Poco produtor",
                  "Poco injetor 1", "Poco injetor 2", "Tempo de injecao",
                  "Densidade", "Viscosidade", "Altura", "Area", "Porosidade",
                  "Permeabilidade"]
dimension_list = ["Pressure", "Pressure", "Volume Flow", "Volume Flow",
                  "Volume Flow", "Time", "Density", "Viscosity", "Length",
                  "Area", "Dimensionless", "Dimensionless"]
unit_dict = {"Area": ["acre", "square_foot", "square_inch", "meter ** 2"],
             "Density": ["kilogram / meter ** 3", "pound / foot ** 3",
                         "pound / dry_gallon", "pound / inch ** 3"],
             "Length": ["foot", "meter", "inch", "yard"],
             "Mass Flow": ["kilogram / day", "pound / day"],
             "Pressure": ["Pa", "psi"],
             "Volume": ["dry_barrel", "foot ** 3", "dry_gallon", "inch ** 3",
                        "meter ** 3"],
             "Volume Flow": ["dry_barrel / day", "foot ** 3 / day",
                             "dry_gallon / day"],
             "Weigth": ["kilogram", "pound"],
             "Weigth per Length": ["kilogram / meter", "pound / foot",
                                   "pound / inch"],
             "Time": ["second", "minute", "hour", "day", "week", "month",
                      "year"],
             "Viscosity": ["centipoise", "stokes", "rhe"],
             "Dimensionless": [""]}


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.value = {}
        self.unit = {}
        self.setGeometry(50, 50, 500, 500)
        self.setWindowTitle("PRESTO - Python Reservoir Simulation Toolbox")
        self.setWindowIcon(QtGui.QIcon('presto-logo.png'))
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
                self.close_application))
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

    def close_application(self):
        print("Exiting!")
        sys.exit()

    def open_file(self):
        name = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
        file = ConfigObj(name[0])
        for x in parameter_list:
            self.value[x] = file["values"][x]
            self.unit[x] = file["units"][x]
        self.table_widget.update_parameters()

    def save_file(self):
        name = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File')
        file = ConfigObj(name[0])
        file["values"] = {}
        file["units"] = {}
        for x in parameter_list:
            file["values"][x] = self.value[x]
            file["units"][x] = self.unit[x]
        file.write()


class MyAction(QtWidgets.QAction):
    def __init__(self, parent, name, shortcut, status, function):
        super(MyAction, self).__init__(name, parent)
        self.setShortcut(shortcut)
        self.setStatusTip(status)
        self.triggered.connect(function)


class MyTableWidget(QtWidgets.QTabWidget):
    def __init__(self, parent):
        super(MyTableWidget, self).__init__(parent)
        self.parent = parent
        # Define layout
        self.layout = QtWidgets.QGridLayout(self)
        # Make first tab
        self.tab1 = QtWidgets.QWidget()
        # Define layout of tab 1
        self.tab1.layout = self.make_tab1_layout()
        # Add tabs to tab screen
        self.addTab(self.tab1, "Tab 1")

    def make_labels(self, parent):
        labels = {}
        for x in parameter_list:
            labels[x] = QtWidgets.QLabel(x, parent)
        return labels

    def make_inputs(self, parent):
        inputs = {}
        for x in parameter_list:
            inputs[x] = QtWidgets.QLineEdit(parent)
            inputs[x].textEdited.connect(self.get_value)
        return inputs

    def make_dropdowns(self, parent):
        boxes = {}
        i = 0
        for x in parameter_list:
            boxes[x] = MyComboBox(parent, self.parent.ureg, dimension_list[i])
            boxes[x].editTextChanged.connect(self.get_unit)
            i = i + 1
        return boxes

    def make_tab1_layout(self):
        layout = QtWidgets.QGridLayout(self.tab1)
        layout.labels = self.make_labels(self.tab1)
        layout.inputs = self.make_inputs(self.tab1)
        layout.boxes = self.make_dropdowns(self.tab1)
        i = 0
        j = 1
        for x in parameter_list:
            layout.addWidget(layout.labels[x], (i % 6) + 1, j)
            layout.addWidget(layout.inputs[x], (i % 6) + 1, j + 1)
            layout.addWidget(layout.boxes[x], (i % 6) + 1, j + 2)
            i = i + 1
            if i >= 6:
                j = 4
        return layout

    def get_value(self, text):
        for x in parameter_list:
            try:
                cur = float(self.tab1.layout.inputs[x].text())
            except ValueError:
                cur = 0.0
            self.parent.value[x] = cur
        self.dbg(1)

    def get_unit(self, text):
        for x in parameter_list:
            self.parent.unit[x] = self.tab1.layout.boxes[x].currentText()
        self.dbg(2)

    def update_parameters(self):
        for x in parameter_list:
            self.tab1.layout.inputs[x].setText(self.parent.value[x])
            self.tab1.layout.boxes[x].setCurrentText(self.parent.unit[x])

    def dbg(self, opt):
        if opt == 1:
            for x in parameter_list:
                print(self.parent.value[x])
        else:
            for x in parameter_list:
                print(self.parent.unit[x])
        print()


class MyComboBox(QtWidgets.QComboBox):
    def __init__(self, parent, ureg, dimension):
        super(MyComboBox, self).__init__(parent)
        self.addItem("-- Choose Unit")
        for x in unit_dict[dimension]:
            self.addItem(x)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    GUI = Window()
    app.exec_()
    sys.exit()

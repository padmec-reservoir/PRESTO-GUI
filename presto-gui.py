import sys
import pint
from PyQt5 import QtWidgets, QtGui
from configobj import ConfigObj

# Create list of parameters
parameter_list = ["param1", "param2", "result"]
dropdown_list = ["param1", "param2", "result", "dim"]
unit_dict = {"dims" : ["Area", "Density", "Length", "Mass Flow", "Pressure",
                       "Volume", "Volume Flow", "Weigth", "Weigth per Length"],
             "Area" : ["acre", "square_foot", "square_inch", "meter ** 2"],
             "Density" : ["kilogram / meter ** 3", "pound / foot ** 3",
                          "pound / dry_gallon", "pound / inch ** 3"],
             "Length" : ["foot", "meter", "inch", "yard"],
             "Mass Flow" : ["kilogram / day", "pound / day"],
             "Pressure" : ["Pa", "psi"],
             "Volume" : ["dry_barrel", "foot ** 3", "dry_gallon", "inch ** 3",
                         "meter ** 3"],
             "Volume Flow" : ["dry_barrel / day", "foot ** 3 / day",
                              "dry_gallon / day"],
             "Weigth" : ["kilogram", "pound"],
             "Weigth per Length" : ["kilogram / meter", "pound / foot",
                                    "pound / inch"],
             "idle" : None}


class Window(QtWidgets.QMainWindow):
    def __init__(self, parameters=None, dropdown=None):
        super(Window, self).__init__()
        if not parameters:
            parameters = {}
        self.param = parameters
        if not dropdown:
            dropdown = {}
        self.dpdown = dropdown
        self.setGeometry(50, 50, 300, 300)
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
            self.param[x] = float(file["parameters"][x])
        for x in dropdown_list:
            self.dpdown[x] = file["dropdowns"][x]
        self.table_widget.update_parameters()

    def save_file(self):
        name = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File')
        file = ConfigObj(name[0])
        file["parameters"] = {}
        for x in parameter_list:
            file["parameters"][x] = self.param[x]
        file["dropdowns"] = {}
        for x in dropdown_list:
            file["dropdowns"][x] = self.dpdown[x]
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
        self.layout = QtWidgets.QVBoxLayout(self)
        # Make first tab
        self.tab1 = QtWidgets.QWidget()
        # Define layout of tab 1
        self.tab1.layout = QtWidgets.QFormLayout(self.tab1)
        # First Row
        self.tab1.row1_label = QtWidgets.QLabel("Dimension", self.tab1)
        self.tab1.row1_dim = MyComboBox(self.tab1, parent.ureg, "dims")
        self.tab1.row1_dim.currentTextChanged.connect(self.get_dim)
        self.tab1.layout.addRow(self.tab1.row1_label, self.tab1.row1_dim)
        # Second Row
        self.tab1.row2 = QtWidgets.QWidget()
        self.tab1.row2.label = QtWidgets.QLabel("Parameters", self.tab1.row2)
        self.tab1.row2.layout = QtWidgets.QGridLayout(self.tab1.row2)
        # Creating and binding functions to text input and dropdown 1
        self.tab1.row2.prm1 = QtWidgets.QLineEdit(self.tab1.row2)
        self.tab1.row2.prm1.textEdited.connect(self.get_param1)
        self.tab1.row2.prm1_dpdown = MyComboBox(self.tab1.row2, parent.ureg, "idle")
        self.tab1.row2.prm1_dpdown.currentTextChanged.connect(self.get_dpdown1)
        # Creating and binding functions to text input and dropdown 2
        self.tab1.row2.prm2 = QtWidgets.QLineEdit(self.tab1.row2)
        self.tab1.row2.prm2.textEdited.connect(self.get_param2)
        self.tab1.row2.prm2_dpdown = MyComboBox(self.tab1.row2, parent.ureg, "idle")
        self.tab1.row2.prm2_dpdown.currentTextChanged.connect(self.get_dpdown2)
        # Setting up the layout of second row
        self.tab1.row2.layout.addWidget(self.tab1.row2.prm1, 1, 1)
        self.tab1.row2.layout.addWidget(self.tab1.row2.prm1_dpdown, 1, 2)
        self.tab1.row2.layout.addWidget(self.tab1.row2.prm2, 2, 1)
        self.tab1.row2.layout.addWidget(self.tab1.row2.prm2_dpdown, 2, 2)
        self.tab1.layout.addRow(self.tab1.row2.label, self.tab1.row2)
        # Third row
        self.tab1.row3Label = QtWidgets.QLabel("Result", self.tab1)
        self.tab1.row3Result = QtWidgets.QLineEdit(self.tab1)
        self.tab1.row3Result.setReadOnly(True)
        self.tab1.layout.addRow(self.tab1.row3Label, self.tab1.row3Result)
        # Add tabs to tab screen
        self.addTab(self.tab1, "Tab 1")

    def get_param1(self, text):
        try:
            value = float(text)
        except ValueError:
            value = 0.0
        self.parent.param["param1"] = value
        self.set_result()

    def get_param2(self, text):
        try:
            value = float(text)
        except ValueError:
            value = 0.0
        self.parent.param["param2"] = value
        self.set_result()

    def get_dpdown1(self, text):
        if text == "-- Choose Unit":
            text = ""
        self.parent.dpdown["param1"] = text
        self.set_result()

    def get_dpdown2(self, text):
        if text == "-- Choose Unit":
            text = ""
        self.parent.dpdown["param2"] = text
        self.set_result()

    def get_dim(self, text):
        self.parent.dpdown["dim"] = text
        while self.tab1.row2.prm1_dpdown.count() > 1:
            self.tab1.row2.prm1_dpdown.removeItem(1)
            self.tab1.row2.prm2_dpdown.removeItem(1)
        if text != "-- Choose Dimension":
            for x in unit_dict[text]:
                self.tab1.row2.prm1_dpdown.addItem(x)
                self.tab1.row2.prm2_dpdown.addItem(x)

    def set_result(self):
        param1_value = self.parent.param["param1"]
        param1_unit = self.parent.dpdown["param1"]
        param2_value = self.parent.param["param2"]
        param2_unit = self.parent.dpdown["param2"]
        param1 = param1_value * self.parent.ureg(param1_unit)
        param2 = param2_value * self.parent.ureg(param2_unit)
        res = param1 * param2
        self.parent.param["result"] = res.magnitude
        self.parent.dpdown["result"] = str(res.units)
        self.tab1.row3Result.setText(str(res.magnitude)+" "+str(res.units))

    def update_parameters(self):
        # Refactor this method
        self.tab1.row2.prm1.setText(str(self.parent.param["param1"]))
        self.tab1.row2.prm2.setText(str(self.parent.param["param2"]))
        self.tab1.row3Result.setText(str(self.parent.param["result"]) + " " +
                                     self.parent.dpdown["result"])
        self.tab1.row1_dim.setCurrentText(self.parent.dpdown["dim"])
        self.tab1.row2.prm1_dpdown.setCurrentText(self.parent.dpdown["param1"])
        self.tab1.row2.prm2_dpdown.setCurrentText(self.parent.dpdown["param2"])


class MyComboBox(QtWidgets.QComboBox):
    def __init__(self, parent, ureg, dimension):
        super(MyComboBox, self).__init__(parent)
        if dimension == "dims":
            self.addItem("-- Choose Dimension")
            for x in unit_dict[dimension]:
                self.addItem(x)
        else:
            self.addItem("-- Choose Unit")


if __name__ == '__main__':
    # Create list of parameters values based om parameter list
    parameters_values = {}
    dropdown_values = {}
    for x in parameter_list:
        parameters_values[x] = 0.0
    for x in dropdown_list:
        dropdown_values[x] = ""
    app = QtWidgets.QApplication(sys.argv)
    GUI = Window(parameters_values, dropdown_values)
    app.exec_()
    sys.exit()

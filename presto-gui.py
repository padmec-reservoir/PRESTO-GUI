import sys
import pint
from PyQt5 import QtWidgets, QtGui
from configobj import ConfigObj

# Create list of parameters
parameter_list = ["param1", "param2", "result"]


class Window(QtWidgets.QMainWindow):
    def __init__(self, parameters=None):
        super(Window, self).__init__()
        if not parameters:
            parameters = {}
        self.param = parameters
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
            self.param[x] = (float(file[x][0]), str(file[x][1]))
        self.table_widget.update_parameters()

    def save_file(self):
        name = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File')
        file = ConfigObj(name[0])
        for x in parameter_list:
            file[x] = self.param[x]
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
        # Define layout
        self.parent = parent
        self.layout = QtWidgets.QVBoxLayout(self)
        # Make first tab
        self.tab1 = QtWidgets.QWidget()
        # Define layout of tab 1
        self.tab1.layout = QtWidgets.QFormLayout(self.tab1)
        # First Row
        self.tab1.row1_label = QtWidgets.QLabel("Exit", self.tab1)
        self.tab1.row1_button = QtWidgets.QPushButton("Quit", self.tab1)
        self.tab1.row1_button.clicked.connect(parent.close_application)
        self.tab1.layout.addRow(self.tab1.row1_label, self.tab1.row1_button)
        # Second Row
        self.tab1.row2 = QtWidgets.QWidget()
        self.tab1.row2.label = QtWidgets.QLabel("Parameters", self.tab1.row2)
        self.tab1.row2.layout = QtWidgets.QGridLayout(self.tab1.row2)
        # Creating and binding functions to text input and dropdown 1
        self.tab1.row2.prm1 = QtWidgets.QLineEdit(self.tab1.row2)
        self.tab1.row2.prm1.textEdited.connect(self.get_param1)
        self.tab1.row2.prm1_dpdown = MyComboBox(self.tab1.row2, parent.ureg)
        self.tab1.row2.prm1_dpdown.currentTextChanged.connect(self.get_dpdown1)
        # Creating and binding functions to text input and dropdown 2
        self.tab1.row2.prm2 = QtWidgets.QLineEdit(self.tab1.row2)
        self.tab1.row2.prm2.textEdited.connect(self.get_param2)
        self.tab1.row2.prm2_dpdown = MyComboBox(self.tab1.row2, parent.ureg)
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
        self.parent.param["param1"] = (value, self.parent.param["param1"][1])
        self.set_result()

    def get_param2(self, text):
        try:
            value = float(text)
        except ValueError:
            value = 0.0
        self.parent.param["param2"] = (value, self.parent.param["param2"][1])
        self.set_result()

    def get_dpdown1(self, text):
        self.parent.param["param1"] = (self.parent.param["param1"][0], text)
        self.set_result()

    def get_dpdown2(self, text):
        self.parent.param["param2"] = (self.parent.param["param2"][0], text)
        self.set_result()

    def set_result(self):
        param1 = (self.parent.param["param1"][0] *
                  self.parent.ureg(self.parent.param["param1"][1]))
        param2 = (self.parent.param["param2"][0] *
                  self.parent.ureg(self.parent.param["param2"][1]))
        res = param1 * param2
        self.parent.param["result"] = (res.magnitude, str(res.units))
        self.tab1.row3Result.setText(str(res.magnitude)+" "+str(res.units))

    def update_parameters(self):
        self.tab1.row2.prm1.setText(str(self.parent.param["param1"][0]))
        self.tab1.row2.prm2.setText(str(self.parent.param["param2"][0]))
        self.tab1.row2.prm1_dpdown.setCurrentText(
            self.parent.param["param1"][1])
        self.tab1.row2.prm2_dpdown.setCurrentText(
            self.parent.param["param2"][1])
        self.tab1.row3Result.setText(str(self.parent.param["result"][0]) +
                                     " " +
                                     self.parent.param["result"][1])


class MyComboBox(QtWidgets.QComboBox):
    def __init__(self, parent, ureg):
        super(MyComboBox, self).__init__(parent)
        # Create list of units
        self.unitList = ([""] +
                         list(
                            set([a for a in ureg._units.keys() and
                                [x._name for x in ureg._units.values()]])))
        self.unitList.sort()
        for x in self.unitList:
            self.addItem(x)


if __name__ == '__main__':
    # Create list of parameters values based om parameter list
    parametersValues = {}
    for x in parameter_list:
        parametersValues[x] = (0.0, "")
    app = QtWidgets.QApplication(sys.argv)
    GUI = Window(parametersValues)
    app.exec_()
    sys.exit()

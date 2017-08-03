import sys
import pint
from PyQt5 import QtWidgets, QtGui, QtCore

#Create registry
ureg = pint.UnitRegistry()
#Create list of units
unitList = [""]+list(set([a for a in ureg._units.keys() and [x._name for x in ureg._units.values()]]))
unitList.sort()
#Create list of parameters
parameterList = ["param1", "param2", "result"]

class Window(QtWidgets.QMainWindow):
    def __init__(self, parameters = {}):
        super(Window, self).__init__()
        self.param = parameters
        self.setGeometry(50, 50, 300, 300)
        self.setWindowTitle("PRESTO - Python Reservoir Simulation Toolbox")
        self.setWindowIcon(QtGui.QIcon('presto-logo.png'))
        
        #Menubar
        ##Create submenu exit
        self.exitApp = QtWidgets.QAction("&Exit", self)
        self.exitApp.setShortcut("Ctrl+Q")
        self.exitApp.setStatusTip("Leave The App")
        self.exitApp.triggered.connect(self.closeApplication)
        ##Create submenu open file
        self.openFile = QtWidgets.QAction("&Open File", self)
        self.openFile.setShortcut("Ctrl+O")
        self.openFile.setStatusTip("Open existing parameter file")
        self.openFile.triggered.connect(self.fileOpen)
        ##Create menu File in menubar and add 
        self.mainMenu = self.menuBar()
        self.fileMenu = self.mainMenu.addMenu("&File")
        self.fileMenu.addAction(self.exitApp)
        self.fileMenu.addAction(self.openFile)
        
        #Statusbar
        self.statusBar()
        
        #Tabs
        ##Create tab screen
        self.tableWidget = QtWidgets.QTabWidget(self)
        self.tableWidget.layout = QtWidgets.QVBoxLayout(self.tableWidget)
        ##Create tabs inside tab screen
        self.tab1 = QtWidgets.QWidget()
        self.tab2 = QtWidgets.QWidget()
        ##Define whats inside tab1
        self.tab1.layout = QtWidgets.QFormLayout(self.tab1)
        ###First Row
        self.tab1.row1Label = QtWidgets.QLabel("Exit", self.tab1)
        self.tab1.row1Button = QtWidgets.QPushButton("Quit", self.tab1)
        self.tab1.row1Button.clicked.connect(Window.closeApplication)
        self.tab1.layout.addRow(self.tab1.row1Label, self.tab1.row1Button)
        ###Second Row
        self.tab1.row2Label = QtWidgets.QLabel("Parameters", self.tab1)
        self.tab1.row2Box = QtWidgets.QWidget()
        self.tab1.row2Box.layout = QtWidgets.QGridLayout(self.tab1.row2Box)
        ####Defining parameters inputboxes and dropdowns
        #####Creating and binding functions to text input and dropdown 1
        self.tab1.row2Box.param1In = QtWidgets.QLineEdit(self.tab1.row2Box)
        self.tab1.row2Box.param1In.textEdited.connect(self.getParam1)
        self.tab1.row2Box.param1Dropdown = MyComboBox(self.tab1.row2Box)
        self.tab1.row2Box.param1Dropdown.currentTextChanged.connect(self.getDropdown1)
        #####Creating and binding functions to text input and dropdown 2
        self.tab1.row2Box.param2In = QtWidgets.QLineEdit(self.tab1.row2Box)
        self.tab1.row2Box.param2In.textEdited.connect(self.getParam2)
        self.tab1.row2Box.param2Dropdown = MyComboBox(self.tab1.row2Box)
        self.tab1.row2Box.param2Dropdown.currentTextChanged.connect(self.getDropdown2)
        #####Setting up the layout of second row
        self.tab1.row2Box.layout.addWidget(self.tab1.row2Box.param1In, 1, 1)
        self.tab1.row2Box.layout.addWidget(self.tab1.row2Box.param1Dropdown, 1, 2)
        self.tab1.row2Box.layout.addWidget(self.tab1.row2Box.param2In, 2, 1)
        self.tab1.row2Box.layout.addWidget(self.tab1.row2Box.param2Dropdown, 2, 2)
        self.tab1.layout.addRow(self.tab1.row2Label, self.tab1.row2Box)
        ###Third row
        self.tab1.row3Label = QtWidgets.QLabel("Result", self.tab1)
        self.tab1.row3Result = QtWidgets.QLineEdit(self.tab1)
        self.tab1.row3Result.setReadOnly(True)
        self.tab1.layout.addRow(self.tab1.row3Label, self.tab1.row3Result)
        ##Add tabs to tab screen
        self.tableWidget.addTab(self.tab1, "Tab 1")
        self.setCentralWidget(self.tableWidget)
        
        #Show
        self.show()
        
    def closeApplication(self):
        print("Exiting!")
        sys.exit()
        
    def fileOpen(self):
        name = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
        if name[0] == '':
            return
        file = open(name[0], 'r')
        
    def getParam1(self, text):
        value = 0.0
        if text != "":
            value = float(text)
        self.param["param1"] = (value, self.param["param1"][1])
        self.setResult()
    
    def getParam2(self, text):
        value = 0.0
        if text != "":
            value = float(text)
        self.param["param2"] = (value, self.param["param2"][1])
        self.setResult()
        
    def getDropdown1(self, text):
        self.param["param1"] = (self.param["param1"][0], text)
        self.setResult()
        
    def getDropdown2(self, text):
        self.param["param2"] = (self.param["param2"][0], text)
        self.setResult()
    
    def setResult(self):
        res = (self.param["param1"][0] * ureg.parse_expression(self.param["param1"][1])) * (self.param["param2"][0] * ureg.parse_expression(self.param["param2"][1]))
        self.param["result"] = (res.magnitude, str(res.units))
        self.tab1.row3Result.setText(str(res.magnitude)+" "+str(res.units))
        print (res)

class MyComboBox(QtWidgets.QComboBox):
    def __init__(self, parent):
        super(MyComboBox, self).__init__(parent)
        for x in unitList:
            self.addItem(x)
        
if __name__ == '__main__':
    #Create list of parameters values based om parameter list
    parametersValues = {}
    for x in parameterList:
        parametersValues[x] = (0.0, unitList[0])
    app = QtWidgets.QApplication(sys.argv)
    GUI = Window(parametersValues)
    app.exec_()
    print(parametersValues)
    sys.exit()
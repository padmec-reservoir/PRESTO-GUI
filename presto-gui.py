import sys
from PyQt5 import QtWidgets, QtGui, QtCore

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("PRESTO - Python Reservoir Simulation Toolbox")
        self.setWindowIcon(QtGui.QIcon('presto-logo.png'))
        
        #Menubar
        extractAction = QtWidgets.QAction("&Exit", self)
        extractAction.setShortcut("Ctrl+Q")
        extractAction.setStatusTip("Leave The App")
        extractAction.triggered.connect(self.close_application)
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("&File")
        fileMenu.addAction(extractAction)
        
        #Statusbar
        self.statusBar()
        
        #Tabs
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)
        
        #Show
        self.show()
        
    def close_application(self):
        print("Exiting!")
        sys.exit()
        
class MyTableWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super(QtWidgets.QWidget, self).__init__(parent)
        #Define layout manager to MyTableWidget
        self.layout = QtWidgets.QVBoxLayout(self)
 
        # Initialize tab screen
        self.tabs = QtWidgets.QTabWidget()
        self.tab1 = QtWidgets.QWidget()
        self.tab2 = QtWidgets.QWidget()
        
        #Button to Tab 1
        ##Define layout manager to Tab 1
        self.tab1.layout = QtWidgets.QGridLayout(self.tab1)
        ##Create the button
        self.tab1.btn = QtWidgets.QPushButton("Quit", self)
        self.tab1.btn.clicked.connect(Window.close_application)
        ##Add the button to the layout manager
        self.tab1.layout.addWidget(self.tab1.btn)
        
        #Text input to Tab 2
        ##Define layout manager to Tab 1
        self.tab2.layout = QtWidgets.QGridLayout(self.tab2)
        ##Create and add 8 pairs of labels and text inputs to Tab 2
        for i in range(1,5):
            for j in range(1,3):
                self.tab2.label = QtWidgets.QLabel("Input "+str((2*(i-1))+j), self)
                self.tab2.textbox = QtWidgets.QLineEdit(self)
                self.tab2.layout.addWidget(self.tab2.label, i, 2*j - 1)
                self.tab2.layout.addWidget(self.tab2.textbox, i, 2*j)
        # Add tabs
        self.tabs.addTab(self.tab1,"Tab 1")
        self.tabs.addTab(self.tab2,"Tab 2")

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())
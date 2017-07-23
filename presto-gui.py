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
        btn = QtWidgets.QPushButton("Quit", self)
        btn.clicked.connect(Window.close_application)
        ##Add the button to the layout manager
        self.tab1.layout.addWidget(btn)

        # Add tabs
        self.tabs.addTab(self.tab1,"Tab 1")
        self.tabs.addTab(self.tab2,"Tab 2")

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())
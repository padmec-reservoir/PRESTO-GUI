import sys
from PyQt5.QtWidgets import QApplication
from parameters import parameter_list, fluids, mesh
from MyWindow import MyWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = MyWindow(parameter_list, fluids, mesh)
    GUI.show()
    app.exec_()
    sys.exit()

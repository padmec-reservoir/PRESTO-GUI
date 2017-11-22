import sys
from PyQt5.QtWidgets import QApplication
from MyWindow import MyWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = MyWindow()
    GUI.show()
    app.exec_()
    sys.exit()

import sys
from PyQt5.QtWidgets import QApplication
from MainWindow import MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = MainWindow()
    GUI.show()
    app.exec_()
    sys.exit()

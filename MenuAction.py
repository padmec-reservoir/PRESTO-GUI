from PyQt5.QtWidgets import QAction


class MenuAction(QAction):
    def __init__(self, parent, name, shortcut, status, function):
        super(MenuAction, self).__init__(name, parent)
        self.setShortcut(shortcut)
        self.setStatusTip(status)
        self.triggered.connect(function)

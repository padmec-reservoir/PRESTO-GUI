from PyQt5.QtWidgets import QComboBox


class MyComboBox(QComboBox):
    def __init__(self, parent, unit_system, dimension):
        super(MyComboBox, self).__init__(parent)
        self.addItem("-- Choose Unit")
        for x in unit_system[dimension]:
            self.addItem(x)

from PyQt5.QtWidgets import (QTreeWidgetItem, QWidget, QGridLayout, QLabel,
                             QLineEdit, QComboBox, QCheckBox, QButtonGroup)
from PyQt5.QtCore import Qt
from parameters import (units_systems, reservoir, mesh, fluids, initial)


class MyTreeItem(QTreeWidgetItem):
    def __init__(self, parent, name, leafs):
        super(MyTreeItem, self).__init__(parent, [name])
        self.itens = {}
        if isinstance(leafs, dict):
            for x in leafs:
                self.itens[x] = MyTreeItem(self, x, leafs[x])
                self.addChild(self.itens[x])
                self.make_screen(x)
        else:
            for x in leafs:
                self.itens[x] = MyTreeItem(self, x, [])
                self.addChild(self.itens[x])
                self.make_screen(x)

    def get_selected(self):
        for x in self.itens.values():
            if x.isSelected():
                return x
            elif x.get_selected():
                return x.get_selected()
        return 0

    def make_screen(self, name):
        cur = self.itens[name]
        cur.screen = QWidget()
        cur.screen.layout = QGridLayout(cur.screen)
        cur.screen.layout.setAlignment(Qt.AlignTop)
        if name == "Dimensionality":
            cur.units = set()
            cur.button_group = QButtonGroup(cur.screen)
            cur.button_group.buttonClicked.connect(self.update_unit)
            cur.button_group.setExclusive(False)
            cur.buttons = {}
            i = 1
            for x in units_systems:
                cur.buttons[x] = QCheckBox(x, cur.screen)
                cur.button_group.addButton(cur.buttons[x])
                cur.screen.layout.addWidget(cur.buttons[x], i, 1)
                i += 1
        if name == "Reservoir":
            cur.labels = {}
            cur.inputs = {}
            cur.boxes = {}
            i = 1
            for x in reservoir:
                cur.labels[x[0]] = QLabel(x[0], cur.screen)
                cur.inputs[x[0]] = QLineEdit(cur.screen)
                cur.boxes[x[0]] = QComboBox(cur.screen)
                cur.screen.layout.addWidget(cur.labels[x[0]], i, 1)
                cur.screen.layout.addWidget(cur.inputs[x[0]], i, 2)
                cur.screen.layout.addWidget(cur.boxes[x[0]], i, 3)
                i += 1
        if name == "Mesh":
            cur.labels = {}
            cur.inputs = {}
            cur.boxes = {}
            i = 1
            for x in mesh:
                cur.labels[x[0]] = QLabel(x[0], cur.screen)
                cur.inputs[x[0]] = QLineEdit(cur.screen)
                cur.boxes[x[0]] = QComboBox(cur.screen)
                cur.screen.layout.addWidget(cur.labels[x[0]], i, 1)
                cur.screen.layout.addWidget(cur.inputs[x[0]], i, 2)
                cur.screen.layout.addWidget(cur.boxes[x[0]], i, 3)
                i += 1
        if name == "Rock (K, Φ)":
            pass
        if name == "Fluid":
            cur.labels = {}
            cur.inputs = {}
            cur.boxes = {}
            cur.labels["Oil"] = QLabel("Oil", cur.screen)
            cur.screen.layout.addWidget(cur.labels["Oil"], 1, 1)
            i = 2
            for x in fluids:
                cur.labels[x[0]] = QLabel(x[0], cur.screen)
                cur.inputs[x[0]] = QLineEdit(cur.screen)
                cur.boxes[x[0]] = QComboBox(cur.screen)
                cur.screen.layout.addWidget(cur.labels[x[0]], i, 1)
                cur.screen.layout.addWidget(cur.inputs[x[0]], i, 2)
                cur.screen.layout.addWidget(cur.boxes[x[0]], i, 3)
                i += 1
            cur.labels["Water"] = QLabel("Water", cur.screen)
            cur.screen.layout.addWidget(cur.labels["Water"], i, 1)
            i += 1
            for x in fluids:
                cur.labels[x[0]] = QLabel(x[0], cur.screen)
                cur.inputs[x[0]] = QLineEdit(cur.screen)
                cur.boxes[x[0]] = QComboBox(cur.screen)
                cur.screen.layout.addWidget(cur.labels[x[0]], i, 1)
                cur.screen.layout.addWidget(cur.inputs[x[0]], i, 2)
                cur.screen.layout.addWidget(cur.boxes[x[0]], i, 3)
                i += 1
        if name == "Rock (Flux, ρ, k)":
            pass
        if name == "Analisys Interval":
            pass
        if name == "Initial Conditions":
            cur.labels = {}
            cur.inputs = {}
            cur.boxes = {}
            i = 1
            for x in initial:
                cur.labels[x[0]] = QLabel(x[0], cur.screen)
                cur.inputs[x[0]] = QLineEdit(cur.screen)
                cur.boxes[x[0]] = QComboBox(cur.screen)
                cur.screen.layout.addWidget(cur.labels[x[0]], i, 1)
                cur.screen.layout.addWidget(cur.inputs[x[0]], i, 2)
                cur.screen.layout.addWidget(cur.boxes[x[0]], i, 3)
                i += 1
        if name == "Injection/Producer":
            pass
        if name == "Aquifer":
            pass
        if name == "Numerical Methods":
            pass
        if name == "Interval":
            pass
        if name == "Variables":
            pass
        cur.screen.hide()

    def update_unit(self, button):
        cur = self.itens["Dimensionality"]
        for x in cur.buttons.values():
            if x.isChecked():
                cur.units.add(x.text())
            else:
                cur.units.discard(x.text())

    def get_data(self, name):
        cur = self.itens[name]
        values = {}
        units = {}
        for x in cur.inputs:
            values[x] = cur.inputs[x].text()
            units[x] = cur.boxes[x].currentText()
        return values, units

    def set_data(self, values, units, name):
        cur = self.itens[name]
        old_boxes = {}
        for x in cur.boxes:
            old_boxes[x] = cur.boxes[x].blockSignals(True)
        for x in values:
            cur.inputs[x].setText(values[x])
            cur.boxes[x].setCurrentText(units[x])
        for x in cur.boxes:
            cur.boxes[x].blockSignals(old_boxes[x])

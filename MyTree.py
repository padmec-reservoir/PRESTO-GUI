from PyQt5.QtWidgets import (QTreeWidget, QWidget, QGridLayout, QPushButton,
                             QLabel, QLineEdit, QComboBox, QCheckBox,
                             QButtonGroup)
from PyQt5.QtCore import Qt
from MyTreeItem import MyTreeItem
from parameters import (entries, problem, model, geometry, well, properties,
                        initial_conditions, boundary, method, output)


class MyTree(QTreeWidget):
    def __init__(self, parent, name):
        super(MyTree, self).__init__(parent)
        self.parent = parent
        self.setHeaderLabel(name)
        self.itemClicked.connect(self.update_screen)
        self.roots = {}
        for x in entries:
            self.roots[x] = MyTreeItem(self, x, entries[x])
            self.addTopLevelItem(self.roots[x])
            self.make_screen(x)

    def update_screen(self, cur):
        main = self.parent.main_widget.layout
        try:
            black = main.itemAtPosition(1, 2).widget()
            main.removeWidget(black)
            black.hide()
        except AttributeError:
            pass
        main.addWidget(cur.screen, 1, 2)
        cur.screen.show()

    def get_selected(self):
        for x in self.roots.values():
            if x.isSelected():
                return x
            elif x.get_selected():
                return x.get_selected()
        return 0

    def update_units(self, units):
        for x in self.roots:
            self.roots[x].update_units(units)

    def make_screen(self, name):
        cur = self.roots[name]
        cur.screen = QWidget()
        cur.screen.layout = QGridLayout(cur.screen)
        cur.screen.layout.setAlignment(Qt.AlignTop)
        if name == "Problem":
            cur.name = problem
            cur.labels = {}
            cur.inputs = {}
            cur.boxes = {}
            i = 1
            for x in cur.name:
                cur.labels[x[0]] = QLabel(x[0], cur.screen)
                cur.inputs[x[0]] = QLineEdit(cur.screen)
                cur.boxes[x[0]] = QComboBox(cur.screen)
                cur.screen.layout.addWidget(cur.labels[x[0]], i, 1)
                cur.screen.layout.addWidget(cur.inputs[x[0]], i, 2)
                cur.screen.layout.addWidget(cur.boxes[x[0]], i, 3)
                i += 1
        if name == "Physical/Mathematical Model":
            cur.name = model
            cur.model = ""
            cur.button_group = QButtonGroup(cur.screen)
            cur.button_group.buttonClicked.connect(self.update_model)
            cur.button_group.setExclusive(True)
            cur.buttons = {}
            i = 1
            for x in cur.name:
                cur.buttons[x] = QCheckBox(x, cur.screen)
                cur.button_group.addButton(cur.buttons[x])
                cur.screen.layout.addWidget(cur.buttons[x], i, 1)
                i += 1
        if name == "Geometry":
            cur.name = geometry
            cur.labels = {}
            cur.inputs = {}
            cur.boxes = {}
            i = 1
            for x in cur.name:
                cur.labels[x[0]] = QLabel(x[0], cur.screen)
                cur.inputs[x[0]] = QLineEdit(cur.screen)
                cur.boxes[x[0]] = QComboBox(cur.screen)
                cur.screen.layout.addWidget(cur.labels[x[0]], i, 1)
                cur.screen.layout.addWidget(cur.inputs[x[0]], i, 2)
                cur.screen.layout.addWidget(cur.boxes[x[0]], i, 3)
                i += 1
        if name == "Wells (Geometry)":
            cur.buttom = QPushButton("New Well", cur.screen)
            cur.buttom.clicked.connect(self.make_well)
            cur.screen.layout.addWidget(cur.buttom, 1, 1)
        if name == "Physical Properties":
            cur.name = properties
            cur.labels = {}
            cur.inputs = {}
            cur.boxes = {}
            i = 1
            for x in cur.name:
                cur.labels[x[0]] = QLabel(x[0], cur.screen)
                cur.inputs[x[0]] = QLineEdit(cur.screen)
                cur.boxes[x[0]] = QComboBox(cur.screen)
                cur.screen.layout.addWidget(cur.labels[x[0]], i, 1)
                cur.screen.layout.addWidget(cur.inputs[x[0]], i, 2)
                cur.screen.layout.addWidget(cur.boxes[x[0]], i, 3)
                i += 1
        if name == "Initial Conditions":
            cur.name = initial_conditions
            cur.labels = {}
            cur.inputs = {}
            cur.boxes = {}
            i = 1
            for x in cur.name:
                cur.labels[x[0]] = QLabel(x[0], cur.screen)
                cur.inputs[x[0]] = QLineEdit(cur.screen)
                cur.boxes[x[0]] = QComboBox(cur.screen)
                cur.screen.layout.addWidget(cur.labels[x[0]], i, 1)
                cur.screen.layout.addWidget(cur.inputs[x[0]], i, 2)
                cur.screen.layout.addWidget(cur.boxes[x[0]], i, 3)
                i += 1
        if name == "Boundary Conditions":
            cur.name = boundary
            cur.labels = {}
            cur.inputs = {}
            cur.boxes = {}
            i = 1
            for x in cur.name:
                cur.labels[x[0]] = QLabel(x[0], cur.screen)
                cur.inputs[x[0]] = QLineEdit(cur.screen)
                cur.boxes[x[0]] = QComboBox(cur.screen)
                cur.screen.layout.addWidget(cur.labels[x[0]], i, 1)
                cur.screen.layout.addWidget(cur.inputs[x[0]], i, 2)
                cur.screen.layout.addWidget(cur.boxes[x[0]], i, 3)
                i += 1
        if name == "Numerical Methods":
            cur.name = method
            cur.methods = set()
            cur.button_group = QButtonGroup(cur.screen)
            cur.button_group.buttonClicked.connect(cur.update_method)
            cur.button_group.setExclusive(False)
            cur.buttons = {}
            i = 1
            for x in cur.name:
                cur.buttons[x] = QCheckBox(x, cur.screen)
                cur.button_group.addButton(cur.buttons[x])
                cur.screen.layout.addWidget(cur.buttons[x], i, 1)
                i += 1
        if name == "Output Configuration":
            cur.name = output
            cur.labels = {}
            cur.inputs = {}
            cur.boxes = {}
            i = 1
            for x in cur.name:
                cur.labels[x[0]] = QLabel(x[0], cur.screen)
                cur.inputs[x[0]] = QLineEdit(cur.screen)
                cur.boxes[x[0]] = QComboBox(cur.screen)
                cur.screen.layout.addWidget(cur.labels[x[0]], i, 1)
                cur.screen.layout.addWidget(cur.inputs[x[0]], i, 2)
                cur.screen.layout.addWidget(cur.boxes[x[0]], i, 3)
                i += 1
        cur.screen.hide()

    def make_well(self, clkd, name=""):
        cur = self.roots["Wells (Geometry)"]
        if not name:
            name = "Well "+str(len(cur.itens) + 1)
        cur.itens[name] = MyTreeItem(cur, name, [])
        cur.addChild(cur.itens[name])
        cur = cur.itens[name]
        cur.screen = QWidget()
        cur.screen.layout = QGridLayout(cur.screen)
        cur.screen.layout.setAlignment(Qt.AlignTop)
        cur.button_group = QButtonGroup(cur.screen)
        cur.button_group.buttonClicked.connect(self.update_well_type)
        cur.button_group.setExclusive(True)
        cur.buttons = {}
        i = 1
        for x in ["Injection", "Producer"]:
            cur.buttons[x] = QCheckBox(x, cur.screen)
            cur.button_group.addButton(cur.buttons[x])
            cur.screen.layout.addWidget(cur.buttons[x], 1, i)
            i += 1
        cur.type = ""
        cur.name = well
        cur.labels = {}
        cur.inputs = {}
        cur.boxes = {}
        cur.labels["Rename"] = QLabel("Name", cur.screen)
        cur.inputs["Rename"] = QLineEdit(cur.screen)
        cur.inputs["Rename"].setText(name)
        cur.inputs["Rename"].textEdited.connect(self.update_well_name)
        cur.screen.layout.addWidget(cur.labels["Rename"], 2, 1)
        cur.screen.layout.addWidget(cur.inputs["Rename"], 2, 2)
        i = 3
        for x in cur.name:
            cur.labels[x[0]] = QLabel(x[0], cur.screen)
            cur.inputs[x[0]] = QLineEdit(cur.screen)
            cur.boxes[x[0]] = QComboBox(cur.screen)
            cur.screen.layout.addWidget(cur.labels[x[0]], i, 1)
            cur.screen.layout.addWidget(cur.inputs[x[0]], i, 2)
            cur.screen.layout.addWidget(cur.boxes[x[0]], i, 3)
            i += 1
        cur.delbut = QPushButton("Delete Well", cur.screen)
        cur.delbut.clicked.connect(self.delete_well)
        cur.screen.layout.addWidget(cur.delbut, i, 1)
        self.roots["Problem"].itens["Unit System"].update_unit_list(None)

    def update_well_type(self, clkd):
        cur = self.roots["Wells (Geometry)"].itens
        well = None
        for x in cur.values():
            if clkd in x.buttons.values():
                well = x
                break
        well.type = clkd.text()

    def delete_well(self):
        cur = self.roots["Wells (Geometry)"]
        item = self.get_selected()
        main = self.parent.main_widget.layout
        index = cur.indexOfChild(item)
        child = cur.takeChild(index)
        main.removeWidget(child.screen)
        child.screen.hide()
        del cur.itens[item.text(0)]

    def update_well_name(self, text):
        cur = self.get_selected()
        name = ""
        for x in self.roots["Wells (Geometry)"].itens:
            if self.roots["Wells (Geometry)"].itens[x] == cur:
                name = x
        del(self.roots["Wells (Geometry)"].itens[name])
        cur.setText(0, text)
        self.roots["Wells (Geometry)"].itens[text] = cur

    def update_model(self, button):
        cur = self.roots["Physical/Mathematical Model"]
        for x in cur.buttons.values():
            if x.isChecked():
                cur.model = x.text()

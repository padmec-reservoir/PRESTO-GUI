from PyQt5.QtWidgets import (QTreeWidgetItem, QWidget, QGridLayout, QLabel,
                             QLineEdit, QComboBox, QCheckBox, QButtonGroup)
from PyQt5.QtCore import Qt
from parameters import (units_systems, reservoir, mesh, rock_1, fluids, rock_2,
                        injection_producer, aquifer, interval, variables,
                        si_units, imperial_units, field_units, start_unit,
                        dimensionality)


class MyTreeItem(QTreeWidgetItem):
    def __init__(self, parent, name, leafs):
        super(MyTreeItem, self).__init__(parent, [name])
        self.parent = parent
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
            cur.name = dimensionality
            cur.dimensions = ""
            cur.button_group = QButtonGroup(cur.screen)
            cur.button_group.buttonClicked.connect(self.update_dimensionality)
            cur.button_group.setExclusive(True)
            cur.buttons = {}
            i = 1
            for x in cur.name:
                cur.buttons[x] = QCheckBox(x, cur.screen)
                cur.button_group.addButton(cur.buttons[x])
                cur.screen.layout.addWidget(cur.buttons[x], i, 1)
                i += 1
        if name == "Unit System":
            cur.units = set()
            cur.name = units_systems
            cur.button_group = QButtonGroup(cur.screen)
            cur.button_group.buttonClicked.connect(self.update_unit_list)
            cur.button_group.setExclusive(False)
            cur.buttons = {}
            i = 1
            for x in cur.name:
                cur.buttons[x] = QCheckBox(x, cur.screen)
                cur.button_group.addButton(cur.buttons[x])
                cur.screen.layout.addWidget(cur.buttons[x], i, 1)
                i += 1
        if name == "Reservoir":
            cur.name = reservoir
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
        if name == "Mesh":
            cur.name = mesh
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
        if name == "Rock (K, O)":
            cur.name = rock_1
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
        if name == "Fluid":
            cur.name = fluids
            cur.labels = {}
            cur.inputs = {}
            cur.boxes = {}
            i = 1
            for x in cur.name:
                if(i == 1):
                    cur.labels["Oil"] = QLabel("Oil", cur.screen)
                    cur.screen.layout.addWidget(cur.labels["Oil"], 1, 1)
                    i += 1
                if(i == 4):
                    cur.labels["Water"] = QLabel("Water", cur.screen)
                    cur.screen.layout.addWidget(cur.labels["Water"], i, 1)
                    i += 1
                if(i == 7):
                    cur.labels["Gas"] = QLabel("Gas", cur.screen)
                    cur.screen.layout.addWidget(cur.labels["Gas"], i, 1)
                    i += 1
                cur.labels[x[0]] = QLabel(x[0], cur.screen)
                cur.inputs[x[0]] = QLineEdit(cur.screen)
                cur.boxes[x[0]] = QComboBox(cur.screen)
                cur.screen.layout.addWidget(cur.labels[x[0]], i, 1)
                cur.screen.layout.addWidget(cur.inputs[x[0]], i, 2)
                cur.screen.layout.addWidget(cur.boxes[x[0]], i, 3)
                i += 1
        if name == "Rock (Flux, p, k)":
            cur.name = rock_2
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
        if name == "Injection/Producer":
            cur.name = injection_producer
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
        if name == "Aquifer":
            cur.name = aquifer
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
        if name == "Interval":
            cur.name = interval
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
        if name == "Variables":
            cur.variables = set()
            cur.name = variables
            cur.button_group = QButtonGroup(cur.screen)
            cur.button_group.buttonClicked.connect(self.update_variables)
            cur.button_group.setExclusive(False)
            cur.buttons = {}
            i = 1
            for x in cur.name:
                cur.buttons[x] = QCheckBox(x, cur.screen)
                cur.button_group.addButton(cur.buttons[x])
                cur.screen.layout.addWidget(cur.buttons[x], i, 1)
                i += 1
        cur.screen.hide()

    def update_unit_list(self, button):
        if (self.text(0) == "Problem"):
            cur = self.itens["Unit System"]
            up = self.parent
        else:
            cur = self
            up = self.parent.parent
        for x in cur.buttons.values():
            if x.isChecked():
                cur.units.add(x.text())
            else:
                cur.units.discard(x.text())
        valid_units = start_unit
        for system in cur.units:
            if system == "SI":
                cur_list = si_units
            elif system == "Imperial Units":
                cur_list = imperial_units
            elif system == "Field Units":
                cur_list = field_units
            for dim in cur_list:
                for unit in cur_list[dim]:
                    valid_units[dim].add(unit)
        up.update_units(valid_units)

    def update_units(self, units):
        try:
            for x in self.name:
                while self.boxes[x[0]].count() > 0:
                    self.boxes[x[0]].removeItem(0)
                for unit in units[x[1]]:
                    self.boxes[x[0]].addItem(unit)
        except AttributeError:
            pass
        for x in self.itens:
            self.itens[x].update_units(units)

    def get_data(self):
        values = {}
        units = ""
        name = self.text(0)
        if name == "Dimensionality":
            values = self.dimensions
        elif name == "Unit System":
            values = [x for x in self.units]
        elif name == "Physical/Mathematical Model":
            values = self.model
        elif name == "Numerical Methods":
            values = [x for x in self.methods]
        elif name == "Variables":
            values = [x for x in self.variables]
        else:
            units = {}
            try:
                for x in self.inputs:
                    try:
                        values[x] = float(self.inputs[x].text())
                    except ValueError:
                        if x is not "Rename":
                            values[x] = 0.0
                        else:
                            values[x] = self.inputs[x].text()
                    try:
                        units[x] = self.boxes[x].currentText()
                    except KeyError:
                        units[x] = ""
            except AttributeError:
                pass
        return values, units

    def set_data(self, values, units):
        name = self.text(0)
        if name == "Dimensionality":
            self.dimensions = values
            self.buttons[values].setChecked(True)
            self.update_dimensionality(None)
        elif name == "Unit System":
            for system in values:
                self.buttons[system].setChecked(True)
            self.update_unit_list(None)
        elif name == "Physical/Mathematical Model":
            self.model = values
            self.buttons[values].setChecked(True)
        elif name == "Numerical Methods":
            for method in values:
                self.buttons[method].setChecked(True)
            self.update_method(None)
        elif name == "Variables":
            for variable in values:
                self.buttons[variable].setChecked(True)
            self.update_variables(None)
        else:
            old_boxes = {}
            try:
                for x in self.boxes:
                    old_boxes[x] = self.boxes[x].blockSignals(True)
                for x in values:
                    self.inputs[x].setText(values[x])
                    try:
                        self.boxes[x].setCurrentText(units[x])
                    except KeyError:
                        pass
                for x in self.boxes:
                    self.boxes[x].blockSignals(old_boxes[x])
            except AttributeError:
                pass

    def update_dimensionality(self, button):
        if (self.text(0) == "Problem"):
            cur = self.itens["Dimensionality"]
            up = self.parent
        else:
            cur = self
            up = self.parent.parent
        for x in cur.buttons.values():
            if x.isChecked():
                cur.dimensions = x.text()
        for x in up.roots["Geometry"].inputs.values():
            x.setEnabled(False)
        for x in up.roots["Geometry"].itens["Mesh"].inputs.values():
            x.setEnabled(False)
        for x in up.roots["Wells (Geometry)"].itens.values():
            for y in x.inputs.values():
                if (y.text() != "Rename"):
                    y.setEnabled(False)

        if cur.dimensions == "1D":
            geometry_open = ["Length X"]
            mesh_open = ["Steps in X"]
            well_open = ["X"]
        if cur.dimensions == "2D":
            geometry_open = ["Length X", "Length Y"]
            mesh_open = ["Steps in X", "Steps in Y"]
            well_open = ["X", "Y"]
        if cur.dimensions == "3D":
            geometry_open = ["Length X", "Length Y", "Length Z"]
            mesh_open = ["Steps in X", "Steps in Y", "Steps in Z"]
            well_open = ["X", "Y", "Z"]

        for x in up.roots["Geometry"].inputs:
            if (x in geometry_open):
                up.roots["Geometry"].inputs[x].setEnabled(True)
        for x in up.roots["Geometry"].itens["Mesh"].inputs:
            if (x in mesh_open):
                up.roots["Geometry"].itens["Mesh"].inputs[x].setEnabled(True)
        for x in up.roots["Wells (Geometry)"].itens.values():
            for y in x.inputs:
                if (y != "Rename"):
                    x.inputs[y].setEnabled(True)

    def update_variables(self, button):
        if (self.text(0) == "Output Configuration"):
            cur = self.itens["Variables"]
        else:
            cur = self
        for x in cur.buttons.values():
            if x.isChecked():
                cur.variables.add(x.text())
            else:
                cur.variables.discard(x.text())

    def update_method(self, button):
        for x in self.buttons.values():
            if x.isChecked():
                self.methods.add(x.text())
            else:
                self.methods.discard(x.text())

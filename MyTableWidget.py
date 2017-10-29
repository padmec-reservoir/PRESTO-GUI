from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QTabWidget, QGridLayout, QWidget, QLabel,
                             QLineEdit, QTreeWidget, QTreeWidgetItem,
                             QSizePolicy, QPushButton, QHBoxLayout)
from PyQt5.QtGui import QIcon
from parameters import (si_units, imperial_units, field_units, units_systems,
                        start_unit)
from MyComboBox import MyComboBox


class MyTableWidget(QTabWidget):
    def __init__(self, parent, parameter_list, fluids):
        super(MyTableWidget, self).__init__(parent)
        self.parameter_list = parameter_list
        self.fluids = fluids
        self.unit_list = [si_units, imperial_units, field_units]
        self.checked_units = set()
        self.parent = parent
        self.layout = QGridLayout(self)
        self.tab1 = self.make_tab1(self)
        self.tab2 = self.make_tab2(self)
        # self.tab3 = self.make_tab3(self)
        self.tab4 = self.make_tab4(self)
        # self.tab5 = self.make_tab5(self)
        self.addTab(self.tab1, "Condições Iniciais")
        self.addTab(self.tab2, "Fluidos")
        # self.addTab(self.tab3, "Campo de Permeabilidade")
        self.addTab(self.tab4, "Poços")
        # self.addTab(self.tab5, "Malha")

    def make_tab1(self, parent):
        tab1 = QWidget(parent)
        tab1.value = dict((x[0], 0) for x in self.parameter_list)
        tab1.unit = dict((x[0], "") for x in self.parameter_list)
        tab1.layout = QGridLayout(tab1)
        tab1.layout.setAlignment(Qt.AlignTop)
        tab1.tree = self.make_tree(tab1)
        tab1.layout.addWidget(tab1.tree, 1, 1, 6, 1)
        tab1.labels = self.make_labels(tab1, self.parameter_list)
        tab1.inputs = self.make_inputs(tab1, self.parameter_list)
        tab1.boxes = self.make_dropdowns(tab1, self.parameter_list)
        i = 0
        j = 2
        for x in self.parameter_list:
            tab1.layout.addWidget(tab1.labels[x[0]], (i % 6) + 1, j)
            tab1.layout.addWidget(tab1.inputs[x[0]], (i % 6) + 1, j + 1)
            tab1.layout.addWidget(tab1.boxes[x[0]], (i % 6) + 1, j + 2)
            i = i + 1
        return tab1

    def make_tab2(self, parent):
        tab2 = QWidget(parent)
        tab2.layout = QGridLayout(tab2)
        tab2.layout.setAlignment(Qt.AlignTop)
        tab2.oil = QLabel("Óleo", tab2)
        tab2.oil.value = dict((x[0], 0) for x in self.fluids)
        tab2.oil.unit = dict((x[0], "") for x in self.fluids)
        tab2.oil.labels = self.make_labels(tab2, self.fluids)
        tab2.oil.inputs = self.make_inputs(tab2, self.fluids)
        tab2.oil.boxes = self.make_dropdowns(tab2, self.fluids)
        tab2.water = QLabel("Água", tab2)
        tab2.water.value = dict((x[0], 0) for x in self.fluids)
        tab2.water.unit = dict((x[0], "") for x in self.fluids)
        tab2.water.labels = self.make_labels(tab2, self.fluids)
        tab2.water.inputs = self.make_inputs(tab2, self.fluids)
        tab2.water.boxes = self.make_dropdowns(tab2, self.fluids)
        tab2.layout.addWidget(tab2.oil, 1, 1)
        tab2.layout.addWidget(tab2.water, 1, 4)
        i = 2
        for x in self.fluids:
            tab2.layout.addWidget(tab2.oil.labels[x[0]], i, 1)
            tab2.layout.addWidget(tab2.oil.inputs[x[0]], i, 2)
            tab2.layout.addWidget(tab2.oil.boxes[x[0]], i, 3)
            tab2.layout.addWidget(tab2.water.labels[x[0]], i, 4)
            tab2.layout.addWidget(tab2.water.inputs[x[0]], i, 5)
            tab2.layout.addWidget(tab2.water.boxes[x[0]], i, 6)
            i = i + 1
        return tab2

    def make_tab3(self, parent):
        tab3 = QWidget(parent)
        return tab3

    def make_tab4(self, parent):
        tab4 = QWidget(parent)
        tab4.inpos = {}
        tab4.outpos = {}
        tab4.layout = QGridLayout(tab4)
        tab4.layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        tab4.inwells = {}
        tab4.inwells_c = 0
        tab4.outwells = {}
        tab4.outwells_c = 0
        tab4.add_inwell_but = QPushButton("Novo Poço Injetor", tab4)
        tab4.add_inwell_but.clicked.connect(self.make_inwell)
        tab4.del_inwell_but = QPushButton("Deletar Poço Injetor", tab4)
        tab4.del_inwell_but.clicked.connect(self.delete_inwell)
        tab4.add_outwell_but = QPushButton("Novo Poço Extrator", tab4)
        tab4.add_outwell_but.clicked.connect(self.make_outwell)
        tab4.del_outwell_but = QPushButton("Remover Poço Extrator", tab4)
        tab4.del_outwell_but.clicked.connect(self.delete_outwell)
        tab4.layout.addWidget(tab4.add_inwell_but, 1, 1)
        tab4.layout.addWidget(tab4.del_inwell_but, 1, 2)
        tab4.layout.addWidget(tab4.add_outwell_but, 1, 3)
        tab4.layout.addWidget(tab4.del_outwell_but, 1, 4)
        return tab4

    def make_tab5(self, parent):
        tab5 = QWidget(parent)
        return tab5

    def make_inwell(self, posx = 0, posy = 0):
        well = QWidget(self.tab4)
        well.layout = QHBoxLayout(well)
        self.tab4.inwells_c = self.tab4.inwells_c + 1
        well.name = "Poco injetor "+str(self.tab4.inwells_c)
        well.label = QLabel(well.name, well)
        well.xlabel = QLabel("X: ", well)
        well.xin = QLineEdit(well)
        well.xin.textEdited.connect(self.get_well_pos)
        well.ylabel = QLabel("Y: ", well)
        well.yin = QLineEdit(well)
        well.yin.textEdited.connect(self.get_well_pos)
        well.layout.addWidget(well.label)
        well.layout.addWidget(well.xlabel)
        well.layout.addWidget(well.xin)
        well.layout.addWidget(well.ylabel)
        well.layout.addWidget(well.yin)
        self.tab4.inwells[well.name] = well
        self.tab4.inpos[well.name] = (posx, posy)
        i = self.tab4.inwells_c + 1
        self.tab4.layout.addWidget(well, i, 1, i, 2, Qt.AlignLeft)

    def make_outwell(self, posx = 0, posy = 0):
        well = QWidget(self.tab4)
        well.layout = QHBoxLayout(well)
        self.tab4.outwells_c = self.tab4.outwells_c + 1
        well.name = "Poco extrator "+str(self.tab4.outwells_c)
        well.label = QLabel(well.name, well)
        well.xlabel = QLabel("X: ", well)
        well.xin = QLineEdit(well)
        well.xin.textEdited.connect(self.get_well_pos)
        well.ylabel = QLabel("Y: ", well)
        well.yin = QLineEdit(well)
        well.yin.textEdited.connect(self.get_well_pos)
        well.layout.addWidget(well.label)
        well.layout.addWidget(well.xlabel)
        well.layout.addWidget(well.xin)
        well.layout.addWidget(well.ylabel)
        well.layout.addWidget(well.yin)
        self.tab4.outwells[well.name] = well
        self.tab4.outpos[well.name] = (posx, posy)
        i = self.tab4.outwells_c + 1
        self.tab4.layout.addWidget(well, i, 3, i, 4, Qt.AlignRight)

    def delete_inwell(self, a = None):
        if self.tab4.inwells_c == 0:
            return
        deleted = "Poco injetor "+str(self.tab4.inwells_c)
        self.tab4.inwells_c = self.tab4.inwells_c - 1
        del self.tab4.inpos[deleted]
        well = self.tab4.inwells.pop(deleted)
        self.tab4.layout.removeWidget(well)
        well.setParent(None)

    def delete_outwell(self, a = None):
        if self.tab4.outwells_c == 0:
            return
        deleted = "Poco extrator "+str(self.tab4.outwells_c)
        self.tab4.outwells_c = self.tab4.outwells_c - 1
        del self.tab4.outpos[deleted]
        well = self.tab4.outwells.pop(deleted)
        self.tab4.layout.removeWidget(well)
        well.setParent(None)

    def get_well_pos(self, text):
        for x in self.tab4.inwells.values():
            try:
                a = float(x.xin.text())
            except ValueError:
                a = 0.0
            try:
                b = float(x.yin.text())
            except ValueError:
                b = 0.0
            self.tab4.inpos[x.name] = (a, b)
        for x in self.tab4.outwells.values():
            try:
                a = float(x.xin.text())
            except ValueError:
                a = 0.0
            try:
                b = float(x.yin.text())
            except ValueError:
                b = 0.0
            self.tab4.outpos[x.name] = (a, b)

    def make_labels(self, parent, label_list):
        labels = {}
        for x in label_list:
            labels[x[0]] = QLabel(x[0], parent)
        return labels

    def make_inputs(self, parent, input_list):
        inputs = {}
        for x in input_list:
            inputs[x[0]] = QLineEdit(parent)
            inputs[x[0]].textEdited.connect(self.get_value)
        return inputs

    def make_dropdowns(self, parent, dropdown_list):
        boxes = {}
        for x in dropdown_list:
            boxes[x[0]] = MyComboBox(parent, start_unit, x[1])
            boxes[x[0]].currentTextChanged.connect(self.get_unit)
        return boxes

    def make_tree(self, parent):
        tree_widget = QTreeWidget(parent)
        tree_widget.setHeaderLabel("Options")
        tree_widget.itemClicked.connect(self.update_units)
        tree_widget.units = QTreeWidgetItem(tree_widget, ["Unit Systems"])
        for x in units_systems:
            child = QTreeWidgetItem(tree_widget.units, [x])
            child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
            child.setCheckState(0, Qt.Unchecked)
            tree_widget.units.addChild(child)
        tree_widget.addTopLevelItem(tree_widget.units)
        return tree_widget

    def get_value(self, text):
        for x in self.parameter_list:
            try:
                cur = float(self.tab1.inputs[x[0]].text())
            except ValueError:
                cur = 0.0
            self.tab1.value[x[0]] = cur
        for x in self.fluids:
            try:
                oil_cur = float(self.tab2.oil.inputs[x[0]].text())
                water_cur = float(self.tab2.water.inputs[x[0]].text())
            except ValueError:
                oil_cur = 0.0
                water_cur = 0.0
            self.tab2.oil.value[x[0]] = oil_cur
            self.tab2.water.value[x[0]] = water_cur

    def get_unit(self, text):
        for x in self.parameter_list:
            self.tab1.unit[x[0]] = self.tab1.boxes[x[0]].currentText()
        for x in self.fluids:
            self.tab2.oil.unit[x[0]] = self.tab2.oil.boxes[x[0]].currentText()
            self.tab2.water.unit[x[0]] = self.tab2.water.boxes[x[0]].currentText()

    def update_wells(self, info):
        while self.tab4.inwells_c > 0:
            self.delete_inwell()
        while self.tab4.outwells_c > 0:
            self.delete_outwell()
        for x in info["inpos"]:
            self.make_inwell(info["inpos"][x][0], info["inpos"][x][1])
            self.tab4.inwells[x].xin.setText(str(info["inpos"][x][0]))
            self.tab4.inwells[x].yin.setText(str(info["inpos"][x][1]))
        for x in info["outpos"]:
            self.make_outwell(info["outpos"][x][0], info["outpos"][x][1])
            self.tab4.outwells[x].xin.setText(str(info["outpos"][x][0]))
            self.tab4.outwells[x].yin.setText(str(info["outpos"][x][1]))

    def update_parameters(self):
        old_tab1 = {}
        old_tab2_oil = {}
        old_tab2_water = {}
        for x in self.tab1.boxes:
            old_tab1[x] = self.tab1.boxes[x].blockSignals(True)
        for x in self.tab2.oil.boxes:
            old_tab2_oil[x] = self.tab2.oil.boxes[x].blockSignals(True)
        for x in self.tab2.water.boxes:
            old_tab2_water[x] = self.tab2.water.boxes[x].blockSignals(True)
        for x in self.checked_units:
            self.tab1.tree.units.child(int(x)).setCheckState(0, Qt.Checked)
        self.update_units(None, None)
        for x in self.parameter_list:
            self.tab1.inputs[x[0]].setText(self.tab1.value[x[0]])
            self.tab1.boxes[x[0]].setCurrentText(self.tab1.unit[x[0]])
        for x in self.fluids:
            self.tab2.oil.inputs[x[0]].setText(self.tab2.oil.value[x[0]])
            self.tab2.oil.boxes[x[0]].setCurrentText(self.tab2.oil.unit[x[0]])
            self.tab2.water.inputs[x[0]].setText(self.tab2.water.value[x[0]])
            self.tab2.water.boxes[x[0]].setCurrentText(self.tab2.water.unit[x[0]])
        for x in self.tab1.boxes:
            self.tab1.boxes[x].blockSignals(old_tab1[x])
        for x in self.tab2.oil.boxes:
            self.tab2.oil.boxes[x].blockSignals(old_tab2_oil[x])
        for x in self.tab2.water.boxes:
            self.tab2.water.boxes[x].blockSignals(old_tab2_water[x])

    def update_units(self, item, col):
        count = self.tab1.tree.units.childCount()
        for x in range(count):
            if (self.tab1.tree.units.child(x).checkState(0) & Qt.Checked):
                self.checked_units.add(x)
            else:
                self.checked_units.discard(x)
        final_units = {}
        for p in self.parameter_list:
            final_units[p[1]] = set()
            for x in self.checked_units:
                for k in self.unit_list[x][p[1]]:
                    final_units[p[1]].add(k)
        for p in self.parameter_list:
            cur_units = [self.tab1.boxes[p[0]].itemText(i)
                         for i in range(self.tab1.boxes[p[0]].count())]
            for k in cur_units:
                if k not in final_units[p[1]]:
                    i = self.tab1.boxes[p[0]].findText(k)
                    self.tab1.boxes[p[0]].removeItem(i)
            for k in final_units[p[1]]:
                if self.tab1.boxes[p[0]].findText(k) == -1:
                    self.tab1.boxes[p[0]].addItem(k)
            if self.tab1.boxes[p[0]].count() == 0:
                self.tab1.boxes[p[0]].addItem("-- Choose Unit")
        for p in self.fluids:
            final_units[p[1]] = set()
            for x in self.checked_units:
                for k in self.unit_list[x][p[1]]:
                    final_units[p[1]].add(k)
        for p in self.fluids:
            cur_units = [self.tab2.oil.boxes[p[0]].itemText(i)
                         for i in range(self.tab2.oil.boxes[p[0]].count())]
            for k in cur_units:
                if k not in final_units[p[1]]:
                    i = self.tab2.oil.boxes[p[0]].findText(k)
                    self.tab2.oil.boxes[p[0]].removeItem(i)
                    i = self.tab2.water.boxes[p[0]].findText(k)
                    self.tab2.water.boxes[p[0]].removeItem(i)
            for k in final_units[p[1]]:
                if self.tab2.oil.boxes[p[0]].findText(k) == -1:
                    self.tab2.oil.boxes[p[0]].addItem(k)
                if self.tab2.water.boxes[p[0]].findText(k) == -1:
                    self.tab2.water.boxes[p[0]].addItem(k)
            if self.tab2.oil.boxes[p[0]].count() == 0:
                self.tab2.oil.boxes[p[0]].addItem("-- Choose Unit")
            if self.tab2.water.boxes[p[0]].count() == 0:
                self.tab2.water.boxes[p[0]].addItem("-- Choose Unit")

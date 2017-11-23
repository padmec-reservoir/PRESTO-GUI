import pint
from sys import exit
from configobj import ConfigObj
from PyQt5.QtWidgets import (QTabWidget, QGridLayout, QWidget, QLabel,
                             QLineEdit, QTreeWidget, QTreeWidgetItem,
                             QSizePolicy, QPushButton, QFormLayout,
                             QFileDialog, QMainWindow)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from MyAction import MyAction
from MyComboBox import MyComboBox
from parameters import (si_units, imperial_units, field_units, units_systems,
                        start_unit, parameter_list, fluids, mesh, fields)


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(50, 50, 700, 500)
        self.setWindowTitle("PRESTO - Python Reservoir Simulation Toolbox")
        self.setWindowIcon(QIcon('presto-logo2.png'))
        self.ureg = pint.UnitRegistry()
        self.unit_list = [si_units, imperial_units, field_units]
        self.checked_units = set()
        self.last_click = ""

        # Menubar
        self.main_menu = self.menuBar()
        self.file_menu = self.main_menu.addMenu("&File")
        self.file_menu.addAction(
            MyAction(
                self,
                "&Exit",
                "Ctrl+Q",
                "Leave the app",
                exit))
        self.file_menu.addAction(
            MyAction(
                self,
                "&Open File",
                "Ctrl+O",
                "Open existing paramter file",
                self.open_file))
        self.file_menu.addAction(
            MyAction(
                self,
                "&Save File",
                "Ctrl+S",
                "Save current parameters",
                self.save_file))

        # Statusbar
        self.statusBar()

        # Tabs
        self.main_widget = QWidget(self)
        self.main_widget.layout = QGridLayout(self.main_widget)
        self.tree = self.make_tree(self)
        self.tab1 = self.make_tab1(self)
        self.tab2 = self.make_tab2(self)
        self.tab3 = self.make_tab3(self)
        self.tab4 = self.make_tab4(self)
        self.tab5 = self.make_tab5(self)
        self.tab2.hide()
        self.tab3.hide()
        self.tab4.hide()
        self.tab5.hide()
        self.main_widget.layout.addWidget(self.tree, 1, 1)
        self.main_widget.layout.addWidget(self.tab1, 1, 2)
        self.setCentralWidget(self.main_widget)

    def open_file(self):
        name = QFileDialog.getOpenFileName(self, 'Open File')
        if not name[0]:
            return
        config_file = ConfigObj(name[0])
        self.checked_units.clear()
        for x in config_file["systems"]:
            self.checked_units.add(int(x))
        for x in parameter_list:
            self.tab1.value[x[0]] = config_file["tab1"]["values"][x[0]]
            self.tab1.unit[x[0]] = config_file["tab1"]["units"][x[0]]
        for x in fluids:
            self.tab2.oil.value[x[0]] = config_file["tab2"]["oil"]["values"][x[0]]
            self.tab2.oil.unit[x[0]] = config_file["tab2"]["oil"]["units"][x[0]]
            self.tab2.water.value[x[0]] = config_file["tab2"]["water"]["values"][x[0]]
            self.tab2.water.unit[x[0]] = config_file["tab2"]["water"]["units"][x[0]]
        for x in mesh:
            self.tab5.value[x[0]] = config_file["tab5"]["values"][x[0]]
            self.tab5.unit[x[0]] = config_file["tab5"]["units"][x[0]]
        self.update_parameters()
        self.update_wells(config_file["tab4"])

    def save_file(self):
        # Need data validation on values and units
        name = QFileDialog.getSaveFileName(self, 'Save File')
        if not name[0]:
            return
        config_file = ConfigObj(name[0])
        config_file["systems"] = []
        config_file["tab1"] = {}
        config_file["tab1"]["values"] = {}
        config_file["tab1"]["units"] = {}
        config_file["tab2"] = {}
        config_file["tab2"]["oil"] = {}
        config_file["tab2"]["oil"]["values"] = {}
        config_file["tab2"]["oil"]["units"] = {}
        config_file["tab2"]["water"] = {}
        config_file["tab2"]["water"]["values"] = {}
        config_file["tab2"]["water"]["units"] = {}
        config_file["tab4"] = {}
        config_file["tab4"]["inpos"] = {}
        config_file["tab4"]["outpos"] = {}
        config_file["tab5"] = {}
        config_file["tab5"]["values"] = {}
        config_file["tab5"]["units"] = {}
        for x in self.checked_units:
            config_file["systems"].append(x)
        for x in parameter_list:
            config_file["tab1"]["values"][x[0]] = self.tab1.value[x[0]]
            config_file["tab1"]["units"][x[0]] = self.tab1.unit[x[0]]
        for x in fluids:
            config_file["tab2"]["oil"]["values"][x[0]] = self.tab2.oil.value[x[0]]
            config_file["tab2"]["oil"]["units"][x[0]] = self.tab2.oil.unit[x[0]]
            config_file["tab2"]["water"]["values"][x[0]] = self.tab2.water.value[x[0]]
            config_file["tab2"]["water"]["units"][x[0]] = self.tab2.water.unit[x[0]]
        for x in self.tab4.inpos:
            config_file["tab4"]["inpos"][x] = self.tab4.inpos[x]
        for x in self.tab4.outpos:
            config_file["tab4"]["outpos"][x] = self.tab4.outpos[x]
        for x in mesh:
            config_file["tab5"]["values"][x[0]] = self.tab5.value[x[0]]
            config_file["tab5"]["units"][x[0]] = self.tab5.unit[x[0]]
        config_file.write()

    def make_tab1(self, parent):
        tab1 = QWidget(parent)
        tab1.value = dict((x[0], 0) for x in parameter_list)
        tab1.unit = dict((x[0], "") for x in parameter_list)
        tab1.layout = QGridLayout(tab1)
        tab1.layout.setAlignment(Qt.AlignTop)
        tab1.layout.addWidget(self.tree, 1, 1, 6, 1)
        tab1.labels = self.make_labels(tab1, parameter_list)
        tab1.inputs = self.make_inputs(tab1, parameter_list)
        tab1.boxes = self.make_dropdowns(tab1, parameter_list)
        i = 0
        j = 2
        for x in parameter_list:
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
        tab2.oil.value = dict((x[0], 0) for x in fluids)
        tab2.oil.unit = dict((x[0], "") for x in fluids)
        tab2.oil.labels = self.make_labels(tab2, fluids)
        tab2.oil.inputs = self.make_inputs(tab2, fluids)
        tab2.oil.boxes = self.make_dropdowns(tab2, fluids)
        tab2.water = QLabel("Água", tab2)
        tab2.water.value = dict((x[0], 0) for x in fluids)
        tab2.water.unit = dict((x[0], "") for x in fluids)
        tab2.water.labels = self.make_labels(tab2, fluids)
        tab2.water.inputs = self.make_inputs(tab2, fluids)
        tab2.water.boxes = self.make_dropdowns(tab2, fluids)
        tab2.layout.addWidget(tab2.oil, 1, 1)
        tab2.layout.addWidget(tab2.water, 1, 4)
        i = 2
        for x in fluids:
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
        tab4.inwells = {}
        tab4.in_c = 1
        tab4.outpos = {}
        tab4.outwells = {}
        tab4.out_c = 1
        tab4.layout = QGridLayout(tab4)
        tab4.layout.setVerticalSpacing(20)
        tab4.layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        tab4.add_inwell_but = QPushButton("Novo Poço Injetor", tab4)
        tab4.add_inwell_but.clicked.connect(self.make_inwell)
        tab4.add_outwell_but = QPushButton("Novo Poço Ejetor", tab4)
        tab4.add_outwell_but.clicked.connect(self.make_outwell)
        tab4.layout.addWidget(tab4.add_inwell_but, 1, 1)
        tab4.layout.addWidget(tab4.add_outwell_but, 2, 1)
        return tab4

    def make_tab5(self, parent):
        tab5 = QWidget(parent)
        tab5.value = dict((x[0], 0) for x in mesh)
        tab5.unit = dict((x[0], "") for x in mesh)
        tab5.layout = QGridLayout(tab5)
        tab5.layout.setAlignment(Qt.AlignTop)
        tab5.labels = self.make_labels(tab5, mesh)
        tab5.inputs = self.make_inputs(tab5, mesh)
        tab5.boxes = self.make_dropdowns(tab5, mesh)
        i = 0
        for x in mesh:
            tab5.layout.addWidget(tab5.labels[x[0]], i, 1)
            tab5.layout.addWidget(tab5.inputs[x[0]], i, 2)
            tab5.layout.addWidget(tab5.boxes[x[0]], i, 3)
            i = i + 1
        return tab5

    def make_inwell(self, posx = 0, posy = 0, time = 0, unit = ""):
        well = QWidget(self.tab4)
        well.layout = QFormLayout(well)
        well.name = "Poco injetor "+str(self.tab4.in_c)
        self.tab4.in_c += 1
        well.label = QLabel(well.name, well)
        well.delete = QPushButton("Remover poço", well)
        well.delete.clicked.connect(self.delete_well)
        well.xlabel = QLabel("X: ", well)
        well.xin = QLineEdit(well)
        well.xin.textEdited.connect(self.get_well_pos)
        well.ylabel = QLabel("Y: ", well)
        well.yin = QLineEdit(well)
        well.yin.textEdited.connect(self.get_well_pos)
        well.timelabel = QLabel("Time: ", well)
        well.timein = QLineEdit(well)
        well.timein.textEdited.connect(self.get_well_pos)
        well.timebox = MyComboBox(well, start_unit, "Time")
        well.wrap = QWidget()
        well.wrap.layout = QGridLayout(well.wrap)
        well.wrap.layout.addWidget(well.timein, 1, 1)
        well.wrap.layout.addWidget(well.timebox, 1, 2)
        well.layout.addRow(well.label, well.delete)
        well.layout.addRow(well.xlabel, well.xin)
        well.layout.addRow(well.ylabel, well.yin)
        well.layout.addRow(well.timelabel, well.wrap)

        for x in range(self.tree.fields.childCount()):
            if self.tree.fields.child(x).text(0) == "Poços":
                well.entry = QTreeWidgetItem(self.tree.fields.child(x), [well.name])

        self.tab4.inwells[well.name] = well
        self.tab4.inpos[well.name] = (posx, posy, time, unit)
        self.update_units(0, -1)

    def make_outwell(self, posx = 0, posy = 0, time = 0, unit = ""):
        well = QWidget(self.tab4)
        well.layout = QFormLayout(well)
        well.name = "Poco ejetor "+str(self.tab4.out_c)
        self.tab4.out_c += 1
        well.label = QLabel(well.name, well)
        well.delete = QPushButton("Remover poço", well)
        well.delete.clicked.connect(self.delete_well)
        well.xlabel = QLabel("X: ", well)
        well.xin = QLineEdit(well)
        well.xin.textEdited.connect(self.get_well_pos)
        well.ylabel = QLabel("Y: ", well)
        well.yin = QLineEdit(well)
        well.yin.textEdited.connect(self.get_well_pos)
        well.timelabel = QLabel("Time: ", well)
        well.timein = QLineEdit(well)
        well.timein.textEdited.connect(self.get_well_pos)
        well.timebox = MyComboBox(well, start_unit, "Time")
        well.wrap = QWidget()
        well.wrap.layout = QGridLayout(well.wrap)
        well.wrap.layout.addWidget(well.timein, 1, 1)
        well.wrap.layout.addWidget(well.timebox, 1, 2)
        well.layout.addRow(well.label, well.delete)
        well.layout.addRow(well.xlabel, well.xin)
        well.layout.addRow(well.ylabel, well.yin)
        well.layout.addRow(well.timelabel, well.wrap)

        for x in range(self.tree.fields.childCount()):
            if self.tree.fields.child(x).text(0) == "Poços":
                well.entry = QTreeWidgetItem(self.tree.fields.child(x), [well.name])

        self.tab4.outwells[well.name] = well
        self.tab4.outpos[well.name] = (posx, posy, time, unit)
        self.update_units(0, -1)

    def delete_well(self, a = None):
        if len(self.tab4.inwells) + len(self.tab4.outwells) == 0:
            return
        deleted = self.last_click
        if deleted in self.tab4.inpos.keys():
            del self.tab4.inpos[deleted]
            well = self.tab4.inwells.pop(deleted)
            well.setParent(None)
        elif deleted in self.tab4.outpos.keys():
            del self.tab4.outpos[deleted]
            well = self.tab4.outwells.pop(deleted)
            well.setParent(None)
        for x in range(self.tree.fields.childCount()):
            if self.tree.fields.child(x).text(0) == "Poços":
                for y in range(self.tree.fields.child(x).childCount()):
                    try:
                        print(self.tree.fields.child(x).child(y).text(0))
                    except AttributeError:
                        print("wtf")
                    if self.tree.fields.child(x).child(y).text(0) == deleted:
                        line = self.tree.fields.child(x).takeChild(y)
                        return

    def get_well_pos(self, text):
        for x in self.tab4.inwells.values():
            try:
                posx = float(x.xin.text())
            except ValueError:
                posx = 0.0
            try:
                posy = float(x.yin.text())
            except ValueError:
                posy = 0.0
            try:
                time = float(x.timein.text())
            except:
                time = 0.0
            unit = x.timebox.currentText()
            self.tab4.inpos[x.name] = (posx, posy, time, unit)
        for x in self.tab4.outwells.values():
            try:
                posx = float(x.xin.text())
            except ValueError:
                posx = 0.0
            try:
                posy = float(x.yin.text())
            except ValueError:
                posy = 0.0
            try:
                time = float(x.timein.text())
            except:
                time = 0.0
            unit = x.timebox.currentText()
            self.tab4.outpos[x.name] = (posx, posy, time, unit)

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
        tree_widget.setHeaderLabel("Menu")
        tree_widget.itemClicked.connect(self.update_units)
        tree_widget.units = QTreeWidgetItem(tree_widget, ["Unit Systems"])
        for x in units_systems:
            child = QTreeWidgetItem(tree_widget.units, [x])
            child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
            child.setCheckState(0, Qt.Unchecked)
            tree_widget.units.addChild(child)
        tree_widget.addTopLevelItem(tree_widget.units)
        tree_widget.fields = QTreeWidgetItem(tree_widget, ["Fields"])
        for x in fields:
            child = QTreeWidgetItem(tree_widget.fields, [x])
            tree_widget.fields.addChild(child)
        tree_widget.addTopLevelItem(tree_widget.fields)
        return tree_widget

    def get_value(self, text):
        for x in parameter_list:
            try:
                tab1_cur = float(self.tab1.inputs[x[0]].text())
            except ValueError:
                tab1_cur = 0.0
            self.tab1.value[x[0]] = tab1_cur
        for x in fluids:
            try:
                oil_cur = float(self.tab2.oil.inputs[x[0]].text())
                water_cur = float(self.tab2.water.inputs[x[0]].text())
            except ValueError:
                oil_cur = 0.0
                water_cur = 0.0
            self.tab2.oil.value[x[0]] = oil_cur
            self.tab2.water.value[x[0]] = water_cur
        for x in mesh:
            try:
                tab5_cur = float(self.tab5.inputs[x[0]].text())
            except ValueError:
                tab5_cur = 0.0
            self.tab5.value[x[0]] = tab5_cur

    def get_unit(self, text):
        for x in parameter_list:
            self.tab1.unit[x[0]] = self.tab1.boxes[x[0]].currentText()
        for x in fluids:
            i = x[0]
            self.tab2.oil.unit[i] = self.tab2.oil.boxes[i].currentText()
            self.tab2.water.unit[i] = self.tab2.water.boxes[i].currentText()
        for x in mesh:
            self.tab5.unit[x[0]] = self.tab5.boxes[x[0]].currentText()

    def update_wells(self, info):
        while len(self.tab4.inwells) > 0:
            self.delete_inwell()
        while len(self.tab4.outwells) > 0:
            self.delete_outwell()
        self.tab4.in_c = 1
        self.tab4.out_c = 1
        for x in info["inpos"]:
            posx = info["inpos"][x][0]
            posy = info["inpos"][x][1]
            time = info["inpos"][x][2]
            unit = info["inpos"][x][3]
            self.make_inwell(posx, posy, time, unit)
            self.tab4.inwells[x].xin.setText(str(posx))
            self.tab4.inwells[x].yin.setText(str(posy))
            self.tab4.inwells[x].timein.setText(str(time))
        for x in info["outpos"]:
            posx = info["outpos"][x][0]
            posy = info["outpos"][x][1]
            time = info["outpos"][x][2]
            unit = info["outpos"][x][3]
            self.make_outwell(posx, posy, time, unit)
            self.tab4.outwells[x].xin.setText(str(posx))
            self.tab4.outwells[x].yin.setText(str(posy))
            self.tab4.outwells[x].timein.setText(str(time))
        self.update_parameters()

    def update_parameters(self):
        old_tab1 = {}
        old_tab2_oil = {}
        old_tab2_water = {}
        old_tab4_in = {}
        old_tab4_out = {}
        old_tab5 = {}
        for x in self.tab1.boxes:
            old_tab1[x] = self.tab1.boxes[x].blockSignals(True)
        for x in self.tab2.oil.boxes:
            old_tab2_oil[x] = self.tab2.oil.boxes[x].blockSignals(True)
        for x in self.tab2.water.boxes:
            old_tab2_water[x] = self.tab2.water.boxes[x].blockSignals(True)
        for x in self.tab4.inwells:
            old_tab4_in[x] = self.tab4.inwells[x].timebox.blockSignals(True)
        for x in self.tab4.outwells:
            old_tab4_out[x] = self.tab4.outwells[x].timebox.blockSignals(True)
        for x in self.tab5.boxes:
            old_tab5[x] = self.tab5.boxes[x].blockSignals(True)
        for x in self.checked_units:
            self.tree.units.child(int(x)).setCheckState(0, Qt.Checked)

        self.update_units(None, None)
        for x in parameter_list:
            self.tab1.inputs[x[0]].setText(self.tab1.value[x[0]])
            self.tab1.boxes[x[0]].setCurrentText(self.tab1.unit[x[0]])
        for x in fluids:
            self.tab2.oil.inputs[x[0]].setText(self.tab2.oil.value[x[0]])
            self.tab2.oil.boxes[x[0]].setCurrentText(self.tab2.oil.unit[x[0]])
            self.tab2.water.inputs[x[0]].setText(self.tab2.water.value[x[0]])
            self.tab2.water.boxes[x[0]].setCurrentText(self.tab2.water.unit[x[0]])
        for x in self.tab4.inwells.values():
            x.timebox.setCurrentText(self.tab4.inpos[x.name][3])
        for x in self.tab4.outwells.values():
            x.timebox.setCurrentText(self.tab4.outpos[x.name][3])
        for x in mesh:
            self.tab5.inputs[x[0]].setText(self.tab5.value[x[0]])
            self.tab5.boxes[x[0]].setCurrentText(self.tab5.unit[x[0]])

        for x in self.tab1.boxes:
            self.tab1.boxes[x].blockSignals(old_tab1[x])
        for x in self.tab2.oil.boxes:
            self.tab2.oil.boxes[x].blockSignals(old_tab2_oil[x])
        for x in self.tab2.water.boxes:
            self.tab2.water.boxes[x].blockSignals(old_tab2_water[x])
        for x in self.tab4.inwells:
            self.tab4.inwells[x].timebox.blockSignals(old_tab4_in[x])
        for x in self.tab4.outwells:
            self.tab4.outwells[x].timebox.blockSignals(old_tab4_out[x])
        for x in self.tab5.boxes:
            self.tab5.boxes[x].blockSignals(old_tab5[x])

    def update_units(self, item, col):
        try:
            tab = item.text(col)
        except AttributeError:
            tab = ""
        self.last_click = tab
        if (tab in units_systems or col == -1):
            count = self.tree.units.childCount()
            for x in range(count):
                if (self.tree.units.child(x).checkState(0) & Qt.Checked):
                    self.checked_units.add(x)
                else:
                    self.checked_units.discard(x)
            final_units = {}
            for p in parameter_list:
                final_units[p[1]] = set()
                for x in self.checked_units:
                    for k in self.unit_list[x][p[1]]:
                        final_units[p[1]].add(k)
            for p in parameter_list:
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
            for p in fluids:
                final_units[p[1]] = set()
                for x in self.checked_units:
                    for k in self.unit_list[x][p[1]]:
                        final_units[p[1]].add(k)
            for p in fluids:
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
            final_units["Time"] = set()
            for x in self.checked_units:
                for k in self.unit_list[x]["Time"]:
                    final_units["Time"].add(k)
            for x in self.tab4.inwells.values():
                cur_units = [x.timebox.itemText(i)
                             for i in range(x.timebox.count())]
                for k in cur_units:
                    if k not in final_units["Time"]:
                        i = x.timebox.findText(k)
                        x.timebox.removeItem(i)
                for k in final_units["Time"]:
                    if x.timebox.findText(k) == -1:
                        x.timebox.addItem(k)
                if x.timebox.count() == 0:
                    x.timebox.addItem("-- Choose Unit")
            for x in self.tab4.outwells.values():
                cur_units = [x.timebox.itemText(i)
                             for i in range(x.timebox.count())]
                for k in cur_units:
                    if k not in final_units["Time"]:
                        i = x.timebox.findText(k)
                        x.timebox.removeItem(i)
                for k in final_units["Time"]:
                    if x.timebox.findText(k) == -1:
                        x.timebox.addItem(k)
                if x.timebox.count() == 0:
                    x.timebox.addItem("-- Choose Unit")
            for p in mesh:
                final_units[p[1]] = set()
                for x in self.checked_units:
                    for k in self.unit_list[x][p[1]]:
                        final_units[p[1]].add(k)
            for p in mesh:
                cur_units = [self.tab5.boxes[p[0]].itemText(i)
                             for i in range(self.tab5.boxes[p[0]].count())]
                for k in cur_units:
                    if k not in final_units[p[1]]:
                        i = self.tab5.boxes[p[0]].findText(k)
                        self.tab5.boxes[p[0]].removeItem(i)
                for k in final_units[p[1]]:
                    if self.tab5.boxes[p[0]].findText(k) == -1:
                        self.tab5.boxes[p[0]].addItem(k)
                if self.tab5.boxes[p[0]].count() == 0:
                    self.tab5.boxes[p[0]].addItem("-- Choose Unit")
        if (tab != ""):
            self.tab1.hide()
            self.tab2.hide()
            self.tab3.hide()
            self.tab4.hide()
            self.tab5.hide()
            for x in self.tab4.inwells:
                self.tab4.inwells[x].hide()
            for x in self.tab4.outwells:
                self.tab4.outwells[x].hide()
        if (tab in fields):
            if item.text(col) == fields[0]:
                self.tab1.show()
                self.main_widget.layout.addWidget(self.tab1, 1, 2)
            if item.text(col) == fields[1]:
                self.tab2.show()
                self.main_widget.layout.addWidget(self.tab2, 1, 2)
            if item.text(col) == fields[2]:
                self.tab3.show()
                self.main_widget.layout.addWidget(self.tab3, 1, 2)
            if item.text(col) == fields[3]:
                self.tab4.show()
                self.main_widget.layout.addWidget(self.tab4, 1, 2)
            if item.text(col) == fields[4]:
                self.tab5.show()
                self.main_widget.layout.addWidget(self.tab5, 1, 2)
        elif (tab in self.tab4.inwells):
            well = self.tab4.inwells[tab]
            well.show()
            self.main_widget.layout.addWidget(well, 1, 2)
        elif (tab in self.tab4.outwells):
            well = self.tab4.outwells[tab]
            well.show()
            self.main_widget.layout.addWidget(well, 1, 2)

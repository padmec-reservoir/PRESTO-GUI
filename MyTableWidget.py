from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QTabWidget, QGridLayout, QWidget, QLabel,
                             QLineEdit, QTreeWidget, QTreeWidgetItem)
from parameters import (si_units, imperial_units, field_units, units_systems,
                        start_unit)
from MyComboBox import MyComboBox


class MyTableWidget(QTabWidget):
    def __init__(self, parent, parameter_list):
        super(MyTableWidget, self).__init__(parent)
        self.parameter_list = parameter_list
        self.unit_list = [si_units, imperial_units, field_units]
        self.parent = parent
        self.layout = QGridLayout(self)
        self.tab1 = QWidget(self)
        self.tab1.layout = self.make_tab1_layout(self.tab1)
        self.tab2 = QWidget(self)
        self.tab2.tree_view = self.make_tab2_tree(self.tab2)
        self.addTab(self.tab1, "Tab 1")
        self.addTab(self.tab2, "Tab 2")

    def make_labels(self, parent):
        labels = {}
        for x in self.parameter_list:
            labels[x[0]] = QLabel(x[0], parent)
        return labels

    def make_inputs(self, parent):
        inputs = {}
        for x in self.parameter_list:
            inputs[x[0]] = QLineEdit(parent)
            inputs[x[0]].textEdited.connect(self.get_value)
        return inputs

    def make_dropdowns(self, parent):
        boxes = {}
        for x in self.parameter_list:
            boxes[x[0]] = MyComboBox(parent, start_unit, x[1])
            boxes[x[0]].currentTextChanged.connect(self.get_unit)
        return boxes

    def make_tab1_layout(self, parent):
        layout = QGridLayout(parent)
        layout.labels = self.make_labels(parent)
        layout.inputs = self.make_inputs(parent)
        layout.boxes = self.make_dropdowns(parent)
        i = 0
        j = 1
        for x in self.parameter_list:
            layout.addWidget(layout.labels[x[0]], (i % 6) + 1, j)
            layout.addWidget(layout.inputs[x[0]], (i % 6) + 1, j + 1)
            layout.addWidget(layout.boxes[x[0]], (i % 6) + 1, j + 2)
            i = i + 1
            if i >= 6:
                j = 4
        return layout

    def make_tab2_tree(self, parent):
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
                cur = float(self.tab1.layout.inputs[x[0]].text())
            except ValueError:
                cur = 0.0
            self.parent.value[x[0]] = cur

    def get_unit(self, text):
        for x in self.parameter_list:
            self.parent.unit[x[0]] = self.tab1.layout.boxes[x[0]].currentText()

    def update_parameters(self):
        old_state = {}
        for x in self.tab1.layout.boxes:
            old_state[x] = self.tab1.layout.boxes[x].blockSignals(True)
        for x in self.parameter_list:
            self.tab1.layout.inputs[x[0]].setText(self.parent.value[x[0]])
            self.tab1.layout.boxes[x[0]].setCurrentText(self.parent.unit[x[0]])
        for x in self.tab1.layout.boxes:
            self.tab1.layout.boxes[x].blockSignals(old_state[x])

    def update_units(self, item, col):
        for x in self.parameter_list:
            while self.tab1.layout.boxes[x[0]].count() > 1:
                self.tab1.layout.boxes[x[0]].removeItem(1)
        for x in range(self.tab2.tree_view.units.childCount()):
            if (self.tab2.tree_view.units.child(x).checkState(0) & Qt.Checked):
                for p in self.parameter_list:
                    for k in self.unit_list[x][p[1]]:
                        if self.tab1.layout.boxes[p[0]].findText(k) == -1:
                            self.tab1.layout.boxes[p[0]].addItem(k)

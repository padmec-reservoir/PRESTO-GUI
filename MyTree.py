from PyQt5.QtWidgets import (QTreeWidget, QWidget, QGridLayout, QPushButton,
                             QLabel, QLineEdit, QComboBox)
from PyQt5.QtCore import Qt
from MyTreeItem import MyTreeItem
from parameters import entries, well

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

    def make_screen(self, name):
        cur = self.roots[name]
        cur.screen = QWidget()
        cur.screen.layout = QGridLayout(cur.screen)
        cur.screen.layout.setAlignment(Qt.AlignTop)
        if name == "Wells (Geometry)":
            cur.buttons = {}
            k = "New Injection Well"
            cur.buttons[k] = QPushButton(k, cur.screen)
            cur.buttons[k].clicked.connect(self.make_inwell)
            k = "New Producer Well"
            cur.buttons[k] = QPushButton(k, cur.screen)
            cur.buttons[k].clicked.connect(self.make_outwell)
            i = 1
            for x in cur.buttons.values():
                cur.screen.layout.addWidget(x, i, 1)
                i += 1

    def make_inwell(self, clckd):
        cur = self.roots["Wells (Geometry)"]
        name = "Injection Well "+str(len(cur.itens) + 1)
        cur.itens[name] = MyTreeItem(cur, name, [])
        cur.addChild(cur.itens[name])
        self.make_well(cur.itens[name], name)

    def make_outwell(self, clckd):
        cur = self.roots["Wells (Geometry)"]
        name = "Producer Well "+str(len(cur.itens) + 1)
        cur.itens[name] = MyTreeItem(cur, name, [])
        cur.addChild(cur.itens[name])
        self.make_well(cur.itens[name], name)

    def make_well(self, cur, name):
        cur.name = name
        cur.screen = QWidget()
        cur.screen.layout = QGridLayout(cur.screen)
        cur.screen.layout.setAlignment(Qt.AlignTop)
        cur.labels = {}
        cur.inputs = {}
        cur.boxes = {}
        '''cur.labels["Rename"] = QLabel("Name", cur.screen)
        cur.inputs["Rename"] = QLineEdit(cur.screen)
        cur.inputs["Rename"].setText(name)
        cur.inputs["Rename"].textEdited.connect(self.update_well_name)
        cur.screen.layout.addWidget(cur.labels["Rename"], 1, 1)
        cur.screen.layout.addWidget(cur.inputs["Rename"], 1, 2)
        i = 2'''
        i = 1
        for x in well:
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

    def get_selected(self):
        for x in self.roots.values():
            if x.isSelected():
                return x
            elif x.get_selected():
                return x.get_selected()
        return 0

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
        pass

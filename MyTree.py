from PyQt5.QtWidgets import QTreeWidget
from MyTreeItem import MyTreeItem
from parameters import roots, leafs

class MyTree(QTreeWidget):
    def __init__(self, parent, name):
        super(MyTree, self).__init__(parent)
        self.setHeaderLabel(name)
        self.roots = {}
        for x in roots:
            self.roots[x] = MyTreeItem(self, x, leafs[x])
            self.addTopLevelItem(self.roots[x])

    def get_selected(self):
        for x in self.roots:
            if self.roots[x].isSelected():
                return self.roots[x]
        for x in self.roots:
            if self.roots[x].get_selected():
                return self.roots[x].get_selected()

    def aaaa(self):
        print(self.get_selected().text(0))

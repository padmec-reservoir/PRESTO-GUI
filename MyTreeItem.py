from PyQt5.QtWidgets import QTreeWidgetItem

class MyTreeItem(QTreeWidgetItem):
    def __init__(self, parent, name, leafs):
        super(MyTreeItem, self).__init__(parent, [name])
        self.itens = {}
        if isinstance(leafs, dict):
            for x in leafs:
                self.itens[x] = MyTreeItem(self, x, leafs[x])
                self.addChild(self.itens[x])
        else:
            for x in leafs:
                self.itens[x] = QTreeWidgetItem(self, [x])
                self.addChild(self.itens[x])

    def get_selected(self):
        for x in self.itens:
            if self.itens[x].isSelected():
                return self.itens[x]
        for x in self.itens:
            if isinstance(self.itens[x], MyTreeItem):
                if self.itens[x].get_selected():
                    return self.itens[x].get_selected()

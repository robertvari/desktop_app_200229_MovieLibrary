from PySide2.QtWidgets import QTreeWidget, QTreeWidgetItem


class CategorySelector(QTreeWidget):
    def __init__(self):
        super(CategorySelector, self).__init__()
        self.setMaximumWidth(200)
        self.setHeaderHidden(True)

        self.refresh()

    def refresh(self):
        self.clear()


class CategoryItem(QTreeWidgetItem):
    def __init__(self, parent, name):
        super(CategoryItem, self).__init__(parent)
        self.setText(0, str(name))

        self.setExpanded(True)
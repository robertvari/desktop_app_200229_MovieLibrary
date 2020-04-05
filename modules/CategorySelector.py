from PySide2.QtWidgets import QTreeWidget, QTreeWidgetItem
from PySide2.QtCore import Signal, Qt

from nodes.database import Client


class CategorySelector(QTreeWidget):
    client = Client()
    filter_activated = Signal(dict)

    def __init__(self):
        super(CategorySelector, self).__init__()
        self.setMaximumWidth(200)
        self.setHeaderHidden(True)
        self.setSelectionMode(QTreeWidget.ExtendedSelection)
        self.itemSelectionChanged.connect(self.get_filter)

        self.refresh()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.clearSelection()

    def get_filter(self):
        selected_items = self.selectedItems()

        filter_set = []

        for item in selected_items:
            if isinstance(item, ParentCategory):
                continue
            filter_set.append(item.name)

        self.filter_activated.emit(set(filter_set))

    def refresh(self):
        self.clear()

        release_date_category = ParentCategory("Release Date", self)
        for date in self.client.get_release_dates():
            CategoryItem(date, release_date_category)

        language_category = ParentCategory("Language", self)
        for languge in self.client.get_languages():
            CategoryItem(languge, language_category)

        genre_category = ParentCategory("Genre", self)
        for genre in self.client.get_genres():
            CategoryItem(genre, genre_category)


class ParentCategory(QTreeWidgetItem):
    def __init__(self, name, parent):
        super(ParentCategory, self).__init__(parent)
        self.name = name
        self.setText(0, name)
        self.setExpanded(True)


class CategoryItem(QTreeWidgetItem):
    def __init__(self, name, parent):
        super(CategoryItem, self).__init__(parent)
        self.name = name
        self.setText(0, str(name))

        self.setExpanded(True)
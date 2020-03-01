from PySide2.QtWidgets import QTreeWidget, QTreeWidgetItem

data_dict = {
    "genre": [
        "action",
        "comedy",
        "thriller",
        "horror",
        "sci-fi",
    ],

    "year": [
        1970,
        1980,
        1990,
        2000,
    ],

    "language": [
        "eng",
        "hun",
        "fr",
    ]
}


class CategorySelector(QTreeWidget):
    def __init__(self):
        super(CategorySelector, self).__init__()
        self.setMaximumWidth(200)
        self.setHeaderHidden(True)

        self.refresh()

    def refresh(self):
        self.clear()

        for k, v in data_dict.items():
            top_item = CategoryItem(self, k)

            for i in v:
                CategoryItem(top_item, i)


class CategoryItem(QTreeWidgetItem):
    def __init__(self, parent, name):
        super(CategoryItem, self).__init__(parent)
        self.setText(0, str(name))
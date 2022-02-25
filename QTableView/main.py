import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QTableView

# QTreeView
# from PyQt6.QtWidgets import QAbstractItemView, QHBoxLayout, QPushButton
# from PyQt6.Qt import QStandardItemModel, QStandardItem, QItemSelectionModel
# from PyQt6.QtGui import QColor
# from PyQt6.QtCore import Qt


VERSIONS = ("001", "002", "008", "012")


# class TableModel(QtCore.QAbstractTableModel):
#     def __init__(self, data):
#         super(TableModel, self).__init__()
#         self._data = data

#     def data(self, index, role):
#         if role == Qt.DisplayRole:
#             # See below for the nested-list data structure.
#             # .row() indexes into the outer list,
#             # .column() indexes into the sub-list
#             return self._data[index.row()][index.column()]

#     def rowCount(self, index):
#         # The length of the outer list.
#         return len(self._data)

#     def columnCount(self, index):
#         # The following takes the first sub-list, and returns
#         # the length (only works if all rows are an equal length)
#         return len(self._data[0])


class Window(QDialog):
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("My Menu")
        # self.setFixedSize(400, 300)
        self._layout()

    def _layout(self):
        layout = QVBoxLayout()
        layout.addLayout(self._tableLayout())
        layout.addLayout(self._buttonLayout())
        self.setLayout(layout)

    def _tableLayout(self):
        layout = QVBoxLayout()

        return layout

    def _buttonLayout(self):
        layout = QHBoxLayout()
        btn = QPushButton("Submit")
        # btn.clicked.connect(self._printRow)
        layout.addWidget(btn)
        return layout


def main():
    app = QApplication(sys.argv)
    demo = Window()
    demo.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

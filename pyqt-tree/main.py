import sys
from PyQt5.QtWidgets import QDialog, QApplication, QTreeView, QVBoxLayout
from PyQt5.QtWidgets import QAbstractItemView, QHBoxLayout, QPushButton
from PyQt5.Qt import QStandardItemModel, QStandardItem, QItemSelectionModel
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt


VERSIONS = ("001", "002", "008", "012")


class Window(QDialog):
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("My Menu")
        self.setFixedSize(400, 300)
        self._layout()

    def _layout(self):
        layout = QVBoxLayout()
        layout.addLayout(self._treeLayout())
        layout.addLayout(self._buttonLayout())
        self.setLayout(layout)

    def _treeLayout(self):
        layout = QVBoxLayout()

        self.checkin_treeView = QTreeView()
        self.checkin_treeView.setAlternatingRowColors(True)
        # checkin_treeView.setRootIsDecorated(False)
        self.checkin_treeView.setSortingEnabled(True)

        # Make the tree view read-only

        # self.checkin_treeView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        checkin_standardItemModel = QStandardItemModel(0, 2)
        checkin_standardItemModel.setHorizontalHeaderLabels(("Name", "Frames"))

        for v in VERSIONS:
            checkin_standardItemModel.appendRow(
                (QStandardItem(v), QStandardItem("240"))
            )

        self.checkin_treeView.setModel(checkin_standardItemModel)
        layout.addWidget(self.checkin_treeView)
        return layout

    def _buttonLayout(self):
        layout = QHBoxLayout()
        btn = QPushButton("Submit")
        btn.clicked.connect(self._printRow)
        layout.addWidget(btn)
        return layout

    def _printRow(self):
        t = self.checkin_treeView
        print(t.currentIndex().data())


app = QApplication(sys.argv)
demo = Window()
demo.show()
sys.exit(app.exec_())

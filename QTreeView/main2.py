import re
import operator
import os
import sys
import sqlite3
import cookies
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QDialog, QApplication, QTreeView, QVBoxLayout, QWidget
from PyQt5.QtWidgets import QAbstractItemView, QHBoxLayout, QPushButton, QTableView
from PyQt5.Qt import QStandardItemModel, QStandardItem, QItemSelectionModel
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt


def main():
    app = QApplication(sys.argv)
    w = MyWindow()
    w.show()
    sys.exit(app.exec_())


class MyWindow(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)

        # data
        self.tabledata = [
            ("apple", "red", "small"),
            ("apple", "red", "medium"),
            ("apple", "green", "small"),
            ("banana", "yellow", "large"),
        ]
        self.header = ["fruit", "color", "size"]

        # create table
        self.createTable()

        # layout
        layout = QVBoxLayout()
        layout.addWidget(self.tv)
        self.setLayout(layout)

    def createTable(self):
        # create the view
        self.tv = QTableView()
        self.tv.setStyleSheet("gridline-color: rgb(191, 191, 191)")

        # set the table model
        tm = MyTableModel(self.tabledata, self.header, self)
        self.tv.setModel(tm)

        # set the minimum size
        self.tv.setMinimumSize(400, 300)

        # hide grid
        self.tv.setShowGrid(True)

        # set the font
        font = QFont("Calibri (Body)", 12)
        self.tv.setFont(font)

        # hide vertical header
        vh = self.tv.verticalHeader()
        vh.setVisible(False)

        # set horizontal header properties
        hh = self.tv.horizontalHeader()
        hh.setStretchLastSection(True)

        # set column width to fit contents
        self.tv.resizeColumnsToContents()

        # set row height
        nrows = len(self.tabledata)
        for row in range(nrows):
            self.tv.setRowHeight(row, 18)

        # enable sorting
        self.tv.setSortingEnabled(True)


class MyTableModel(QAbstractTableModel):
    def __init__(self, datain, headerdata, parent=None, *args):
        """datain: a list of lists
        headerdata: a list of strings
        """
        QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = datain
        self.headerdata = headerdata

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        return len(self.arraydata[0])

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
        return QVariant(self.arraydata[index.row()][index.column()])

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headerdata[col])
        return QVariant()

    def sort(self, Ncol, order):
        """Sort table by given column number."""
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.arraydata = sorted(self.arraydata, key=operator.itemgetter(Ncol))
        if order == Qt.DescendingOrder:
            self.arraydata.reverse()
        self.emit(SIGNAL("layoutChanged()"))


if __name__ == "__main__":
    main()

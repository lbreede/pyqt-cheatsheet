from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from functools import partial


GENERIC_LABEL_WIDTH = 150
MENU_WIDTH = 160
LINE_EDIT_WIDTH = 35
RESOLUTION_LABEL = "{nframes} ipmages at {x}x{y}"


class Window(QDialog):
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("My Menu")

        self.x = 1280
        self.y = 720

        self._layout()
        self._createMenu()

    def _layout(self):
        layout = QVBoxLayout()
        layout.addLayout(self._labelLayout())
        layout.addLayout(self._menuLayout())

        self.print_btn = QPushButton("Print")
        layout.addWidget(self.print_btn)

        self.setLayout(layout)

    def _labelLayout(self):
        layout = QHBoxLayout()

        label = QLabel("Current Resolution:")
        label.setFixedWidth(GENERIC_LABEL_WIDTH)
        label.setAlignment(Qt.AlignLeft)

        layout.addWidget(label)
        layout.addLayout(self._resolutionLayout())
        return layout

    def parseResolution(self):
        return self.x, self.y

    def _resolutionLayout(self):
        layout = QHBoxLayout()

        self.resolution = QLabel()
        self.resolution.setText(
            RESOLUTION_LABEL.format(nframes=240, x=self.x, y=self.y)
        )
        self.resolution.setFixedWidth(GENERIC_LABEL_WIDTH)
        layout.addWidget(self.resolution)

        return layout

    def _menuLayout(self):
        layout = QHBoxLayout()

        label = QLabel("Resolution:")
        combo_box = QComboBox()
        self.menu = QMenu()

        label.setFixedWidth(GENERIC_LABEL_WIDTH)
        self.menu.setFixedWidth(MENU_WIDTH)

        label.setAlignment(Qt.AlignLeft)

        layout.addWidget(label)
        layout.addWidget(self.menu)
        return layout

    def _createMenu(self):
        for r in self._readResolutions():
            if not r["isSeparator"]:
                action = self.menu.addAction(r["name"])
                action.triggered.connect(partial(self._updateResolution, r))
            else:
                self.menu.addSeparator()

    def _updateResolution(self, res):
        self.x, self.y = res["x"], res["y"]
        self.resolution.setText(
            RESOLUTION_LABEL.format(nframes=240, x=self.x, y=self.y)
        )

    def _readResolutions(self):

        with open("resolutions.txt") as f:
            linelist = f.read().split("\n")

        resolution_dict = []

        for line in linelist:

            a = line.split()

            if a[0] != "_separator_":

                x, y = list(map(int, a[0:2]))
                aspect = float(a[2])
                name = " ".join(a[3:])
                resolution_dict.append(
                    {
                        "name": name,
                        "x": x,
                        "y": y,
                        "aspect": aspect,
                        "isSeparator": False,
                    }
                )

            else:
                resolution_dict.append(
                    {
                        "name": None,
                        "x": None,
                        "y": None,
                        "aspect": None,
                        "isSeparator": True,
                    }
                )

        return resolution_dict

import sys

from PyQt5.QtWidgets import QApplication

from view import Window
from controller import Ctrl


def main():
    app = QApplication(sys.argv)
    view = Window()
    view.show()
    Ctrl(view)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

import sys

from PyQt5.QtWidgets import QApplication

from model import evaluateExpression
from view import PyCalcUi
from controller import PyCalcCtrl

__version__ = "0.1"
__author__ = "Lennart Breede"


def main():
    pycalc = QApplication(sys.argv)
    model = evaluateExpression
    view = PyCalcUi()
    view.show()
    PyCalcCtrl(model=model, view=view)
    sys.exit(pycalc.exec_())


if __name__ == "__main__":
    main()

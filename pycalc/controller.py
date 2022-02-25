from functools import partial

__version__ = "0.1"
__author__ = "Lennart Breede"

ERROR_MSG = "ERROR"

class PyCalcCtrl:
	def __init__(self, model, view):
		self._evaluate = model
		self._view = view
		self._connectSignals()

	def _calculateResult(self):
		result = self._evaluate(expression=self._view.displayText())
		self._view.setDisplayText(result)

	def _buildExpression(self, sub_exp):
		if self._view.displayText() == ERROR_MSG:
			self._view.clearDisplay()

		expression = self._view.displayText() + sub_exp
		self._view.setDisplayText(expression)

	def _connectSignals(self):
		for btnText, btn in self._view.buttons.items():
			if btnText not in {"=", "C"}:
				btn.clicked.connect(partial(self._buildExpression, btnText))

		self._view.buttons["="].clicked.connect(self._calculateResult)
		self._view.display.returnPressed.connect(self._calculateResult)
		self._view.buttons["C"].clicked.connect(self._view.clearDisplay)
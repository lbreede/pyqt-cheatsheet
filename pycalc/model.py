__version__ = "0.1"
__author__ = "Lennart Breede"

ERROR_MSG = "ERROR"

def evaluateExpression(expression):
	try:
		result = str(eval(expression, {}, {}))
	except Exception:
		result = ERROR_MSG

	return result
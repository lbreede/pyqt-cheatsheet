class Ctrl:
    def __init__(self, view):
        self._view = view
        self._connectSignals()

    def _connectSignals(self):
        self._view.print_btn.clicked.connect(self._printResolution)

    def _printResolution(self):
        x, y = self._view.parseResolution()
        print(f"Current Resolution: {x}x{y}")

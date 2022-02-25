import sys
import functools

from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtWidgets import QWidget

def greeting(who):
    if msg.text():
        msg.setText('')
    else:
        msg.setText(f'Hello {who}!')

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('Signals, and slots')
window.setGeometry(100, 100, 280, 80)
layout = QVBoxLayout()
btn = QPushButton('Greet')
btn.clicked.connect(functools.partial(greeting, "Mark"))
layout.addWidget(btn)
msg = QLabel('')
layout.addWidget(msg)
window.setLayout(layout)
window.show()
sys.exit(app.exec_())
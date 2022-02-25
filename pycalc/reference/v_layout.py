import sys

from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("QVBoxLayout")
layout = QVBoxLayout()
layout.addWidget(QPushButton("Top"))
layout.addWidget(QPushButton("Center"))
layout.addWidget(QPushButton("Bottom"))
window.setLayout(layout)
window.show()
sys.exit(app.exec_())
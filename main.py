import sys
from PyQt6.QtWidgets import QApplication, QLabel

app = QApplication(sys.argv)
window = QLabel("Мой Менеджер Паролей!")
window.resize(400, 200)
window.show()

sys.exit(app.exec())
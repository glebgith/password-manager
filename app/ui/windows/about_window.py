from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("О программе")
        self.setWindowIcon(QIcon("icon.png"))
        self.resize(400, 300)
        self.setStyleSheet("background-color: #1E1E2E; color: #E4E4F0;")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(15)

        title = QLabel("Менеджер паролей")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #7C6AF7;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        info = QLabel("Курсовой проект\n\nСтудент: ТВОЁ ФИО\nГруппа: ТВОЯ ГРУППА\n\nСтек: Python, PyQt6, SQLite, AES-GCM")
        info.setStyleSheet("font-size: 14px; color: #A0A0B8;")
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info)

        btn = QPushButton("Закрыть")
        btn.setStyleSheet("background-color: #F87171; color: white; padding: 8px; border-radius: 5px; font-weight: bold;")
        btn.clicked.connect(self.close)
        layout.addWidget(btn)
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
import random
import string

class AddPasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить запись")
        self.resize(400, 350)
        self.setStyleSheet("background-color: #1E1E2E; color: #E4E4F0;")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Название (например, Google)")
        self.title_input.setStyleSheet("padding: 10px; border-radius: 5px; background-color: #2A2A3E; color: white; border: 1px solid #3A3A4E;")
        layout.addWidget(self.title_input)

        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Логин (email)")
        self.login_input.setStyleSheet("padding: 10px; border-radius: 5px; background-color: #2A2A3E; color: white; border: 1px solid #3A3A4E;")
        layout.addWidget(self.login_input)

        pass_layout = QHBoxLayout()
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setStyleSheet("padding: 10px; border-radius: 5px; background-color: #2A2A3E; color: white; border: 1px solid #3A3A4E;")
        pass_layout.addWidget(self.password_input)

        self.gen_btn = QPushButton("Сгенерировать")
        self.gen_btn.setStyleSheet("background-color: #7C6AF7; color: white; padding: 8px; border-radius: 5px; font-weight: bold;")
        self.gen_btn.clicked.connect(self.generate_password)
        pass_layout.addWidget(self.gen_btn)
        layout.addLayout(pass_layout)

        self.save_btn = QPushButton("Сохранить")
        self.save_btn.setStyleSheet("background-color: #7C6AF7; color: white; padding: 12px; border-radius: 5px; font-weight: bold; margin-top: 10px;")
        self.save_btn.clicked.connect(self.accept)
        layout.addWidget(self.save_btn)

    def generate_password(self):
        characters = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(random.choice(characters) for i in range(12))
        self.password_input.setText(password)

    def get_data(self):
        return (
            self.title_input.text(),
            self.login_input.text(),
            self.password_input.text()
        )